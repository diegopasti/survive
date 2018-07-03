import json
import os
import socket
import threading

import pygame

from apps.core.utils import Coordinate
from survive import settings
from survive.settings import BASE_DIR

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
    width = None
    height = None
    position = Coordinate(0,0)

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


class Tree(Object):
    image_path = None
    image = None

    def __init__(self,x,y,w,h):
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.set_position(x,y)


class Pine(Tree):
    image_path = BASE_DIR+"/static/images/trees/_tree_13/_tree_13_70000.png"


class SimpleTree(Tree):
    image_path = BASE_DIR +"/static/images/trees/_tree_01/_tree_01_70000.png"


class Element(Object):
    image_number = None
    image_level = None
    file_image = None

    image = None

    sprite_number = 1
    direction = NORTH
    
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

    def __init__(self, char_number):
        self.image_path = os.path.join(settings.BASE_DIR, 'static/images/beta/chars/'+str(char_number)+'/')
        simple_directions_images = self.image_path+"basic.png"
        diagonal_directions_image = self.image_path+"diagonal.png"
        self.position = Coordinate(0, 0)
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
            variation_y = self.height / 6


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
            pass



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





class KeyBoardControll:

    def verify_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = False
            if event.type == pygame.MOUSEBUTTONUP:
                new_position = pygame.mouse.get_pos()
                self.player.move_to(new_position)

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



        """
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
        """


class Manager():
    game = None

    def __init__(self, game):
        self.game = game

    def create_object(self, object):
        self.game.objects.append(object)

    def create_simple_tree(self,x,y,w,h):
        tree = SimpleTree(x,y,w,h)
        return self.create_object(tree)

    def draw_elements(self):
        for item in self.game.elements:
            item.update(self.game.screen)

    def draw_objects(self):
        for item in self.game.objects:
            image = item.image
            imagerect = item.image.get_rect()
            self.game.screen.blit(image, imagerect)


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



class Game(ClientGame, ServerGame, KeyBoardControll):
    BUFFER_SIZE = 4096
    server_address = "127.0.0.1"
    game_type = "CLIENT"

    elements = []
    objects  = []
    size = [800,600]
    fps = 6

    player = None

    def __init__(self, type="CLIENT"):
        self.setup()
        self.manager = Manager(self)
        self.create_map()

    def create_map(self):
        #self.manager.create_simple_tree(200,290,90,160)
        pass

    def setup(self):
        if self.game_type == "CLIENT":
            ClientGame.__init__(self)
            print('Hosting at:', self.getsockname())
            print('Starting server.')
        else:
            ServerGame.__init__(self)
            print('Client:', self.getsockname())
            print('Start connection..')

        pygame.init()
        pygame.display.set_caption("Survive!")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)

    def start(self):
        self.player = Character(2)


        self.elements.append(self.player)
        self.done = True
        while self.done:
            self.verify_events()

            if self.game_type == "SERVER":
                print("AGUARDAR ALGUM EVENTO")
            else:
                data = b'position:200,100'
                #data = json.dumps(message)
                self.send_client_command(data)




            self.screen.fill(WHITE)
            self.manager.draw_objects()
            self.manager.draw_elements()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()



#server = Game(type="SERVER")
#server.start()
game = Game(type="CLIENT")
game.start()
