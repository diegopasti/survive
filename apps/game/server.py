import json
import socket, threading


DATA_SERVER = {}

class Server:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.server_ip, int(self.server_port)))

    def start(self):
        print("Server: Start application")
        print("Server: Waiting for client request..")
        while True:
            self.server.listen(1)
            clientsock, clientAddress = self.server.accept()
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.client_socket = clientsocket
        self.client_address = clientAddress
        self.client_name    = None
        print("server: New client on", self.client_address)

    def send_data_to_client(self, data=DATA_SERVER):
        print(" - response:", data)
        self.send(data)

    def send(self, request_dict):
        data = json.dumps(request_dict)
        self.client_socket.sendall(bytes(data, 'UTF-8'))

    def verify_message(self):
        data = self.client_socket.recv(4096)
        response = data.decode()
        response = json.loads(response)
        print("client:", response, end="")
        return response

    def run(self):
        print("server: Process started with", self.client_address)
        #self.client_socket.send(bytes("Hi, This is from Server..",'utf-8'))

        while True:
            request = self.verify_message()
            if request['command']=="event":
                DATA_SERVER[self.client_name] = request[self.client_name]
                response = {'command': 'event', 'status': 'accept'}
                self.send_data_to_client(response)

            elif request['command']=="create_player":
                DATA_SERVER[request['player']['name']] = request['player']
                response = {'command':'create_player','status':'accept'}
                self.client_name = request['player']['name']
                self.send_data_to_client(response)


            elif response['command'] == 'exit':
                response = {'command': 'exit', 'status': 'accept'}
                self.send_data_to_client(response)
                break
            else:
                response = {'command': 'nothing', 'status': 'accept'}
                self.send_data_to_client(response)
                self.send_data_to_client()
        print("Client at ", self.client_address, " disconnected...")


if __name__=="__main__":
    Server("127.0.0.1","9000").start()