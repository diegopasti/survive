import pygame
import socket
import json

DEBUG_LOG = True


class ClientGame:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conect()

    def get_data_from_server(self, log=DEBUG_LOG):
        response = self.client_game.recv(4096).decode()
        response = json.loads(response)
        if log:
            print("server:",response)
        return response

    def send_data_to_server(self, request, log=DEBUG_LOG):
        try:
            request['event_counter'] = self.data_game['event_counter']
        except:
            request['event_counter'] = 0
        if log:
            print("client:",request)
        self.send(request)

    def conect(self):
        self.client_game.connect((self.server_ip, int(self.server_port)))

    def send(self, request_dict):
        data = json.dumps(request_dict)
        self.client_game.sendall(bytes(data, 'UTF-8'))

    def close(self):
        self.client_game.close()


class KeyBoardControll:

    def verify_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = False
            if event.type == pygame.MOUSEBUTTONUP:
                new_position = pygame.mouse.get_pos()

                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    self.player.move_to(new_position, running=True)
                else:
                    self.player.move_to(new_position, running=False)

        request_event = {'player':self.player.name, 'command':'move', 'data':{'position':self.player.get_position(),'destination': self.player.get_destination(),'running':self.player.running}}
        return request_event

        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.player.walk(SOUTH_WEST)

        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.player.walk(SOUTH_EAST)

        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.player.walk(NORTH_WEST)

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.player.walk(NORTH_EAST)

        if keys[pygame.K_DOWN]:
            self.player.walk(SOUTH)
        if keys[pygame.K_LEFT]:
            self.player.walk(WEST)
        elif keys[pygame.K_UP]:
            self.player.walk(NORTH)
        elif keys[pygame.K_RIGHT]:
            self.player.walk(EAST)
        else:
            pass



        ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = False

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                    self.player.walk(SOUTH_WEST)

                if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                    self.player.walk(SOUTH_EAST)

                if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                    self.player.walk(NORTH_WEST)

                if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                    self.player.walk(NORTH_EAST)

                if keys[pygame.K_DOWN]:
                    self.player.walk(SOUTH)
                if keys[pygame.K_LEFT]:
                    self.player.walk(WEST)
                elif keys[pygame.K_UP]:
                    self.player.walk(NORTH)
                elif keys[pygame.K_RIGHT]:
                    self.player.walk(EAST)
                else:
                    pass
                    #self.player.stop()

            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.walk(WEST)
                elif keys[pygame.K_UP]:
                    self.player.walk(NORTH)
                elif keys[pygame.K_RIGHT]:
                    self.player.walk(EAST)
                elif keys[pygame.K_DOWN]:
                    self.player.walk(SOUTH)
                else:
                    self.player.stop()

                #if event.key == pygame.K_WEST or event.key == pygame.K_EAST or event.key == pygame.K_NORTH or event.key == pygame.K_SOUTH:
                # if event.type == pygame.MOUSEBUTTONNORTH:
                #    pos = pygame.mouse.get_pos()
                #    self.player.move_to(pos[0],pos[1])
        ""
        """
