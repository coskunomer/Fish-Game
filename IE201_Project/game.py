import random
import pygame
import sys
pygame.init()

class Fish:
    def __init__(self, _width):
        self._width = random.uniform(_width*0.5, _width*1.25)
        self._height = self._width * 0.75
        self._fish = pygame.image.load("game_assets/fish_images/other_fish.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(topleft=(random.uniform(50, 1250), random.uniform(50, 550)))
        self._vel_x = random.uniform(-5, 5)
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

    def move(self):
        self._fish_rect.x += self._vel_x
        self._fish_rect.y += self._vel_y

    def corner_vertical(self):
        self._vel_y = -self._vel_y

    def corner_horizontal(self):
        self._vel_x = -self._vel_x

class Obstacles:
    def __init__(self):
        pass

class MainFish(Fish):
    def __init__(self):
        super(MainFish, self).__init__(_width=30)
        self._width = 30
        self._height = self._width*2/3
        self._fish = pygame.image.load("game_assets/fish_images/main_fish.png")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(center=(650, 300))
        self._vel_x = 0
        self._vel_y = 0
        self._acceleration = 0.5
        self._boost_duration = 7000

    def control_main_fish(self, type, boosted=1):
        if type == "l" and abs(self._vel_x - self._acceleration) < (500 / self.get_width()):
            self._vel_x -= self._acceleration*boosted
        if type == "r" and (self._vel_x + self._acceleration) < (500 / self.get_width()):
            self._vel_x += self._acceleration*boosted
        if type == "d" and (self._vel_y + self._acceleration) < (500 / self.get_width()):
            self._vel_y += self._acceleration*boosted
        if type == "u" and abs(self._vel_y - self._acceleration) < (500 / self.get_width()):
            self._vel_y -= self._acceleration*boosted

    def corner_vertical(self):
        self._vel_y = 0

    def corner_horizontal(self):
        self._vel_x = 0

    def increase_size(self):
        self._fish_rect.width *= 1.05
        self._fish_rect.height = self._fish_rect.width*2/3
        self._fish = pygame.transform.scale(self._fish, (self._fish_rect.width, self._fish_rect.height))

    def update_acceleration(self):
        self._acceleration = max(0.05, 300 / (self.get_height() * self.get_width()))

    def decelerate(self):
        pass

    def boost_size(self):
        self._fish_rect.width += 10
        self._fish_rect.height = self._fish_rect.width * 2 / 3
        self._fish = pygame.transform.scale(self._fish, (self._fish_rect.width, self._fish_rect.height))

    def reboost_size(self):
        self._fish_rect.width -= 10
        self._fish_rect.height = self._fish_rect.width * 2 / 3
        self._fish = pygame.transform.scale(self._fish, (self._fish_rect.width, self._fish_rect.height))

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
        self._fish = pygame.image.load("game_assets/jellyfish/jellyfish.jpg")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(topleft=(random.uniform(100, 1200), random.choice([1, 509])))
        self._vel_x = 0
        self._vel_y = random.uniform(3, 8)

class Octapus(Fish):
    def __init__(self):
        super(Octapus, self).__init__(_width=40)
        self._width = 60
        self._height = 60
        self._fish = pygame.image.load("game_assets/octopus/octopus.jpg")
        self._fish = pygame.transform.scale(self._fish, (self._width, self._height))
        self._fish_rect = self._fish.get_rect(topleft=(random.uniform(100, 1200), random.choice([1, 509])))
        self._vel_x = 0
        self._vel_y = random.uniform(3, 8)


class FishingNet(Obstacles):
    def __init__(self):
        super(FishingNet, self).__init__()
        pass


class FishingRod(Obstacles):
    def __init__(self):
        super(FishingRod, self).__init__()
        pass


class SpeedBooster():
    def __init__(self):
        #super(SpeedBooster, self).__init__()
        self._width = 40
        self._height = 40
        self._duration = random.uniform(5000, 10000)
        self._image = pygame.image.load("game_assets/boosters/speed_booster.png")
        self._image = pygame.transform.scale(self._image, (self._width, self._height))
        self._image_rect = self._image.get_rect(topleft=(random.uniform(100, 1200), random.uniform(50, 540)))

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
        self._image_rect = self._image.get_rect(topleft=(random.uniform(100, 1200), random.uniform(50, 540)))

class UserInput:
    def __init__(self, key_input, main_fish, speed_boosted):
        self._key_input = key_input
        self._main_fish = main_fish
        if speed_boosted:
            if key_input[pygame.K_LEFT]:
                self._main_fish.control_main_fish("l", boosted=4)
            if key_input[pygame.K_UP]:
                self._main_fish.control_main_fish("u", boosted=4)
            if key_input[pygame.K_RIGHT]:
                self._main_fish.control_main_fish("r", boosted=4)
            if key_input[pygame.K_DOWN]:
                self._main_fish.control_main_fish("d", boosted=4)
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
        self._main_fish = MainFish()
        self._other_fish = []
        self._score = 0
        self._font_score = pygame.font.SysFont("monospace", 25)
        self._font_game_over = pygame.font.SysFont("monospace", 70)
        self._font_restart = pygame.font.SysFont("monospace", 40)

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
        game_is_on = True
        jelly_is_on = False
        octopus_is_on = False
        speed_booster_is_on = False
        size_booster_is_on = False
        speed_boosted = False
        size_boosted = False
        speed_boosted_duration = 0
        size_boosted_duration = 0
        speed_booster_time = random.uniform(20000, 40000)
        size_booster_time = random.uniform(20000, 40000)
        speed_booster_timer = 0
        size_booster_timer = 0
        start = True
        while True:
            # initialize the game by calling the start_game function if the game is not over
            self.start_game(start)
            # set the start parameter to False since the game has already started
            start = False
            # set up the screen and background
            self._screen.fill("White")
            self._screen.blit(self._background, (0, 0))
            # check if the player clicked quit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            # check if the game is live, continue if so
            if game_is_on:
                # scoretext is our live score that we display on the screen
                scoretext = self._font_score.render("SCORE : " + str(self._score), True, (255, 255, 255))
                self._screen.blit(scoretext, (1100, 50))
                # measure the time elapsed
                game_time += clock.get_time()
                speed_booster_timer += clock.get_time()
                size_booster_timer += clock.get_time()
                if speed_boosted: speed_boosted_duration += clock.get_time()
                if size_boosted: size_boosted_duration += clock.get_time()
                if speed_boosted_duration >= self._main_fish.get_boost_duration():
                    speed_boosted = False
                    speed_boosted_duration = 0
                if size_boosted_duration >= self._main_fish.get_boost_duration():
                    self._main_fish.reboost_size()
                    size_boosted = False
                    size_boosted_duration = 0

                # add boosters
                if speed_booster_timer >= speed_booster_time and speed_booster_is_on == False:
                    speed_booster_timer = 0
                    # add the booster on the screen on a random place
                    # we check in case it collides with our main fish
                    # if so we don't initialize the booster and continue on random assignment
                    while True:
                        self._speed_booster = SpeedBooster()

                        if self._main_fish.get_rect().colliderect(self._speed_booster.get_rect()):
                            del self._speed_booster
                            continue
                        speed_booster_is_on = True
                        break

                if size_booster_timer >= size_booster_time and size_booster_is_on == False:
                    size_booster_timer = 0
                    # add the booster on the screen on a random place
                    # we check in case it collides with our main fish
                    # if so we don't initialize the booster and continue on random assignment
                    while True:
                        self._size_booster = SizeBooster()

                        if self._main_fish.get_rect().colliderect(self._size_booster.get_rect()):
                            del self._size_booster
                            continue
                        size_booster_is_on = True
                        break

                if speed_booster_is_on:
                    if speed_booster_timer >= self._speed_booster.get_duration():
                        speed_booster_is_on = False
                        speed_booster_timer = 0
                        del self._speed_booster

                if size_booster_is_on:
                    if size_booster_timer >= self._size_booster.get_duration():
                        size_booster_is_on = False
                        size_booster_timer = 0
                        del self._size_booster

                if self._score == 10 and jelly_is_on == False:
                    # add the jelly fish on the screen
                    # it will be added from either top of the bottom of the screen
                    # it's location on the x axis is assigned randomly therefore
                    # we check in case it collides with our main fish
                    # if so we don't initialize the jellyfish and continue on random assignment
                    while True:
                        self._jelly_fish = JellyFish()

                        if self._main_fish.get_rect().colliderect(self._jelly_fish.get_rect()):
                            del self._jelly_fish
                            continue
                        # when the jelly fish is created, the parameter "sea_animal_is_on" becomes True
                        jelly_is_on = True
                        break
                if self._score == 15 and octopus_is_on == False:
                    # add the jelly fish on the screen
                    # it will be added from either top of the bottom of the screen
                    # it's location on the x axis is assigned randomly therefore
                    # we check in case it collides with our main fish
                    # if so we don't initialize the jellyfish and continue on random assignment
                    while True:
                        self._octopus = Octapus()

                        if self._main_fish.get_rect().colliderect(self._octopus.get_rect()):
                            del self._octopus
                            continue
                        # when the jelly fish is created, the parameter "sea_animal_is_on" becomes True
                        octopus_is_on = True
                        break
                # we add a fish to the game every 4 seconds
                if game_time >= 4000:
                    game_time = 0
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
                clock.tick(40)
                # taking the user input below
                # user controls the main fish
                key_input = pygame.key.get_pressed()
                UserInput(key_input, self._main_fish, speed_boosted)

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
                if jelly_is_on:
                    if self._jelly_fish.get_rect().top + self._jelly_fish.get_vertical_velocity() < 0 or self._jelly_fish.get_rect().bottom + self._jelly_fish.get_vertical_velocity() > self._height:
                        self._jelly_fish.corner_vertical()

                    if self._jelly_fish.get_rect().left + self._jelly_fish.get_horizontal_velocity() < 0 or self._jelly_fish.get_rect().right + self._jelly_fish.get_horizontal_velocity() > self._width:
                        self._jelly_fish.corner_horizontal()

                    # we check if jellyfish collides with our main fish
                    # if so, our fish dies and we update the parameters accordingly
                    if self._main_fish.get_rect().colliderect(self._jelly_fish.get_rect()):
                        game_is_on = False
                        del self._jelly_fish
                        if speed_booster_is_on: del self._speed_booster
                        if size_booster_is_on: del self._size_booster
                        size_booster_timer = 0
                        speed_booster_timer = 0
                        speed_booster_is_on = False
                        size_booster_is_on = False
                        jelly_is_on = False
                        if octopus_is_on:
                            octopus_is_on = False
                            del self._octopus
                        self.finish_game()
                if octopus_is_on:
                    if self._octopus.get_rect().top + self._octopus.get_vertical_velocity() < 0 or self._octopus.get_rect().bottom + self._octopus.get_vertical_velocity() > self._height:
                        self._octopus.corner_vertical()

                    if self._octopus.get_rect().left + self._octopus.get_horizontal_velocity() < 0 or self._octopus.get_rect().right + self._octopus.get_horizontal_velocity() > self._width:
                        self._octopus.corner_horizontal()

                    # we check if jellyfish collides with our main fish
                    # if so, our fish dies and we update the parameters accordingly
                    if self._main_fish.get_rect().colliderect(self._octopus.get_rect()):
                        game_is_on = False
                        octopus_is_on = False
                        jelly_is_on = False
                        del self._jelly_fish
                        del self._octopus
                        if speed_booster_is_on: del self._speed_booster
                        if size_booster_is_on: del self._size_booster
                        size_booster_timer = 0
                        speed_booster_timer = 0
                        speed_booster_is_on = False
                        size_booster_is_on = False
                        self.finish_game()

                if speed_booster_is_on:
                    if self._main_fish.get_rect().colliderect(self._speed_booster.get_rect()):
                        speed_boosted = True
                        speed_booster_is_on = False
                        del self._speed_booster
                        speed_booster_timer = 0

                if size_booster_is_on:
                    if self._main_fish.get_rect().colliderect(self._size_booster.get_rect()):
                        self._main_fish.boost_size()
                        size_boosted = True
                        size_booster_is_on = False
                        del self._size_booster
                        size_booster_timer = 0



                # we move our main fish
                self._main_fish.move()
                # we move our jellyfish if it is on the screen
                if jelly_is_on: self._jelly_fish.move()
                if octopus_is_on: self._octopus.move()
                # the list of fish that we eat, they will be removed mfrom the game at the end of the while loop
                remove_list = []
                # other fish and main fish movements
                for fish in self._other_fish:
                    # we check if fish are on the edges of the screen
                    # if so we update the velocity
                    if fish.get_rect().top + fish.get_vertical_velocity() < 0 or fish.get_rect().bottom + fish.get_vertical_velocity() > self._height:
                        fish.corner_vertical()

                    if fish.get_rect().left + fish.get_horizontal_velocity() < 0 or fish.get_rect().right + fish.get_horizontal_velocity() > self._width:
                        fish.corner_horizontal()

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
                            if speed_booster_is_on: del self._speed_booster
                            if size_booster_is_on: del self._size_booster
                            size_booster_timer = 0
                            speed_booster_timer = 0
                            speed_booster_is_on = False
                            size_booster_is_on = False
                            if jelly_is_on:
                                jelly_is_on = False
                                del self._jelly_fish
                            if octopus_is_on:
                                octopus_is_on = False
                                del self._octopus

                            obstacle_time = 0
                            game_is_on = False
                            self.finish_game()
                    # if our fish doesn't collide, game continues as usual
                    else:
                        # move the fish
                        fish.move()
                        # check again if they collide
                        # functions are the same as above
                        if self._main_fish.get_rect().colliderect(fish.get_rect()):
                            if (fish.get_width()*fish.get_height()) <= self._main_fish.get_width()*self._main_fish.get_height():
                                remove_list.append(fish)
                                self._score += 1
                                self._main_fish.increase_size()
                                self._main_fish.update_acceleration()
                            else:
                                if speed_booster_is_on: del self._speed_booster
                                if size_booster_is_on: del self._size_booster
                                size_booster_timer = 0
                                speed_booster_timer = 0
                                speed_booster_is_on = False
                                size_booster_is_on = False
                                if jelly_is_on:
                                    jelly_is_on = False
                                    del self._jelly_fish
                                if octopus_is_on:
                                    octopus_is_on = False
                                    del self._octopus
                                obstacle_time = 0
                                game_is_on = False
                                self.finish_game()
                        # put the fish on the screen if there is no collision
                        else:
                            self._screen.blit(fish.get_image(), fish.get_rect())

                # remove the fish that are eaten by our fish from the game
                for fish in remove_list:
                    self._other_fish.remove(fish)
                    del fish
                # our fish gets slower if player doesn't move our fish
                self._main_fish.decelerate()
                # we draw our fish on the screen
                self._screen.blit(self._main_fish.get_image(), self._main_fish.get_rect())
                if jelly_is_on: self._screen.blit(self._jelly_fish.get_image(), self._jelly_fish.get_rect())
                if octopus_is_on: self._screen.blit(self._octopus.get_image(), self._octopus.get_rect())
                if speed_booster_is_on: self._screen.blit(self._speed_booster.get_image(), self._speed_booster.get_rect())
                if size_booster_is_on: self._screen.blit(self._size_booster.get_image(),
                                                          self._size_booster.get_rect())
            # if the game is over, we display a screen that says game is over
            else:
                text = self._font_game_over.render("GAME OVER", True, (255, 255, 255))
                self._screen.blit(text, (420, 200))
                restart = self._font_restart.render("PRESS R TO RESTART", True, (255, 255, 255))
                self._screen.blit(restart, (460, 300))
                # if the player presses "R" we restart the game again
                key_input = pygame.key.get_pressed()
                if key_input[pygame.K_r]:
                    start = True
                    game_is_on = True
            # update the display
            pygame.display.flip()
            pygame.display.update()


game = Game()
game.run_game()