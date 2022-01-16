import random
import pygame
import sys
pygame.init()

class Fish:
    def __init__(self, _width):
        super(Fish, self).__init__()
        self._width = random.uniform(_width*0.55, _width*1.33)
        self._height = self._width * 0.5
        self._fish = pygame.image.load("game_assets/fish_images/fish1_left.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._choice = random.choice((0, 1))
        self._fish_rect = self._fish.get_rect(topleft=(self._choice*1220, random.uniform(50, 550)))
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
        super(Obstacles, self).__init__()
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
        self._acceleration = 0.5
        self._boost_duration = 7000

    def control_main_fish(self, type, boosted=1, freeze=1):
        if type == "l" and abs(self._vel_x - self._acceleration) < (500 / self.get_width()):
            self._vel_x -= self._acceleration*boosted*freeze
        if type == "r" and (self._vel_x + self._acceleration) < (500 / self.get_width()):
            self._vel_x += self._acceleration*boosted*freeze
        if type == "d" and (self._vel_y + self._acceleration) < (500 / self.get_width()):
            self._vel_y += self._acceleration*boosted*freeze
        if type == "u" and abs(self._vel_y - self._acceleration) < (500 / self.get_width()):
            self._vel_y -= self._acceleration*boosted*freeze

    def corner_vertical(self):
        self._vel_y = 0

    def corner_horizontal(self):
        self._vel_x = 0

    def increase_size(self):
        self._fish_rect.width *= 1.05
        self._fish_rect.height = self._fish_rect.width * 0.5
        self._fish = pygame.transform.scale(pygame.image.load("game_assets/fish_images/fish2_left.png"), (self._fish_rect.width, self._fish_rect.height))

    def update_acceleration(self):
        self._acceleration = max(0.05, 300 / (self.get_height() * self.get_width()))

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

class OtherFish(Fish):
    def __init__(self, _width):
        super(OtherFish, self).__init__(_width)

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
                self._main_fish.control_main_fish("l", boosted=2.5, freeze=freeze)
            if key_input[pygame.K_UP]:
                self._main_fish.control_main_fish("u", boosted=2.5, freeze=freeze)
            if key_input[pygame.K_RIGHT]:
                self._main_fish.control_main_fish("r", boosted=2.5, freeze=freeze)
            if key_input[pygame.K_DOWN]:
                self._main_fish.control_main_fish("d", boosted=2.5, freeze=freeze)
        else:
            if key_input[pygame.K_LEFT]:
                self._main_fish.control_main_fish("l")
            if key_input[pygame.K_UP]:
                self._main_fish.control_main_fish("u")
            if key_input[pygame.K_RIGHT]:
                self._main_fish.control_main_fish("r")
            if key_input[pygame.K_DOWN]:
                self._main_fish.control_main_fish("d")



class Game:
    def __init__(self):
        self._width = 1300
        self._height = 590
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._background = pygame.image.load("game_assets/background/background.jpg").convert()
        self._background = pygame.transform.scale(self._background, (self._width, self._height))
        self._other_fish = []
        self._score = 0
        self._font_score = pygame.font.SysFont("monospace", 25)
        self._font_game_over = pygame.font.SysFont("monospace", 70)
        self._font_restart = pygame.font.SysFont("monospace", 40)
        self._clock = pygame.time.Clock()
        self._game_time = 0
        self._main_menu = True
        self._game_is_on = True
        self._jelly_is_on = False
        self._octopus_is_on = False
        self._speed_booster_is_on = False
        self._size_booster_is_on = False
        self._speed_boosted = False
        self._size_boosted = False
        self._speed_boosted_duration = 0
        self._size_boosted_duration = 0
        self._speed_booster_time = random.uniform(20000, 40000)
        self._size_booster_time = random.uniform(20000, 40000)
        self._speed_booster_timer = 0
        self._size_booster_timer = 0
        self._freeze_timer = 0
        self._freeze = 1
        self._start = True
        self._rod_timer = 0
        self._net_timer = 0
        self._rod_is_on = False
        self._net_is_on = False
        self._rod_time = random.uniform(20000, 40000)
        self._net_time = random.uniform(20000, 40000)
        self._size_booster = None
        self._speed_booster = None
        self._jelly_fish = None
        self._octopus = None
        self._net = None
        self._rod = None

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
        self._game_is_on = False
        self._main_menu = False
        self._game_time = 0
        self._jelly_is_on = False
        self._octopus_is_on = False
        self._speed_booster_is_on = False
        self._size_booster_is_on = False
        self._speed_boosted = False
        self._size_boosted = False
        self._speed_boosted_duration = 0
        self._size_boosted_duration = 0
        self._speed_booster_time = random.uniform(20000, 40000)
        self._size_booster_time = random.uniform(20000, 40000)
        self._speed_booster_timer = 0
        self._size_booster_timer = 0
        self._freeze_timer = 0
        self._freeze = 1
        self._rod_timer = 0
        self._net_timer = 0
        self._rod_is_on = False
        self._net_is_on = False
        self._rod_time = random.uniform(20000, 40000)
        self._net_time = random.uniform(20000, 40000)
        self._score = 0
        for fish in self._other_fish:
            del fish
        self._other_fish = []
        if self._speed_booster_is_on: del self._speed_booster
        if self._size_booster_is_on: del self._size_booster
        if self._jelly_is_on:
            self._jelly_is_on = False
            del self._jelly_fish
        if self._octopus_is_on:
            self._octopus_is_on = False
            del self._octopus
        if self._net_is_on:
            del self._net
            self._net_is_on = False
        if self._rod_is_on:
            del self._rod
            self._rod_is_on = False
        self._size_booster = None
        self._speed_booster = None
        self._jelly_fish = None
        self._octopus = None
        self._net = None
        self._rod = None

    def update_timers(self, time):
        self._game_time += time
        self._speed_booster_timer += time
        self._size_booster_timer += time
        self._rod_timer += time
        self._net_timer += time
        if self._freeze == 0: self._freeze_timer += time
        if self._speed_boosted: self._speed_boosted_duration += time
        if self._size_boosted: self._size_boosted_duration += time

    def main_menu(self, mouse, click=False):
        if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 140 <= mouse[1] <= 230:
            pygame.draw.rect(self._screen, (144, 238, 144), [self._width / 3 + 15, 140, 300, 90],
                             border_radius=20)
        else:
            pygame.draw.rect(self._screen, (127, 255, 0), [self._width / 3 + 15, 140, 300, 90],
                             border_radius=20)
        if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 255 <= mouse[1] <= 345:
            pygame.draw.rect(self._screen, (255, 255, 102), [self._width / 3 + 15, 255, 300, 90],
                             border_radius=20)
        else:
            pygame.draw.rect(self._screen, (255, 255, 0), [self._width / 3 + 15, 255, 300, 90], border_radius=20)
        if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 370 <= mouse[1] <= 460:
            pygame.draw.rect(self._screen, (255, 127, 127), [self._width / 3 + 15, 370, 300, 90], border_radius=20)
        else:
            pygame.draw.rect(self._screen, (255, 0, 0), [self._width / 3 + 15, 370, 300, 90], border_radius=20)
        self._screen.blit(self._font_restart.render("EASY", True, (0, 0, 0)), (self._width / 3 + 111, 168))
        self._screen.blit(self._font_restart.render("MEDIUM", True, (0, 0, 0)),
                          (self._width / 3 + 100, 283))
        self._screen.blit(self._font_restart.render("HARD", True, (0, 0, 0)),
                          (self._width / 3 + 111, 398))
        if click:
            if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 140 <= mouse[1] <= 230:
                self._main_menu = False
            elif self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 255 <= mouse[1] <= 345:
                self._main_menu = False
            elif self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 370 <= mouse[1] <= 460:
                self._main_menu = False

    def run_game(self):
        while True:
            # initialize the game by calling the start_game function if the game is not over
            self.start_game(self._start)
            # set the start parameter to False since the game has already started
            self._start = False
            # set up the screen and background
            self._screen.fill("White")
            self._screen.blit(self._background, (0, 0))
            # check if the player clicked quit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            if self._main_menu:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                self.main_menu(mouse, click=click[0])

            # check if the game is live, continue if so
            elif self._game_is_on:
                # score_text is our live score that we display on the screen
                score_text = self._font_score.render("SCORE : " + str(self._score), True, (255, 255, 255))
                self._screen.blit(score_text, (1100, 50))
                # measure the time elapsed
                time = self._clock.get_time()
                self.update_timers(time)

                if self._freeze_timer >= 3000:
                    self._freeze_timer = 0
                    self._freeze = 1
                if self._speed_boosted_duration >= self._main_fish.get_boost_duration():
                    self._speed_boosted = False
                    self._speed_boosted_duration = 0
                if self._size_boosted_duration >= self._main_fish.get_boost_duration():
                    self._main_fish.reboost_size()
                    self._size_boosted = False
                    self._size_boosted_duration = 0

                # add boosters
                if self._speed_booster_timer >= self._speed_booster_time and self._speed_booster_is_on == False:
                    self._speed_booster_timer = 0
                    # add the booster on the screen on a random place
                    # we check in case it collides with our main fish
                    # if so we don't initialize the booster and continue on random assignment
                    while True:
                        self._speed_booster = SpeedBooster()

                        if self._main_fish.get_rect().colliderect(self._speed_booster.get_rect()):
                            del self._speed_booster
                            continue
                        self._speed_booster_is_on = True
                        break

                if self._size_booster_timer >= self._size_booster_time and self._size_booster_is_on == False:
                    self._size_booster_timer = 0
                    # add the booster on the screen on a random place
                    # we check in case it collides with our main fish
                    # if so we don't initialize the booster and continue on random assignment
                    while True:
                        self._size_booster = SizeBooster()

                        if self._main_fish.get_rect().colliderect(self._size_booster.get_rect()):
                            del self._size_booster
                            self._size_booster = None
                            continue
                        self._size_booster_is_on = True
                        break

                if self._speed_booster_is_on:
                    if self._speed_booster_timer >= self._speed_booster.get_duration():
                        self._speed_booster_is_on = False
                        self._speed_booster_timer = 0
                        del self._speed_booster
                        self._speed_booster = None

                if self._size_booster_is_on:
                    if self._size_booster_timer >= self._size_booster.get_duration():
                        self._size_booster_is_on = False
                        self._size_booster_timer = 0
                        del self._size_booster
                        self._size_booster = None

                if self._score == 10 and self._jelly_is_on == False:
                    # add the jelly fish on the screen
                    # it will be added from either top of the bottom of the screen
                    # it's location on the x axis is assigned randomly therefore
                    # we check in case it collides with our main fish
                    # if so we don't initialize the jellyfish and continue on random assignment
                    while True:
                        self._jelly_fish = JellyFish()

                        if self._main_fish.get_rect().colliderect(self._jelly_fish.get_rect()):
                            del self._jelly_fish
                            self._jelly_fish = None
                            continue
                        # when the jelly fish is created, the parameter "sea_animal_is_on" becomes True
                        self._jelly_is_on = True
                        break
                if self._score == 15 and self._octopus_is_on == False:
                    # add the jelly fish on the screen
                    # it will be added from either top of the bottom of the screen
                    # it's location on the x axis is assigned randomly therefore
                    # we check in case it collides with our main fish
                    # if so we don't initialize the jellyfish and continue on random assignment
                    while True:
                        self._octopus = Octapus()

                        if self._main_fish.get_rect().colliderect(self._octopus.get_rect()):
                            del self._octopus
                            self._octopus = None
                            continue
                        # when the jelly fish is created, the parameter "sea_animal_is_on" becomes True
                        self._octopus_is_on = True
                        break
                # we add a fish to the game every 4 seconds
                if self._game_time >= 4000:
                    self._game_time = 0
                    while True:
                        fish = OtherFish(self._main_fish.get_width())
                        # we again check if it collides with our fish
                        if self._main_fish.get_rect().colliderect(fish.get_rect()):
                            del fish
                            continue
                        self._other_fish.append(OtherFish(self._main_fish.get_width()))
                        break
                    # we update the velocities of all fish every 4 seconds
                    # they change both direction and speed
                    for fish in self._other_fish:
                        fish.update_velocity()
                # our constant fps
                self._clock.tick(30)
                # taking the user input below
                # user controls the main fish
                key_input = pygame.key.get_pressed()
                UserInput(key_input, self._main_fish, self._speed_boosted, freeze=self._freeze)

                # we check if the our fish reaches the top or bottom of the screen
                # we update the velocity related
                if self._main_fish.get_rect().top + self._main_fish.get_vertical_velocity() < 0 or self._main_fish.get_rect().bottom + self._main_fish.get_vertical_velocity() > self._height:
                    self._main_fish.corner_vertical()

                # we check if the our fish reaches the leftmost or rightmost of the screen
                # we update the velocity related
                if self._main_fish.get_rect().left + self._main_fish.get_horizontal_velocity() < 0 or self._main_fish.get_rect().right + self._main_fish.get_horizontal_velocity() > self._width:
                    self._main_fish.corner_horizontal()

                # if jelly is on the screen we check if it's on the edges of the screen
                # if so we update the velocity
                if self._jelly_is_on:
                    if self._jelly_fish.get_rect().top + self._jelly_fish.get_vertical_velocity() < 0 or self._jelly_fish.get_rect().bottom + self._jelly_fish.get_vertical_velocity() > self._height:
                        self._jelly_fish.corner_vertical()

                    if self._jelly_fish.get_rect().left + self._jelly_fish.get_horizontal_velocity() < 0 or self._jelly_fish.get_rect().right + self._jelly_fish.get_horizontal_velocity() > self._width:
                        self._jelly_fish.corner_horizontal()

                    # we check if jellyfish collides with our main fish
                    # if so, our fish dies and we update the parameters accordingly
                    if self._main_fish.get_rect().colliderect(self._jelly_fish.get_rect()):
                        self._freeze = 0

                if self._octopus_is_on:
                    if self._octopus.get_rect().top + self._octopus.get_vertical_velocity() < 0 or self._octopus.get_rect().bottom + self._octopus.get_vertical_velocity() > self._height:
                        self._octopus.corner_vertical()

                    if self._octopus.get_rect().left + self._octopus.get_horizontal_velocity() < 0 or self._octopus.get_rect().right + self._octopus.get_horizontal_velocity() > self._width:
                        self._octopus.corner_horizontal()

                    # we check if jellyfish collides with our main fish
                    # if so, our fish dies and we update the parameters accordingly
                    if self._main_fish.get_rect().colliderect(self._octopus.get_rect()):
                        self.finish_game()

                if self._speed_booster_is_on:
                    if self._main_fish.get_rect().colliderect(self._speed_booster.get_rect()):
                        self._speed_boosted = True
                        self._speed_booster_is_on = False
                        del self._speed_booster
                        self._speed_booster = None
                        self._speed_booster_timer = 0

                if self._size_booster_is_on:
                    if self._main_fish.get_rect().colliderect(self._size_booster.get_rect()):
                        self._main_fish.boost_size()
                        self._size_boosted = True
                        self._size_booster_is_on = False
                        del self._size_booster
                        self._size_booster = None
                        self._size_booster_timer = 0

                # the list of fish that we eat, they will be removed from the game at the end of the while loop
                remove_list = []
                # other fish and main fish movements
                for fish in self._other_fish:
                    # we check if fish are on the edges of the screen
                    # if so we update the velocity
                    if fish.get_rect().top + fish.get_vertical_velocity() < 0 or fish.get_rect().bottom + fish.get_vertical_velocity() > self._height:
                        fish.corner_vertical()
                        fish.move()

                    if fish.get_rect().left + fish.get_horizontal_velocity() < 0 or fish.get_rect().right + fish.get_horizontal_velocity() > self._width:
                        fish.corner_horizontal()
                        fish.move()

                    # if the other fish collides with jellyfish, it changes direction
                    if self._jelly_is_on:
                        if fish.get_rect().colliderect(self._jelly_fish.get_rect()):
                            fish.change_direction()
                            fish.move()

                    # if the other fish collides with octopus, it changes direction
                    if self._octopus_is_on:
                        if fish.get_rect().colliderect(self._octopus.get_rect()):
                            fish.change_direction()
                            fish.move()

                    # if the other fish collides with fishing net, it changes direction
                    if self._net_is_on:
                        if fish.get_rect().colliderect(self._net.get_rect()):
                            fish.change_direction()
                            fish.move()

                    # if the other fish collides with fishing rod, it changes direction
                    if self._rod_is_on:
                        if fish.get_rect().colliderect(self._rod.get_rect()):
                            fish.change_direction()
                            fish.move()

                    # if the other fish collides with size booster, it changes direction
                    if self._size_booster_is_on:
                        if fish.get_rect().colliderect(self._size_booster.get_rect()):
                            fish.change_direction()
                            fish.move()

                    # if the other fish collides with speed booster, it changes direction
                    if self._speed_booster_is_on:
                        if fish.get_rect().colliderect(self._speed_booster.get_rect()):
                            fish.change_direction()
                            fish.move()

                    # we check if the main fish collides with an other fish
                    if self._main_fish.get_rect().colliderect(fish.get_rect()):
                        # if so, if the size of our fish is bigger, we eat the fish
                        # we increase the game score and the size of our fish increases accordingly
                        # main fish gets slower as its size increases
                        if (fish.get_width() * fish.get_height()) <= (self._main_fish.get_width() * self._main_fish.get_height()):
                            remove_list.append(fish)
                            self._score += 1
                            self._main_fish.increase_size()
                            self._main_fish.update_acceleration()
                        # otherwise our fish gets eaten and the game ends
                        # we update the parameters accordingly
                        else:
                            self.finish_game()
                    # if our fish doesn't collide, game continues as usual
                    else:
                        # move the fish
                        fish.move()
                        if fish.get_horizontal_velocity() > 0: self._screen.blit(pygame.transform.flip(fish.get_image(), True, False), fish.get_rect())
                        else: self._screen.blit(fish.get_image(), fish.get_rect())

                # remove the fish that are eaten by our fish from the game
                for fish in remove_list:
                    self._other_fish.remove(fish)
                    del fish
                # our fish gets slower if player doesn't move our fish
                self._main_fish.decelerate()
                # we draw our fish on the screen
                if not self._rod_is_on and self._rod_timer >= self._rod_time:
                    self._rod_timer = 0
                    self._rod_is_on = True
                    self._rod = FishingRod()
                    # rod.remove()
                if not self._net_is_on and self._net_timer >= self._net_time:
                    self._net_timer = 0
                    self._net_is_on = True
                    self._net = FishingNet()
                    # rod.remove()
                if self._main_fish.get_horizontal_velocity() <0: self._screen.blit(self._main_fish.get_image(), self._main_fish.get_rect())
                else: self._screen.blit(pygame.transform.flip(self._main_fish.get_image(), True, False), self._main_fish.get_rect())
                if self._rod_is_on:
                    self._rod.move(self._rod_timer)
                    if self._main_fish.get_rect().colliderect(self._rod.get_rect()):
                        self.finish_game()

                if self._net_is_on:
                    self._net.move(self._net_timer)
                    if self._main_fish.get_rect().colliderect(self._net.get_rect()):
                        self.finish_game()

                if self._net_is_on and self._net.get_rect().y < -90:
                    del self._net
                    self._net = None
                    self._net_is_on = False
                    self._net_timer = 0

                if self._rod_is_on and self._rod.get_rect().y < -200:
                    del self._rod
                    self._rod = None
                    self._rod_is_on = False
                    self._rod_timer = 0

                # we move our main fish
                self._main_fish.move(self._freeze)
                # we move our jellyfish if it is on the screen
                if self._jelly_is_on: self._jelly_fish.move()
                if self._octopus_is_on: self._octopus.move()

                if self._net_is_on: self._screen.blit(self._net.get_image(), self._net.get_rect())
                if self._rod_is_on: self._screen.blit(self._rod.get_image(), self._rod.get_rect())
                if self._jelly_is_on: self._screen.blit(self._jelly_fish.get_image(), self._jelly_fish.get_rect())
                if self._octopus_is_on: self._screen.blit(self._octopus.get_image(), self._octopus.get_rect())
                if self._speed_booster_is_on: self._screen.blit(self._speed_booster.get_image(), self._speed_booster.get_rect())
                if self._size_booster_is_on: self._screen.blit(self._size_booster.get_image(),
                                                          self._size_booster.get_rect())
            # if the game is over, we display a screen that says game is over
            else:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                key_input = pygame.key.get_pressed()
                text = self._font_game_over.render("GAME OVER", True, (255, 255, 255))
                self._screen.blit(text, (440, 120))
                if 475 <= mouse[0] <= 775 and 230 <= mouse[1] <= 320:
                    pygame.draw.rect(self._screen, (245, 163, 62), [475, 230, 300, 90],
                                     border_radius=20)
                else: pygame.draw.rect(self._screen, (235, 97, 35), [475, 230, 300, 90],
                                 border_radius=20)
                main_menu = self._font_restart.render("MAIN MENU", True, (0, 0, 0))
                self._screen.blit(main_menu, (511, 259))
                restart = self._font_restart.render("RESTART", True, (0, 0, 0))
                if 475 <= mouse[0] <= 775 and 350 <= mouse[1] <= 440: pygame.draw.rect(self._screen, (254, 217, 177), [475, 350, 300, 90],
                                 border_radius=20)
                else: pygame.draw.rect(self._screen, (245, 163, 62), [475, 350, 300, 90],
                                 border_radius=20)
                self._screen.blit(restart, (540, 375))
                if click[0]:
                    if 475 <= mouse[0] <= 775 and 230 <= mouse[1] <= 320:
                        self._main_menu = True
                        self._start = True
                        self._game_is_on = True
                    if 475 <= mouse[0] <= 775 and 350 <= mouse[1] <= 440:
                        self._start = True
                        self._game_is_on = True
                # if the player presses "R" we restart the game again
                if key_input[pygame.K_r]:
                    self._start = True
                    self._game_is_on = True
            # update the display
            pygame.display.flip()
            pygame.display.update()


game = Game()
game.run_game()
