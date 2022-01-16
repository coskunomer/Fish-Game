import random
import pygame
pygame.init()

class Fish:
    def __init__(self, _width):
        self._width = random.uniform(_width*0.55, _width*1.33)
        self._height = self._width * 0.5
        self._fish = pygame.image.load("game_assets/fish_images/fish1_left.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._choice = random.choice((0, 1))
        self._fish_rect = self._fish.get_rect(topleft=(100 + self._choice*1000, random.uniform(50, 550)))
        if self._choice == 0: self._vel_x = 4
        else: self._vel_x = -4
        self._vel_y = random.uniform(-3, 3)

    def get_width(self):
        return self._fish_rect.width

    def get_height(self):
        return self._fish_rect.height

    def get_image(self):
        return self._fish

    def get_rect(self):
        return self._fish_rect

    def get_vertical_velocity(self):
        return self._vel_y

    def get_horizontal_velocity(self):
        return self._vel_x

    def move(self, freeze=1):
        self._fish_rect.x += self._vel_x * freeze
        self._fish_rect.y += self._vel_y * freeze

    def corner_vertical(self):
        self._vel_y = -self._vel_y

    def corner_horizontal(self):
        self._vel_x = -self._vel_x

    def change_direction(self):
        self._vel_x = -self._vel_x
        self._vel_y = -self._vel_y

class Obstacles:
    def __init__(self):
        self._width = 20
        self._height = 200
        self._duration = random.uniform(20000, 40000)
        self._obstacle = pygame.image.load("game_assets/obstacles/fishing_rod/anchor.png")
        self._obstacle = pygame.transform.scale(self._obstacle, (self._width, self._height))
        self._obstacle_rect = self._obstacle.get_rect(topleft=(random.uniform(30, 650), -200))

    def get_width(self):
        return self._obstacle_rect.width

    def get_height(self):
        return self._obstacle_rect.height

    def get_image(self):
        return self._obstacle

    def get_rect(self):
        return self._obstacle_rect

    def get_duration(self):
        return self._duration

    def move(self, timer):
        if timer > self.get_duration():
            self._obstacle_rect.y -= 1
        else:
            if self.get_rect().y < 0:
                self.get_rect().y += 0.3


class MainFish(Fish):
    def __init__(self):
        super(MainFish, self).__init__(_width=40)
        self._width = 40
        self._height = self._width*0.5
        self._fish = pygame.image.load("game_assets/fish_images/fish2_left.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(center=(650, 300))
        self._fish_right = pygame.image.load("game_assets/fish_images/fish2_right.png")
        self._fish_right = pygame.transform.scale(self._fish_right, (self._width, self._height))
        self._fish_right_rect = self._fish_right.get_rect(center=(650, 300))
        self._vel_x = 0
        self._vel_y = 0
        self._acceleration = 10
        self._boost_duration = 7000

    def control_main_fish(self, type, boosted=1, freeze=1):
        if type == "l":
            self._vel_x = -self._acceleration*boosted*freeze
        if type == "r":
            self._vel_x = self._acceleration*boosted*freeze
        if type == "d":
            self._vel_y = self._acceleration*boosted*freeze
        if type == "u":
            self._vel_y = -self._acceleration*boosted*freeze

    def corner_vertical(self):
        self._vel_y = 0

    def corner_horizontal(self):
        self._vel_x = 0

    def increase_size(self):
        if self._fish_rect.width > 100:
            pass
        self._fish_rect.width *= 1.05
        self._fish_rect.height = self._fish_rect.width * 0.5
        self._fish = pygame.transform.scale(pygame.image.load("game_assets/fish_images/fish2_left.png"), (self._fish_rect.width, self._fish_rect.height))

    def update_acceleration(self):
        self._acceleration = max(3, 282 / (self.get_height() * self.get_width())**0.5)

    def decelerate(self):
        pass

    def boost_size(self):
        self._fish_rect.width += 10
        self._fish_rect.height = self._fish_rect.width * 2 / 3
        self._fish = pygame.transform.scale(pygame.image.load("game_assets/fish_images/fish2_left.png"), (self._fish_rect.width, self._fish_rect.height))

    def reboost_size(self):
        self._fish_rect.width -= 10
        self._fish_rect.height = self._fish_rect.width * 2 / 3
        self._fish = pygame.transform.scale(pygame.image.load("game_assets/fish_images/fish2_left.png"), (self._fish_rect.width, self._fish_rect.height))

    def get_boost_duration(self):
        return self._boost_duration

    def zero_velocity(self):
        self._vel_y = 0
        self._vel_x = 0

class OtherFish(Fish):
    def __init__(self, _width, _difficulty):
        super(OtherFish, self).__init__(_width)
        self._difficulty = _difficulty
        self._width = random.uniform(_width * 0.55 + _width*self._difficulty*0.05, _width * 1.33 + _width*self._difficulty*0.05)
        self._height = self._width * 0.5
        self._fish = pygame.image.load("game_assets/fish_images/fish1_left.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._choice = random.choice((0, 1))
        self._fish_rect = self._fish.get_rect(topleft=(100 + self._choice*1000, random.uniform(50, 550)))

    def update_velocity(self):
        self._vel_x = random.uniform(-5, 5)
        self._vel_y = random.uniform(-3, 3)

class JellyFish(Fish):
    def __init__(self):
        super(JellyFish, self).__init__(_width=40)
        self._width = 40
        self._height = 80
        self._fish = pygame.image.load("game_assets/jellyfish/jellyfish.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(topleft=(random.uniform(100, 1200), random.choice([1, 509])))
        self._vel_x = 0
        self._vel_y = random.uniform(3, 8)

class Octapus(Fish):
    def __init__(self):
        super(Octapus, self).__init__(_width=40)
        self._width = 60
        self._height = 60
        self._fish = pygame.image.load("game_assets/octopus/octopus.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(topleft=(random.uniform(100, 1200), random.choice([1, 509])))
        self._vel_x = 0
        self._vel_y = random.uniform(3, 8)


class FishingNet(Obstacles):
    def __init__(self):
        super(FishingNet, self).__init__()
        self._width = 300
        self._height = 90
        self._obstacle = pygame.image.load("game_assets/obstacles/fishing_net/fishing_net.png")
        self._obstacle = pygame.transform.scale(self._obstacle, (self._width, self._height))
        self._obstacle_rect = self._obstacle.get_rect(topleft=(random.uniform(650, 1000), -90))

class FishingRod(Obstacles):
    def __init__(self):
        super(FishingRod, self).__init__()

class SpeedBooster(pygame.sprite.Sprite):
    def __init__(self):
        super(SpeedBooster, self).__init__()
        self._width = 40
        self._height = 40
        self._duration = random.uniform(5000, 10000)
        self._image = pygame.image.load("game_assets/boosters/speed_booster.png")
        self._image = pygame.transform.scale(self._image, (self._width, self._height))
        self._image_rect = self._image.get_rect(topleft=(random.uniform(100, 1200), random.uniform(200, 540)))

    def get_width(self):
        return self._image_rect.width

    def get_height(self):
        return self._image_rect.height

    def get_image(self):
        return self._image

    def get_rect(self):
        return self._image_rect

    def get_duration(self):
        return self._duration


class SizeBooster(SpeedBooster):
    def __init__(self):
        super(SizeBooster, self).__init__()
        self._image = pygame.image.load("game_assets/boosters/size_booster.png")
        self._image = pygame.transform.scale(self._image, (self._width, self._height))
        self._image_rect = self._image.get_rect(topleft=(random.uniform(100, 1200), random.uniform(200, 540)))

class UserInput:
    def __init__(self, key_input, main_fish=None, speed_boosted=0, freeze=1):
        self._key_input = key_input
        self._main_fish = main_fish
        if speed_boosted:
            if key_input[pygame.K_LEFT]:
                self._main_fish.control_main_fish("l", boosted=2, freeze=freeze)
            if key_input[pygame.K_UP]:
                self._main_fish.control_main_fish("u", boosted=2, freeze=freeze)
            if key_input[pygame.K_RIGHT]:
                self._main_fish.control_main_fish("r", boosted=2, freeze=freeze)
            if key_input[pygame.K_DOWN]:
                self._main_fish.control_main_fish("d", boosted=2, freeze=freeze)
        else:
            if key_input[pygame.K_LEFT]:
                self._main_fish.control_main_fish("l")
            if key_input[pygame.K_UP]:
                self._main_fish.control_main_fish("u")
            if key_input[pygame.K_RIGHT]:
                self._main_fish.control_main_fish("r")
            if key_input[pygame.K_DOWN]:
                self._main_fish.control_main_fish("d")


