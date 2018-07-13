from apps.game.controllers.controllers import KeyBoardControll, ClientGame
from apps.game.objects.characters import Character
from apps.game.objects.trees import Birch, Pine
from apps.game.objects.tiles import Ground
from apps.main.utils import Coordinate
from apps.game.vars import WHITE
import pygame


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

    def create_simple_tree(self,x,y,w,h):
        tree = Birch(x,y,w,h)
        return self.create_object(tree)

    def draw_elements(self):
        for item in self.game.elements:
            self.game.elements[item].update(self.game.screen)

    def draw_objects(self):
        for item in self.game.objects:
            image = item.image
            imagerect = item.image.get_rect()
            self.game.screen.blit(image,(item.position.x,item.position.y), imagerect)


class Game(ClientGame, KeyBoardControll):
    BUFFER_SIZE = 4096
    server_address = None
    server_port = "9000"
    data_game = {}

    elements = {}
    objects  = []
    size = [800,600]
    fps = 8

    player = None

    def __init__(self,server):
        self.server_address = server
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