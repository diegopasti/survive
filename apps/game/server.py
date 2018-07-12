import json
import socket, threading

import sys

DATA_SERVER = {}
DATA_SERVER['events'] = {}
DATA_SERVER['event_counter'] = 0
DATA_SERVER['players_online'] = 0
DATA_SERVER['players']  = {}


EVENTS_SERVER = {}

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
        self.client_socket.close()

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.client_socket = clientsocket
        self.client_address = clientAddress
        self.client_name    = None
        print("server: New client on", self.client_address)

    def send_data_to_client(self, data=DATA_SERVER):
        #print(" - response:", data)
        self.send(data)

    def send(self, request_dict):
        data = json.dumps(request_dict)
        self.client_socket.sendall(bytes(data, 'UTF-8'))

    def verify_message(self, log=True):
        try:
            data = self.client_socket.recv(4096)
            if data is not None:
                response = data.decode()
                response = json.loads(response)
                if log:
                    print("client:", response)
            else:
                print("client: Falha na requisicao", end="")
            return response
        except:
            return None

    def get_event_number(self):
        return DATA_SERVER['event_counter']

    def increment_event_number(self):
        DATA_SERVER['event_counter'] = DATA_SERVER['event_counter'] + 1

    def save_event(self, request):
        self.increment_event_number()
        event_number = self.get_event_number()
        request['id'] = event_number
        request['status'] = True
        DATA_SERVER['events'][self.client_name] = request#[event_number] = request
        return DATA_SERVER#['events']#[self.client_name]#[event_number]

    def increment_users_online(self, request):
        DATA_SERVER['players'][self.client_name] = request['player']
        DATA_SERVER['players_online'] = DATA_SERVER['players_online'] + 1

    def create_player(self, request):
        self.client_name = request['player']['name']
        self.increment_users_online(request)
        self.save_event(request)
        self.response(DATA_SERVER)

    def move_player(self,request):
        DATA_SERVER['players'][self.client_name]['position'] = request['data']['position']
        self.response(self.save_event(request))

    def response(self,request):
        self.send_data_to_client(request)

    def run(self):
        print("server: Process started with", self.client_address)
        #self.client_socket.send(bytes("Hi, This is from Server..",'utf-8'))
        response = {}

        while True:
            request = self.verify_message(log=False)
            if request is not None:
                if request['command'] == "create_player":
                    print("server: create player",request)
                    self.create_player(request)

                elif request['command'] == 'move':
                    self.move_player(request)
                    #self.increment_event_number()
                    #event_number = self.get_event_number()
                    #DATA_SERVER['events'][self.client_name][event_number] = {'id': event_number, 'request': request, 'status':True}

                    """
                    response_list = []
                    diff_events = DATA_SERVER['events']['event_counter'] - request['event_counter']

                    if diff_events>1:
                        request_event_id = request['event_counter']+1
                        last_event_id = DATA_SERVER['events']['event_counter']
                        for item in range(request_event_id,last_event_id):
                            response_list.append(DATA_SERVER['events'][item])
                    elif diff_events==1:
                        response_list.append(DATA_SERVER['events'][self.client_name][event_number])
                    else:
                        print("A DIFERENCA ENTRE O CONTADOR DE EVENTO DO CLIENTE E SERVIDOR DEU ZERO OU MENOR.. ESTRANHO")
                    
                    self.send_data_to_client(response_list)
                    """

                elif request['command'] == "verify_server":
                    # response['command'] = request['command']
                    # response["status"] = "accept"
                    # response['data'] = DATA_SERVER
                    # response['events'] = EVENTS_SERVER
                    self.send_data_to_client(DATA_SERVER)


            else:
                break
            """
            if request is not None:
                if request['command']=="update":
                    response['command'] = request['command']
                    response["status"] = "accept"
                    response['data'] = DATA_SERVER
                    response['events'] = EVENTS_SERVER
                    self.send_data_to_client(response)

                elif request['command']=="create_player":
                    self.client_name = request['player']['name']
                    DATA_SERVER[request['player']['name']] = request['player']
                    EVENTS_SERVER['events'] = request['command']
                    EVENTS_SERVER['events_values'] = request['player']
                    response['command'] = request['command']
                    response["status"] = "accept"
                    response['data'] = DATA_SERVER
                    response['events'] = EVENTS_SERVER
                    self.send_data_to_client(response)
                    #print("VEJA O QUE SOBROU DATA_SERVER: ",DATA_SERVER)

                elif request['command'] == "verify_server":
                    #response['command'] = request['command']
                    #response["status"] = "accept"
                    #response['data'] = DATA_SERVER
                    #response['events'] = EVENTS_SERVER
                    self.send_data_to_client(response)

                elif response['command'] == 'exit':
                    response = {'command': 'exit', 'status': 'accept'}
                    self.send_data_to_client(response)
                    break
                else:
                    response = {'command': 'nothing', 'status': 'accept'}
                    self.send_data_to_client(response)
            else:
                break
            """
        DATA_SERVER['players'].pop(self.client_name)
        print("Client at ", self.client_address, " disconnected...")
        sys.exit()


if __name__=="__main__":
    Server("127.0.0.1","9000").start()