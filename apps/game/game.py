from apps.game.controllers.controllers import KeyBoardControll, ClientGame
from apps.game.objects.characters import Character, Object
from apps.game.objects.trees import Birch, Pine
from apps.game.objects.tiles import Ground
from apps.main.utils import Coordinate
from apps.game.vars import WHITE
import pygame
import json

from survive.settings import BASE_DIR
from apps.game.objects.characters import Object


class Panel(Object):
    image_path = BASE_DIR + "/static/images/panel.png"
    objects = []

    def __init__(self):
        Object.__init__(self,122,580,956,120)
        self.empty_health = Object(284, 583, 96, 96, BASE_DIR + "/static/images/empty.png")
        self.empty_energy = Object(818, 585, 96, 96, BASE_DIR + "/static/images/empty.png")

        self.health = Object(284, 583, 96, 96, BASE_DIR + "/static/images/health.png")
        self.energy = Object(818, 585, 96, 96, BASE_DIR + "/static/images/mana.png")

        self.objects.append(self.empty_health)
        self.objects.append(self.empty_energy)


    def update(self, game):
        for item in self.objects:
            image = item.image
            rect = item.image.get_rect()
            game.screen.blit(image, (item.position.x, item.position.y), rect)

        percent_health = round(game.player.health/game.player.max_health,2)
        rect = pygame.Rect(0, (self.health.height-(percent_health*self.health.height)), self.health.width, self.health.height)
        game.screen.blit(self.health.image,(self.health.position.x,self.health.position.y+((1-percent_health)*self.health.height)),rect)

        percent_energy = round(game.player.energy / game.player.max_energy, 2)
        rect = pygame.Rect(0, (self.energy.height - (percent_energy * self.energy.height)), self.energy.width, self.energy.height)
        game.screen.blit(self.energy.image, (self.energy.position.x, self.energy.position.y + ((1 - percent_energy) * self.energy.height)), rect)

        rect = self.image.get_rect()
        game.screen.blit(self.image, (self.position.x, self.position.y), rect)


class Manager:
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

    def create_birch_tree(self,x,y,w,h):
        tree = Birch(x,y,w,h)
        return self.create_object(tree)
    
    def create_pine_tree(self,x,y,w,h):
        tree = Pine(x,y,w,h)
        return self.create_object(tree)

    def draw_elements(self):
        for item in self.game.elements:
            self.game.elements[item].update(self.game.screen)

    def draw_objects(self):
        for item in self.game.objects:
            image = item.image
            imagerect = item.image.get_rect()
            self.game.screen.blit(image,(item.position.x,item.position.y), imagerect)

    def draw_controls(self):
        self.game.panel.update(self.game)
        #rect = self.game.panel.image.get_rect()
        #self.game.screen.blit(self.game.panel.image, (self.game.panel.position.x, self.game.panel.position.y), rect)
        #image = item.image
        #imagerect = item.image.get_rect()
        #self.game.screen.blit(image, (item.position.x, item.position.y), imagerect)



class Game(ClientGame, KeyBoardControll):
    BUFFER_SIZE = 4096
    server_address = None
    server_port = "9000"
    data_game = {}

    elements = {}
    objects  = []
    size = [1200,700]
    fps = 8

    player = None

    def __init__(self,server):
        self.server_address = server
        self.setup()
        self.manager = Manager(self)
        self.create_map()
        self.create_panel()

    def create_map(self):
        file_map = open('maps/main.json','r').read()
        map = json.loads(file_map)
        tile_size = map['tile_size']
        cont_row = 0
        for registros in map['objects']:
            cont_col = 0
            for item in registros:
                if item == "G":
                    self.manager.create_ground_tile(cont_col*tile_size, cont_row * tile_size, 100, 100)
                elif item == "P":
                    self.manager.create_ground_tile(cont_col*tile_size, cont_row * tile_size, 100, 100)
                    self.manager.create_pine_tree(cont_col*tile_size, cont_row*tile_size, 90, 160)
                elif item == "B":
                    self.manager.create_ground_tile(cont_col*tile_size, cont_row * tile_size, 100, 100)
                    self.manager.create_birch_tree(cont_col*tile_size, cont_row*tile_size, 90, 160)
                cont_col = cont_col + 1
            cont_row = cont_row + 1

    def create_panel(self):
        self.panel = Panel()
        #empty_health = Object(184,483,96,96,BASE_DIR+"/static/images/empty.png")
        #empty_energy = Object(718, 485, 96, 96, BASE_DIR + "/static/images/empty.png")

        #health = Object(184, 483, 96, 96, BASE_DIR + "/static/images/health.png")
        #energy = Object(718, 485, 96, 96, BASE_DIR + "/static/images/mana.png")
        #self.objects.append(empty_health)
        #self.objects.append(health)

        #self.objects.append(empty_energy)
        #self.objects.append(energy)
        #self.objects.append(panel)

    def setup(self):
        ClientGame.__init__(self, self.server_address,self.server_port)
        print('Hosting at:', self.client_game.getsockname())
        print('Starting Client.')
        pygame.init()
        pygame.display.set_caption("Survive!")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)

    def verify_data_server(self, request=None, log=False):
        if request is not None:
            self.send_data_to_server(request, log=log)
        else:
            self.send_data_to_server({"command": "verify_server"},log=False)
        return self.get_data_from_server(log=log)

    def create_player(self, player_name, char_number):
        player = self.manager.create_player(player_name, char_number)
        self.send_data_to_server({"command": "create_player", "player": player.get_data()})
        self.data_game = self.get_data_from_server()
        return player

    def verify_new_players(self):
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

    def update_server_changes(self):
        self.verify_new_players()
        for char in self.data_game['players']:
            if char != self.player.name:
                if self.data_game['players'][char]['destination'] is not None:
                    destination = (float(self.data_game['players'][char]['destination'][0]),float(self.data_game['players'][char]['destination'][1]))
                    running = self.data_game['players'][char]['running']
                    self.elements[char].move_to(destination,running=running)
                else:
                    self.elements[char].stop()

    def start(self, player_name, char_number):
        self.data_game = self.verify_data_server()
        self.player = self.create_player(player_name, char_number)
        self.player.is_player = True
        self.done = True

        while self.done:
            request_events = self.verify_events()
            self.data_game = self.verify_data_server(request=request_events,log=False)

            self.update_server_changes()
            self.screen.fill(WHITE)
            self.manager.draw_objects()
            self.manager.draw_controls()
            self.manager.draw_elements()
            pygame.display.flip()
            self.clock.tick(self.fps)
        self.send_data_to_server({"command": "exit", "player": self.player.get_data()})
        self.close()
        pygame.quit()

if __name__=="__main__":
    import sys
    player_name = sys.argv[1]
    player_char = sys.argv[2]
    server = sys.argv[3]

    game = Game(server)
    game.start(player_name, player_char)