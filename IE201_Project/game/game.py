import random
import pygame
import sys
import time
pygame.init()

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


class MainFish:
    def __init__(self):
        # super(MainFish, self).__init__()
        self._width = 30
        self._height = 20
        self._main_fish = pygame.image.load("game_assets/fish_images/main_fish.png")
        self._main_fish = pygame.transform.scale(self._main_fish, (self._width, self._height))
        self._main_fish_rect = self._main_fish.get_rect(center=(650, 300))
        self._vel_x = 0
        self._vel_y = 0
        self._acceleration = 0.5

    def get_width(self):
        return self._main_fish_rect.width

    def get_height(self):
        return self._main_fish_rect.height

    def get_image(self):
        return self._main_fish

    def get_rect(self):
        return self._main_fish_rect

    def get_vertical_velocity(self):
        return self._vel_y

    def get_horizontal_velocity(self):
        return self._vel_x

    def control_main_fish(self, type):
        if type == "l" and abs(self._vel_x - self._acceleration) < (500 / self.get_width()):
            self._vel_x -= self._acceleration
        if type == "r" and (self._vel_x + self._acceleration) < (500 / self.get_width()):
            self._vel_x += self._acceleration
        if type == "d" and (self._vel_y + self._acceleration) < (500 / self.get_width()):
            self._vel_y += self._acceleration
        if type == "u" and abs(self._vel_y - self._acceleration) < (500 / self.get_width()):
            self._vel_y -= self._acceleration

    def move_main_fish(self):
        self._main_fish_rect.x += self._vel_x
        self._main_fish_rect.y += self._vel_y

    def corner_vertical(self):
        self._vel_y = 0

    def corner_horizontal(self):
        self._vel_x = 0

    def increase_size(self):
        self._main_fish_rect.width *= 1.05
        self._main_fish_rect.height = self._main_fish_rect.width*0.7
        self._main_fish = pygame.transform.scale(self._main_fish, (self._main_fish_rect.width, self._main_fish_rect.height))

    def update_acceleration(self):
        self._acceleration = 300 / (self.get_height() * self.get_width())

    def update_velocity(self):
        pass

class OtherFish:
    def __init__(self, _width):
        # super(OtherFish, self).__init__()
        self._width = random.uniform(_width*0.5, _width*1.3)
        self._height = self._width*0.75
        self._other_fish = pygame.image.load("game_assets/fish_images/other_fish.png")
        self._other_fish = pygame.transform.scale(self._other_fish, (self._width, self._height))
        self._other_fish_rect = self._other_fish.get_rect(topleft=(random.uniform(50, 1250), random.uniform(50, 550)))
        self._vel_x = random.uniform(-5, 5)
        self._vel_y = random.uniform(-3, 3)

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
        self._vel_x = random.uniform(-5, 5)
        self._vel_y = random.uniform(-3, 3)

    def move_fish(self):
        self._other_fish_rect.x += self._vel_x
        self._other_fish_rect.y += self._vel_y

    def corner_vertical(self):
        self._vel_y = -self._vel_y

    def corner_horizontal(self):
        self._vel_x = -self._vel_x

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
        self._score = 0
        self._font_score = pygame.font.SysFont("monospace", 25)
        self._font_game_over = pygame.font.SysFont("monospace", 70)
        self._font_restart = pygame.font.SysFont("monospace", 40)
        self._game_is_on = True

        # self._other_fish = OtherFish()
        # self._jellyfish = JellyFish()
        # self._octopus = Octapus()
        # self._fishing_net = FishingNet()
        # self._fishing_rod = FishingRod()
        # self._speed_booster = SpeedBooster()
        # self._size_booster = SizeBooster()
        # self._user_input = UserInput()

    def start_game(self, start):
        if start == False: return 0
        self._main_fish = MainFish()
        for i in range(5):
            while True:
                fish = OtherFish(self._main_fish.get_width())
                if self._main_fish.get_rect().colliderect(fish.get_rect()):
                    del fish
                    continue
                self._other_fish.append(OtherFish(self._main_fish.get_width()))
                break

    def finish_game(self):
        for fish in self._other_fish:
            del fish
        self._other_fish = []
        self._score = 0

    def run_game(self):
        clock = pygame.time.Clock()
        game_time = 0
        start = True
        while True:
            self.start_game(start)
            start = False
            self._screen.fill("White")
            self._screen.blit(self._background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            if self._game_is_on:
                scoretext = self._font_score.render("SCORE : " + str(self._score), True, (255, 255, 255))
                self._screen.blit(scoretext, (1100, 50))
                game_time += clock.get_time()
                if game_time >= 4000:
                    game_time = 0
                    while True:
                        fish = OtherFish(self._main_fish.get_width())
                        if self._main_fish.get_rect().colliderect(fish.get_rect()):
                            del fish
                            continue
                        self._other_fish.append(OtherFish(self._main_fish.get_width()))
                        break
                    for fish in self._other_fish:
                        fish.update_velocity()
                clock.tick(100)
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
                remove_list = []
                for fish in self._other_fish:
                    if fish.get_rect().top + fish.get_vertical_velocity() < 0 or fish.get_rect().bottom + fish.get_vertical_velocity() > self._height:
                        fish.corner_vertical()

                    if fish.get_rect().left + fish.get_horizontal_velocity() < 0 or fish.get_rect().right + fish.get_horizontal_velocity() > self._width:
                        fish.corner_horizontal()

                    if self._main_fish.get_rect().colliderect(fish.get_rect()):
                        if (fish.get_width() * fish.get_height()) <= self._main_fish.get_width() * self._main_fish.get_height():
                            remove_list.append(fish)
                            self._score += 1
                            self._main_fish.increase_size()
                            self._main_fish.update_acceleration()
                        else:
                            self._game_is_on = False
                            self.finish_game()
                    else:
                        fish.move_fish()
                        if self._main_fish.get_rect().colliderect(fish.get_rect()):
                            if (fish.get_width()*fish.get_height()) <= self._main_fish.get_width()*self._main_fish.get_height():
                                remove_list.append(fish)
                                self._score += 1
                                self._main_fish.increase_size()
                                self._main_fish.update_acceleration()
                            else:
                                self._game_is_on = False
                                self.finish_game()
                        else:
                            self._screen.blit(fish.get_image(), fish.get_rect())

                for fish in remove_list:
                    self._other_fish.remove(fish)
                    del fish
                self._main_fish.update_velocity()
                self._screen.blit(self._main_fish.get_image(), self._main_fish.get_rect())
            else:
                text = self._font_game_over.render("GAME IS OVER", True, (255, 255, 255))
                self._screen.blit(text, (420, 200))
                restart = self._font_restart.render("PRESS R TO RESTART", True, (255, 255, 255))
                self._screen.blit(restart, (460, 300))
                key_input = pygame.key.get_pressed()
                if key_input[pygame.K_r]:
                    start = True
                    self._game_is_on = True
            pygame.display.flip()
            pygame.display.update()


game = Game()
game.run_game()