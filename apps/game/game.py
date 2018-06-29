import os
import pygame
from survive import settings
from survive.settings import BASE_DIR

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define directions
LEFT = 2
UP = 4
RIGHT = 3
DOWN = 1

# Define other variables
CHARACTERS_DIRS = os.path.join(settings.BASE_DIR, 'static/images/chars/')


class Coordinate:

    x = 0
    y = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y

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
    direction = UP
    
    def update(self):
        pass

    def load_image(self, image_number, image_level=1):
        self.image_number = image_number
        self.image_level = image_level
        self.image_path = CHARACTERS_DIRS + str(self.image_number) + "/" + str(self.image_level) + ".png"

        self.image = pygame.image.load(self.image_path)
        self.width = self.image.get_width()/4
        self.height = self.image.get_height()/4
    
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


class Sprites():

    walking = []
    running = []


class Character(Element):

    direction = 1
    sprite_number = 1

    speed = 5

    walking = None
    destination = None

    def __init__(self):
        self.position = Coordinate(0, 0)
        self.image_path = os.path.join(settings.BASE_DIR, 'static/images/chars/')
        self.load_image(1, 3)

    #def load_image(self,hero_image, hero_level):
    #    self.hero_image_number = hero_image
    #    self.hero_level_number = hero_level
    #    self.file_image = self.image_path+str(self.hero_image_number)+"/"+str(self.hero_level_number)+".png"
    #    #self.image = pygame.image.load(self.file_image)

    def update(self, screen):
        screen.blit(self.image, self.get_position(), self.change_sprite())

        if self.walking is not None:
            self.walk(self.walking)

    def walk(self, direction):
        self.walking = direction
        self.direction = direction
        if direction == UP:
            self.position.y = self.position.y - self.speed
        elif direction == RIGHT:
            self.position.x = self.position.x + self.speed
        elif direction == DOWN:
            self.position.y = self.position.y + self.speed
        else:
            self.position.x = self.position.x - self.speed
        self.change_sprite_number()

    def stop(self):
        self.direction = DOWN
        self.walking = None


class KeyBoardControll:

    def verify_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = False

            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so
                # adjust speed.
                if event.key == pygame.K_LEFT:
                    self.player.walk(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.player.walk(RIGHT)
                elif event.key == pygame.K_UP:
                    self.player.walk(UP)
                elif event.key == pygame.K_DOWN:
                    self.player.walk(DOWN)
                else:
                    pass

            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.walk(LEFT)
                elif keys[pygame.K_UP]:
                    self.player.walk(UP)
                elif keys[pygame.K_RIGHT]:
                    self.player.walk(RIGHT)
                elif keys[pygame.K_DOWN]:
                    self.player.walk(DOWN)
                else:
                    self.player.stop()

                #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # if event.type == pygame.MOUSEBUTTONUP:
                #    pos = pygame.mouse.get_pos()
                #    self.player.move_to(pos[0],pos[1])


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


class Game(KeyBoardControll):
    elements = []
    objects  = []
    size = [800,600]
    fps = 8

    player = None

    def __init__(self):
        self.setup()
        self.manager = Manager(self)
        self.create_map()


    def create_map(self):
        self.manager.create_simple_tree(200,290,160,90)

    def setup(self):
        pygame.init()
        pygame.display.set_caption("Survive!")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)

    def start(self):
        self.player = Character()
        self.elements.append(self.player)
        self.done = True
        while self.done:
            self.verify_events()
            self.screen.fill(WHITE)
            self.manager.draw_objects()
            self.manager.draw_elements()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()



Game().start()
