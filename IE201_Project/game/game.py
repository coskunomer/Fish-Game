import random
import pygame
import sys
import time


class Fish:
    def __init__(self):
        pass


class SeaAnimals:
    def __init__(self):
        pass


class Obstacles:
    def __init__(self):
        pass


class Booster:
    def __init__(self):
        pass


class MainFish():
    def __init__(self):
        # super(MainFish, self).__init__()
        self._width = 80
        self._height = 48
        self._main_fish = pygame.image.load("game_assets/fish_images/main_fish.png")
        self._main_fish = pygame.transform.scale(self._main_fish, (self._width, self._height))
        self._main_fish_rect = self._main_fish.get_rect()
        self._vel_x = 0
        self._vel_y = 0
        self._acceleration = 1

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_image(self):
        return self._main_fish

    def get_rect(self):
        return self._main_fish_rect

    def get_vertical_velocity(self):
        return self._vel_y

    def get_horizontal_velocity(self):
        return self._vel_x

    def control_main_fish(self, type):
        if type == "l":
            self._vel_x -= self._acceleration
        if type == "r":
            self._vel_x += self._acceleration
        if type == "d":
            self._vel_y += self._acceleration
        if type == "u":
            self._vel_y -= self._acceleration

    def move_main_fish(self):
        self._main_fish_rect.x += self._vel_x
        self._main_fish_rect.y += self._vel_y

    def corner_vertical(self):
        self._vel_y = 0

    def corner_horizontal(self):
        self._vel_x = 0

class OtherFish():
    def __init__(self):
        # super(OtherFish, self).__init__()
        self._width = 60
        self._height = 36
        self._other_fish = pygame.image.load("game_assets/fish_images/other_fish.png")
        self._other_fish = pygame.transform.scale(self._other_fish, (self._width, self._height))
        self._other_fish_rect = self._other_fish.get_rect()
        self._vel_x = 5
        self._vel_y = 3

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_image(self):
        return self._other_fish

    def get_rect(self):
        return self._other_fish_rect

    def get_vertical_velocity(self):
        return self._vel_y

    def get_horizontal_velocity(self):
        return self._vel_x

    def update_velocity(self):
        self._vel_x = random.uniform(-3, 4)
        self._vel_y = random.uniform(-1, 3)

    def move_fish(self):
        self._other_fish_rect.x += self._vel_x
        self._other_fish_rect.y += self._vel_y

    def corner_vertical(self):
        self._vel_y = 0

    def corner_horizontal(self):
        self._vel_x = 0


class JellyFish(SeaAnimals):
    def __init__(self):
        super(JellyFish, self).__init__()
        pass


class Octapus(SeaAnimals):
    def __init__(self):
        super(Octapus, self).__init__()
        pass


class FishingNet(Obstacles):
    def __init__(self):
        super(FishingNet, self).__init__()
        pass


class FishingRod(Obstacles):
    def __init__(self):
        super(FishingRod, self).__init__()
        pass


class SpeedBooster(Booster):
    def __init__(self):
        super(SpeedBooster, self).__init__()
        pass


class SizeBooster(Booster):
    def __init__(self):
        super(SizeBooster, self).__init__()
        pass


class UserInput:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        self._width = 1300
        self._height = 590
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._background = pygame.image.load("game_assets/background/background.jpg").convert()
        self._background = pygame.transform.scale(self._background, (self._width, self._height))
        self._main_fish = MainFish()
        self._other_fish = []
        for i in range(5):
            self._other_fish.append(OtherFish())
        # self._other_fish = OtherFish()
        # self._jellyfish = JellyFish()
        # self._octopus = Octapus()
        # self._fishing_net = FishingNet()
        # self._fishing_rod = FishingRod()
        # self._speed_booster = SpeedBooster()
        # self._size_booster = SizeBooster()
        # self._user_input = UserInput()

    def run_game(self):
        clock = pygame.time.Clock()
        game_time = 0
        while True:
            self._screen.fill("White")
            self._screen.blit(self._background, (0, 0))
            print(clock.get_time())
            game_time += clock.get_time()
            if game_time >= 3000:
                game_time = 0
                for fish in self._other_fish:
                    fish.update_velocity()
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                key_input = pygame.key.get_pressed()
                if key_input[pygame.K_LEFT]:
                    self._main_fish.control_main_fish("l")
                if key_input[pygame.K_UP]:
                    self._main_fish.control_main_fish("u")
                if key_input[pygame.K_RIGHT]:
                    self._main_fish.control_main_fish("r")
                if key_input[pygame.K_DOWN]:
                    self._main_fish.control_main_fish("d")

            if self._main_fish.get_rect().top + self._main_fish.get_vertical_velocity() < 0 or self._main_fish.get_rect().bottom + self._main_fish.get_vertical_velocity() > self._height:
                self._main_fish.corner_vertical()

            if self._main_fish.get_rect().left + self._main_fish.get_horizontal_velocity() < 0 or self._main_fish.get_rect().right + self._main_fish.get_horizontal_velocity() > self._width:
                self._main_fish.corner_horizontal()

            self._main_fish.move_main_fish()
            for fish in self._other_fish:
                if fish.get_rect().top + fish.get_vertical_velocity() < 0 or fish.get_rect().bottom + fish.get_vertical_velocity() > self._height:
                    fish.corner_vertical()

                if fish.get_rect().left + fish.get_horizontal_velocity() < 0 or fish.get_rect().right + fish.get_horizontal_velocity() > self._width:
                    fish.corner_horizontal()
                fish.move_fish()
                self._screen.blit(fish.get_image(), fish.get_rect())

            self._screen.blit(self._main_fish.get_image(), self._main_fish.get_rect())
            pygame.display.flip()
            pygame.display.update()


game = Game()
game.run_game()
