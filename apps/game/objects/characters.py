from apps.game.vars import SOUTH_WEST, NORTH_WEST, SOUTH_EAST, NORTH_EAST, WEST, SOUTH, EAST, NORTH, CHARACTERS_DIRS, BLACK
from apps.main.utils import Coordinate
from survive import settings
import random
import pygame
import os


class Object:
    image_path = None
    image = None

    width = None
    height = None
    position = None

    def __init__(self, x, y, w, h, image_path=None):
        if image_path is not None:
            self.image = pygame.image.load(image_path)
        else:
            self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.position = Coordinate(x, y)

    def get_position(self):
        return (self.position.x, self.position.y)

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def get_size(self):
        return (self.width, self.height)

    def set_size(self, width, heigth):
        self.width = width
        self.height = heigth


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
        self.width = self.image.get_width() / 4
        self.height = self.image.get_height() / 4

    def get_destination(self):
        if self.destination is not None:
            return (self.destination.x, self.destination.y)
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
            sprite = self.get_sprite(item + 1)
            self.sequences.append(sprite)

    def get_current_sprite(self):
        return self.sequences[self.current_sprite - 1]
        # return self.get_sprite(self.current_sprite)

    def get_sprite(self, sequence_number):
        origin = self.get_sprite_coordinate(sequence_number)
        sprite = pygame.Rect(origin, self.get_size())
        return sprite

    def get_sprite_coordinate(self, sprite_number):
        # print("NUMBER: ",sprite_number," -  WIDTH:",self.width," - HEIGHT:",self.height)
        coord_x = (sprite_number - 1) * self.width
        coord_y = (self.direction - 1) * self.height
        return (coord_x, coord_y)

    def get_size(self):
        return (self.width, self.height)


class Animations:
    current_direction = SOUTH
    current_animation = None
    current_image = None

    def __init__(self, simple_directions_image_path, walking_diagonal_directions_images_path):
        self.directions = {}
        self.simple_directions_image_path = simple_directions_image_path
        self.simple_directions_image = pygame.image.load(self.simple_directions_image_path)

        self.directions[SOUTH] = Sequence(self.simple_directions_image, 1, 8, 4)
        self.directions[WEST] = Sequence(self.simple_directions_image, 2, 8, 4)
        self.directions[NORTH] = Sequence(self.simple_directions_image, 4, 8, 4)
        self.directions[EAST] = Sequence(self.simple_directions_image, 3, 8, 4)

        self.walking_diagonal_directions_images_path = walking_diagonal_directions_images_path
        self.walking_diagonal_directions_images = pygame.image.load(self.walking_diagonal_directions_images_path)
        self.directions[SOUTH_WEST] = Sequence(self.walking_diagonal_directions_images, 1, 8, 4)
        self.directions[NORTH_WEST] = Sequence(self.walking_diagonal_directions_images, 2, 8, 4)
        self.directions[NORTH_EAST] = Sequence(self.walking_diagonal_directions_images, 4, 8, 4)
        self.directions[SOUTH_EAST] = Sequence(self.walking_diagonal_directions_images, 3, 8, 4)
        self.change_direction(SOUTH)

    def get_current_sprite(self):
        sprite = self.current_animation.get_current_sprite()
        # print("PEGAR DIRECAO:",self.current_direction," - CURRENT_SPRITE: ",sprite)
        return sprite  # get_sprite(self.directions[self.current_direction].current_sprite)

    def update(self):
        self.current_animation.update()

    def change_direction(self, direction):
        self.current_direction = direction
        if self.current_direction == 1 or self.current_direction == 3 or self.current_direction == 5 or self.current_direction == 7:
            self.current_image = self.simple_directions_image
        else:
            self.current_image = self.walking_diagonal_directions_images
        self.current_animation = self.directions[self.current_direction]
        # self.current_animation.reset_sequence()


class Monster(Element):
    pass


class Character(Element):
    animations = None
    current_animation = None

    direction = 1
    sprite_number = 1

    speed = 4
    running = False

    walking = None
    destination = None
    destination_distance = None
    is_player = None


    def __init__(self, player_name, char_number, position=None, is_player=False):
        self.name = player_name
        self.is_player = is_player
        self.char_number = char_number
        self.image_path = os.path.join(settings.BASE_DIR, 'static/images/chars/' + str(char_number) + '/')
        walking_simple_directions_images = self.image_path + "animation_walking_base.png"
        walking_diagonal_directions_images = self.image_path + "animation_walking_extra.png"
        running_simple_directions_images = self.image_path + "animation_running_base.png"
        running_diagonal_directions_images = self.image_path + "animation_running_extra.png"

        self.health = 100
        self.max_health = 100

        self.energy = 100
        self.max_energy = 100

        self.regen_energy = 0.5
        self.running_coust_energy = 0.5

        self.level = 1
        self.experience = 0

        if position is None:
            init_x = random.randint(50, 750)
            init_y = random.randint(50, 550)
            self.position = Coordinate(init_x, init_y)
        else:
            self.position = position
        self.animations = {}
        self.animations['walking'] = Animations(walking_simple_directions_images, walking_diagonal_directions_images)
        self.animations['running'] = Animations(running_simple_directions_images, running_diagonal_directions_images)
        self.current_animation = self.animations['walking']
        self.set_size(self.current_animation.current_image.get_width() / 8, self.current_animation.current_image.get_height() / 4)

    def move_to(self, position, show_router=False, running=False):
        self.destination = Coordinate(position[0], position[1])
        self.show_router = show_router
        self.running = running

    def get_center_image(self):
        x = self.position.x + self.width / 2
        y = self.position.y + self.height / 2
        return Coordinate(x, y)

    def update(self, screen):
        if self.destination is not None:
            self.origin = self.get_center_image()
            if self.show_router:
                pygame.draw.line(screen, BLACK, [self.origin.x, self.origin.y], [self.destination.x, self.destination.y], 1)
            self.destination_distance = self.origin.get_distance(self.destination)

            current_speed = self.speed
            if self.is_player:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    if self.energy > 0:
                        self.running = True
                        current_speed = self.speed*2
                        self.energy = self.energy - self.running_coust_energy
                        self.current_animation = self.animations['running']
                    else:
                        self.running = False
                        current_speed = self.speed
                        self.current_animation = self.animations['walking']

                else:
                    self.running = False
                    current_speed = self.speed
                    if self.energy < self.max_energy:
                        self.energy = self.energy + self.regen_energy
                    self.current_animation = self.animations['walking']
            else:
                if self.running:
                    current_speed = self.speed * 2
                    #self.energy = self.energy - self.running_coust_energy
                    self.current_animation = self.animations['running']
                else:
                    current_speed = self.speed
                    self.current_animation = self.animations['walking']

            self.destination_time = self.destination_distance / current_speed
            variation_x = self.width / 6
            variation_y = self.height / 6

            if self.destination_distance < 2:
                self.stop()

                # elif self.origin.x < self.destination.x:
            elif self.destination.x > self.origin.x + variation_x:
                # print("VAMOS PRA DIREITA..",end="")
                if self.destination.y > self.origin.y + variation_y:
                    # print("E VAMOS DESCER")
                    self.walk(SOUTH_EAST)
                elif self.destination.y < self.origin.y - variation_y:
                    # print("E VAMOS SUBIR")
                    self.walk(NORTH_EAST)
                else:
                    # print("RETO. DEVE ESTAR ENTRE 3/6 e 4/6")
                    self.walk(EAST)

            elif self.destination.x < self.origin.x - variation_x:
                # print("VAMOS PRA ESQUERDA..", end="")
                if self.destination.y > self.origin.y + variation_y:
                    # print("E VAMOS DESCER")
                    self.walk(SOUTH_WEST)
                elif self.destination.y < self.origin.y - variation_y:
                    # print("E VAMOS SUBIR")
                    self.walk(NORTH_WEST)
                else:
                    # print("RETO")
                    self.walk(WEST)
            else:
                # print("VOU RETO..", end="")
                if self.destination.y > self.origin.y + variation_y:
                    # print("PRA BAIXO")
                    self.walk(SOUTH)
                elif self.destination.y < self.origin.y - variation_y:
                    # print("PRA CIMA")
                    self.walk(NORTH)
                else:
                    # print("FICAR PARADO")
                    self.destination = None
                    self.stop()
            self.current_animation.update()
        else:
            if self.energy < self.max_energy:
                self.energy = self.energy + self.regen_energy
            self.origin = self.get_center_image()
        screen.blit(self.current_animation.current_image, self.get_position(), self.current_animation.get_current_sprite())

    def walk(self, direction):
        self.walking = direction
        variacao_x = (self.destination.x - self.origin.x) / self.destination_time
        variacao_y = (self.destination.y - self.origin.y) / self.destination_time

        if variacao_x < 0:
            variacao_x = variacao_x * -1
        if variacao_y < 0:
            variacao_y = variacao_y * -1

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

    def stop(self):
        self.walking = None
        self.destination = None
        self.running = False
        self.current_animation = self.animations['walking']
        self.current_animation.change_direction(SOUTH)

    def get_data(self):
        position = str(self.position.x) + "," + str(self.position.y)
        data = {"name": self.name, "char": self.char_number, "position": position, "destination": self.get_destination(),"running":self.running,"health":self.health,"max_health":self.max_health,
                "energy": self.energy, "max_energy": self.max_energy
                }
        return data

    def serialize(self):
        return {'name': self.name, 'char': self.char_number, 'position': self.get_position(), "destination": self.get_destination(),"running":self.running}

