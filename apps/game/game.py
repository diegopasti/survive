from apps.main.utils import Coordinate
from survive.settings import BASE_DIR
from survive import settings
import random
import socket
import pygame
import json
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define directions
SOUTH = 1
SOUTH_WEST = 2
WEST = 3
NORTH_WEST = 4
NORTH = 5
NORTH_EAST = 6
EAST = 7
SOUTH_EAST = 8

# Define other variables
CHARACTERS_DIRS = os.path.join(settings.BASE_DIR, 'static/images/chars/')


class Object:
    image_path = None
    image = None

    width = None
    height = None
    position = None



    def __init__(self,x,y,w,h):
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.position = Coordinate(x,y)

    def get_position(self):
        return (self.position.x, self.position.y)

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def get_size(self):
        return (self.width,self.height)

    def set_size(self, width, heigth):
        self.width = width
        self.height = heigth

class Ground(Object):
    image_path = BASE_DIR + "/static/images/tiles/grass-3.jpg"

class Tree(Object):
    pass

class Pine(Tree):
    image_path = BASE_DIR+"/static/images/trees/pine_tree/pine_tree.png"

class Pine2(Tree):
    image_path = BASE_DIR+"/static/images/trees/pine_tree/pine_tree-2.png"

class Pine3(Tree):
    image_path = BASE_DIR+"/static/images/trees/pine_tree/pine_tree-3.png"

class Birch(Tree):
    image_path = BASE_DIR+ "/static/images/trees/birch_tree/birch_tree.png"

class Birch2(Tree):
    image_path = BASE_DIR+ "/static/images/trees/birch_tree/birch_tree-2.png"

class Birch3(Tree):
    image_path = BASE_DIR+ "/static/images/trees/birch_tree/birch_tree-3.png"

class Oak(Tree):
    image_path = BASE_DIR + "/static/images/trees/oak_tree/oak_tree.png"

class Oak2(Tree):
    image_path = BASE_DIR + "/static/images/trees/oak_tree/oak_tree-2.png"

class Oak3(Tree):
    image_path = BASE_DIR + "/static/images/trees/oak_tree/oak_tree-3.png"

class Tropical(Tree):
    image_path = BASE_DIR+ "/static/images/trees/tropical_tree/tropical_tree.png"

class Tropical2(Tree):
    image_path = BASE_DIR+ "/static/images/trees/tropical_tree/tropical_tree-2.png"

class Tropical3(Tree):
    image_path = BASE_DIR+ "/static/images/trees/tropical_tree/tropical_tree-3.png"

class Element(Object):
    image_number = None
    image_level = None
    file_image = None

    image = None

    sprite_number = 1
    direction = NORTH
    destination = None
    
    def update(self):
        pass

    def load_image(self, image_number, image_level=1):
        self.image_number = image_number
        self.image_level = image_level
        self.image_path = CHARACTERS_DIRS + str(self.image_number) + "/" + str(self.image_level) + ".png"

        self.image = pygame.image.load(self.image_path)
        self.width = self.image.get_width()/4
        self.height = self.image.get_height()/4
    """
    def change_sprite(self):
        self.sprite = pygame.Rect(self.get_sprite_coordinate(), self.get_size())
        return self.sprite
    
    def get_sprite_coordinate(self):
        coord_x = (self.sprite_number-1)*self.width
        coord_y = (self.direction-1)*self.height
        return (coord_x, coord_y)

    def change_sprite_number(self):
        if self.sprite_number < 4:
            self.sprite_number = self.sprite_number + 1
        else:
            self.sprite_number = 1
        return self.sprite_number
    """

    def get_destination(self):
        if self.destination is not None:
            return (self.destination.x,self.destination.y)
        else:
            return None

class Sequence:

    def __init__(self, image, direction, sprite_numbers, total_sequences):
        self.base_image = image
        self.sprite_numbers = sprite_numbers
        self.total_sequences = total_sequences

        self.current_sprite = 1
        self.direction = direction
        self.width = self.base_image.get_width() / sprite_numbers
        self.height = self.base_image.get_height() / total_sequences

        self.sequences = []
        self.save_sprites()

    def update(self):
        self.current_sprite = self.current_sprite + 1
        if self.current_sprite < self.sprite_numbers:
            self.current_sprite = self.current_sprite + 1
        else:
            self.reset_sequence()


    def reset_sequence(self):
        self.current_sprite = 1

    def save_sprites(self):
        for item in range(self.sprite_numbers):
            sprite = self.get_sprite(item+1)
            self.sequences.append(sprite)

    def get_current_sprite(self):
        return self.sequences[self.current_sprite-1]
        #return self.get_sprite(self.current_sprite)


    def get_sprite(self,sequence_number):
        origin = self.get_sprite_coordinate(sequence_number)
        sprite = pygame.Rect(origin, self.get_size())
        return sprite

    def get_sprite_coordinate(self, sprite_number):
        #print("NUMBER: ",sprite_number," -  WIDTH:",self.width," - HEIGHT:",self.height)
        coord_x = (sprite_number - 1) * self.width
        coord_y = (self.direction - 1) * self.height
        return (coord_x, coord_y)

    def get_size(self):
        return (self.width,self.height)


class Animations:

    directions = {}
    current_direction = SOUTH
    current_animation = None
    current_image = None

    def __init__(self, simple_directions_image_path, diagonal_directions_image_path):
        self.simple_directions_image_path = simple_directions_image_path
        self.simple_directions_image = pygame.image.load(self.simple_directions_image_path)

        self.directions[SOUTH] = Sequence(self.simple_directions_image, 1, 8, 4)
        self.directions[WEST]  = Sequence(self.simple_directions_image, 2, 8, 4)
        self.directions[NORTH] = Sequence(self.simple_directions_image, 4, 8, 4)
        self.directions[EAST]  = Sequence(self.simple_directions_image, 3, 8, 4)

        self.diagonal_directions_image_path = diagonal_directions_image_path
        self.diagonal_directions_image = pygame.image.load(self.diagonal_directions_image_path)
        self.directions[SOUTH_WEST] = Sequence(self.diagonal_directions_image, 1, 8, 4)
        self.directions[NORTH_WEST] = Sequence(self.diagonal_directions_image, 2, 8, 4)
        self.directions[NORTH_EAST] = Sequence(self.diagonal_directions_image, 4, 8, 4)
        self.directions[SOUTH_EAST] = Sequence(self.diagonal_directions_image, 3, 8, 4)
        self.change_direction(SOUTH)

    def get_current_sprite(self):
        sprite = self.current_animation.get_current_sprite()
        #print("PEGAR DIRECAO:",self.current_direction," - CURRENT_SPRITE: ",sprite)
        return sprite # get_sprite(self.directions[self.current_direction].current_sprite)

    def update(self):
        self.current_animation.update()

    def change_direction(self, direction):
        self.current_direction = direction
        if self.current_direction == 1 or self.current_direction == 3 or self.current_direction == 5 or self.current_direction == 7:
            self.current_image = self.simple_directions_image
        else:
            self.current_image = self.diagonal_directions_image
        self.current_animation = self.directions[self.current_direction]
        #self.current_animation.reset_sequence()


class Monster(Element):
    pass

class Character(Element):

    animations = {}
    current_animation = None

    direction = 1
    sprite_number = 1

    speed = 6

    walking = None
    destination = None

    def __init__(self, player_name, char_number, position=None):
        self.name = player_name
        self.char_number = char_number
        self.image_path = os.path.join(settings.BASE_DIR, 'static/images/beta/chars/'+str(char_number)+'/')
        simple_directions_images = self.image_path+"basic.png"
        diagonal_directions_image = self.image_path+"diagonal.png"
        if position is None:
            init_x = random.randint(50, 750)
            init_y = random.randint(50, 550)
            self.position = Coordinate(init_x, init_y)
        else:
            self.position = position
        self.animations['walking'] = Animations(simple_directions_images,diagonal_directions_image)
        self.current_animation = self.animations['walking']
        self.set_size(self.current_animation.current_image.get_width() / 8, self.current_animation.current_image.get_height() / 4)

    def move_to(self, position):
        self.destination = Coordinate(position[0],position[1])

    def get_center_image(self):
        x = self.position.x+self.width/2
        y = self.position.y+self.height/2
        return Coordinate(x,y)

    def update(self, screen):
        if self.destination is not None:
            self.origin = self.get_center_image()
            pygame.draw.line(screen, BLACK, [self.origin.x, self.origin.y], [self.destination.x, self.destination.y], 1)
            self.destination_distance = self.origin.get_distance(self.destination)
            self.destination_time = self.destination_distance / self.speed

            variation_x = self.width/6
            variation_y = self.height/6


            if self.destination_distance < 2:
                #print("TO PERTO.. VOU PARAR POR AQUI MSM")
                self.destination = None
                self.stop()

                #elif self.origin.x < self.destination.x:
            elif self.destination.x > self.origin.x+variation_x:
                #print("VAMOS PRA DIREITA..",end="")
                if self.destination.y > self.origin.y+variation_y:
                    #print("E VAMOS DESCER")
                    self.walk(SOUTH_EAST)
                elif self.destination.y < self.origin.y-variation_y:
                    #print("E VAMOS SUBIR")
                    self.walk(NORTH_EAST)
                else:
                    #print("RETO. DEVE ESTAR ENTRE 3/6 e 4/6")
                    self.walk(EAST)

            elif self.destination.x < self.origin.x-variation_x:
                #print("VAMOS PRA ESQUERDA..", end="")
                if self.destination.y > self.origin.y+variation_y:
                    #print("E VAMOS DESCER")
                    self.walk(SOUTH_WEST)
                elif self.destination.y < self.origin.y - variation_y:
                    #print("E VAMOS SUBIR")
                    self.walk(NORTH_WEST)
                else:
                    #print("RETO")
                    self.walk(WEST)
            else:
                #print("VOU RETO..", end="")
                if self.destination.y > self.origin.y + variation_y:
                    #print("PRA BAIXO")
                    self.walk(SOUTH)
                elif self.destination.y < self.origin.y - variation_y:
                    #print("PRA CIMA")
                    self.walk(NORTH)
                else:
                    #print("FICAR PARADO")
                    self.destination = None
                    self.stop()
            self.current_animation.update()


        else:
            #print("COMO MOVER O PERSONAGEM SE NAO SEI PRA ONDE ELE ESTA INDO? kk")
            self.origin = self.get_center_image()
        screen.blit(self.current_animation.current_image, self.get_position(), self.current_animation.get_current_sprite())



        """if self.walking is not None:
            self.walk(self.current_animation.current_direction)
            self.current_animation.update()
        else:
            self.current_animation.change_direction(SOUTH)
        """

    def walk(self, direction):
        self.walking = direction
        #print("MAS ANDO A :",self.speed,"/SEG.. LOGO VOU LEVAR ",self.destination_distance/self.speed," SEGUNDOS PRA CHEGAR")
        variacao_x = (self.destination.x - self.origin.x)/self.destination_time
        variacao_y = (self.destination.y - self.origin.y)/self.destination_time

        if variacao_x < 0:
            variacao_x = variacao_x * -1
        if variacao_y < 0:
            variacao_y = variacao_y * -1

        #print("DESLOCAR EM X:",variacao_x)
        #print("DESLOCAR EM Y:", variacao_y)

        self.current_animation.change_direction(direction)
        if direction == NORTH:
            self.position.y = self.position.y - variacao_y
        elif direction == EAST:
            self.position.x = self.position.x + variacao_x
        elif direction == SOUTH:
            self.position.y = self.position.y + variacao_y
        elif direction == WEST:
            self.position.x = self.position.x - variacao_x

        elif direction == NORTH_EAST:
            self.position.y = self.position.y - variacao_y
            self.position.x = self.position.x + variacao_x
        elif direction == SOUTH_EAST:
            self.position.x = self.position.x + variacao_x
            self.position.y = self.position.y + variacao_y
        elif direction == SOUTH_WEST:
            self.position.x = self.position.x - variacao_x
            self.position.y = self.position.y + variacao_y
        elif direction == NORTH_WEST:
            self.position.x = self.position.x - variacao_x
            self.position.y = self.position.y - variacao_y
        else:
            pass

        #self.change_sprite_number()
        #self.current_animation.update()

    def stop(self):
        self.walking = None
        self.current_animation.change_direction(SOUTH)
        #self.direction = SOUTH

    def get_data(self):
        position = str(self.position.x)+","+str(self.position.y)
        data = {"name":self.name,"char":self.char_number,"position":position,"destination":self.get_destination()}
        return data

    def serialize(self):
        return {'name': self.name, 'char': self.char_number, 'position': self.get_position()}


class KeyBoardControll:

    def verify_events(self):
        request_event = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = False
            if event.type == pygame.MOUSEBUTTONUP:
                new_position = pygame.mouse.get_pos()
                self.player.move_to(new_position)

        request_event = {'player':self.player.name, 'command':'move', 'data':{'position':self.player.get_position(),'destination': self.player.get_destination()}}#'event':{'name':'move','position':new_position}}
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


class Manager():
    game = None

    def __init__(self, game):
        self.game = game

    def create_player(self,player_name, character_number, position=None):
        player = Character(player_name,character_number,position)
        game.elements[player_name] = player
        return player

    def create_object(self, object):
        self.game.objects.append(object)

    def create_ground_tile(self,x,y,w,h):
        ground = Ground(x,y,w,h)
        return self.create_object(ground)

    def create_simple_tree(self,x,y,w,h):
        tree = Birch(x,y,w,h)
        return self.create_object(tree)

    def draw_elements(self):
        for item in self.game.elements:
            self.game.elements[item].update(self.game.screen)
            #item.update(self.game.screen)

    def draw_objects(self):
        for item in self.game.objects:
            image = item.image
            imagerect = item.image.get_rect()
            self.game.screen.blit(image,(item.position.x,item.position.y), imagerect)

"""
class ClientGame(threading.Thread, socket.socket):
    def __init__(self, port=9000):
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        threading.Thread.__init__(self, name='ClientHandler')
        self.settimeout(2)
        self.bind(('localhost', port))
        self.setDaemon(True)

    def send_client_command(self, data):
        # self.sendto(pongserver.server.PongServer.COMMAND_CLIENT_CONNECT.encode('utf-8'), self.server_address)
        if data is None:
            print('Unable to send client command: None!')
            return
        self.sendto(data, (self.server_address,9000))
        return



class ServerGame(threading.Thread, socket.socket):
    def __init__(self, port=9000):
        threading.Thread.__init__(self, name='Server thread')
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        self.port = port
        self.bind(('', self.port))

        self.clients = []
        self.player_addresses = dict()
        self._current_player_to_assign = 1
        self.client_handlers = []

"""


class ClientGame:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conect()

    def get_data_from_server(self, log=True):
        response = self.client_game.recv(4096).decode()
        response = json.loads(response)
        if log:
            print("server:",response)
        return response

    def send_data_to_server(self, request, log=True):
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

class Game(ClientGame, KeyBoardControll):
    BUFFER_SIZE = 4096
    server_address = "127.0.0.1"
    server_port = "9000"
    data_game = {}

    elements = {}
    objects  = []
    size = [800,600]
    fps = 10

    player = None

    def __init__(self):
        self.setup()
        self.manager = Manager(self)
        self.create_map()

    def create_map(self):
        tree1 = Birch(200,290,90,160)
        tree2 = Pine(400, 290, 90, 160)

        #while do chão
        y = 0
        while y < 600:
            x = 0
            while x < 800:
                self.manager.create_ground_tile(x,y,50,50)
                x += 50
            y = y + 50

        #print('>>>',tree1.position.x)
        #print('>>>',tree2.position.x)
        self.objects.append(tree1)
        self.objects.append(tree2)
        #self.manager.create_simple_tree(200,290,90,160)
        #self.manager.create_simple_tree(400, 290, 90, 160)

    def setup(self):
        ClientGame.__init__(self, self.server_address,self.server_port)
        print('Hosting at:', self.client_game.getsockname())
        print('Starting Client.')
        pygame.init()
        pygame.display.set_caption("Survive!")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)

    def verify_data_server(self, log=True):
        self.send_data_to_server({"command": "verify_server"},log=log)
        return self.get_data_from_server(log=log)

    def create_player(self, player_name, char_number):
        player = self.manager.create_player(player_name, char_number)
        self.send_data_to_server({"command": "create_player", "player": player.get_data()})
        self.data_game = self.get_data_from_server()
        return player

    def start(self, player_name, char_number):
        self.data_game = self.verify_data_server()
        self.player = self.create_player(player_name, char_number)
        self.done = True

        while self.done:

            """
                ENVIAR E RECEBER OS DADOS DO EVENTO DE ANDAR E DEPOIS TER UM COMANDO PRA PEGAR
                AS ATUALIZACOES PRECISARIA USAR UM REQUEST SO.. POIS ASSIM DIMINUIMOS O NUMERO
                DE ACESSO AO SERVIDOR.. MAS POR ENQUANTO VAI TER QUE FICAR ASSIM..
                
                EM VEZ DE RETORNAR SOMENTE A RESPOSTA DO EVENTO QUE GERAMOS, PRECISAMOS
                TRAZER OS EVENTOS TODOS QUE FORAM RECEBIDOS LA.
            """
            request_events = self.verify_events()
            if request_events['data']['destination'] != None:
                self.send_data_to_server(request_events, log=False)
                response_events = self.get_data_from_server()

            self.data_game = self.verify_data_server(log=False)
            #response_events = self.get_data_from_server()

            if len(self.elements) != len(self.data_game['players']):
                for item in self.data_game['players']:
                    if item not in self.elements:
                        if type(self.data_game['players'][item]['position']) == str:
                            position_parts = self.data_game['players'][item]['position'].split(',')
                        else:
                            position_parts = self.data_game['players'][item]['position']

                        if type(self.data_game['players'][item]['destination']) == str:
                            destination_parts = self.data_game['players'][item]['destination'].split(',')
                        else:
                            destination_parts = self.data_game['players'][item]['destination']

                        x = int(position_parts[0])
                        y = int(position_parts[1])
                        position = Coordinate(x, y)
                        new_player = self.manager.create_player(self.data_game['players'][item]['name'], self.data_game['players'][item]['char'], position)

                        if destination_parts is not None:
                            dx = int(destination_parts[0])
                            dy = int(destination_parts[1])
                            new_player.destination = Coordinate(dx, dy)






            self.screen.fill(WHITE)
            self.manager.draw_objects()
            self.manager.draw_elements()

            #for item in self.elements:
            #    self.data_game[item.name] = item.get_data()

            #self.data_game['command']= 'update'
            #self.send_data_to_server(self.data_game)
            #response = self.get_data_from_server()

            #if response
            """
            if response["events"]=="create_player" and response["status"]=="accept":
                print("server:",response['events_values']['name'],"enter in game..")
                new_player = response['events_values']['name']
                position_part = response['events_values']['position'].split(",")
                position = Coordinate(int(position_part[0]),int(position_part[1]))
                new_player = self.manager.create_player(new_player, int(response['player']['char']),position)
                self.data_game[new_player.name]=new_player.get_data()

            self.screen.fill(WHITE)
            self.manager.draw_objects()
            if response["command"]=="event" and response["status"]=="accept":
                #print("client: Request was accepted")
                self.manager.draw_elements()
            else:
                #print("client: Request not accepted")
                #self.data_game = backup_data
                self.manager.draw_elements()
            """
            pygame.display.flip()
            self.clock.tick(self.fps)

        self.send_data_to_server({"command": "exit", "player": self.player.get_data()})
        self.close()
        pygame.quit()

if __name__=="__main__":
    import sys
    player_name = sys.argv[1]
    player_char = sys.argv[2]

    game = Game()
    game.start(player_name, player_char)