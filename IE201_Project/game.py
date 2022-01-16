import random
import pygame
import sys
pygame.init()
from classes import FishingRod, FishingNet, MainFish, OtherFish, SpeedBooster, SizeBooster, Octapus, JellyFish, UserInput

class Game:
    def __init__(self):
        self._difficulty = 0
        self._width = 1300
        self._height = 590
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._background = pygame.image.load("game_assets/background/background.jpg").convert()
        self._background = pygame.transform.scale(self._background, (self._width, self._height))
        self._other_fish = dict()
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
        self._win = 0
        self._left = True
        self._finish = False

    def start_game(self, start):
        if start == False: return 0
        self._main_fish = MainFish()
        for i in range(5):
            while True:
                fish = OtherFish(self._main_fish.get_width(), self.get_difficulty())
                if self._main_fish.get_rect().colliderect(fish.get_rect()):
                    del fish
                    continue
                self._other_fish[OtherFish(self._main_fish.get_width(), self.get_difficulty())] = [False, 0, 0]
                break

    def finish_game(self):
        self._game_is_on = False
        self._finish = False
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
        for fish in self._other_fish.keys():
            del fish
        self._other_fish = dict()
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
                self._difficulty = 0
            elif self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 255 <= mouse[1] <= 345:
                self._main_menu = False
                self._difficulty = 1
            elif self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 370 <= mouse[1] <= 460:
                self._main_menu = False
                self._difficulty = 2

    def get_difficulty(self):
        return self._difficulty

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
                        fish = OtherFish(self._main_fish.get_width(), self.get_difficulty())
                        # we again check if it collides with our fish
                        if self._main_fish.get_rect().colliderect(fish.get_rect()):
                            del fish
                            continue
                        self._other_fish[fish] = [False, 0, 0]
                        break
                    # we update the velocities of all fish every 4 seconds
                    # they change both direction and speed
                for fish in self._other_fish.keys():
                    if self._other_fish[fish][2] >= 5000:
                        fish.update_velocity()
                        self._other_fish[fish][2] = 0
                    self._other_fish[fish][2] += time
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
                        self._finish = True

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
                for fish in self._other_fish.keys():
                    # we check if fish are on the edges of the screen
                    # if so we update the velocity
                    if fish.get_rect().top + fish.get_vertical_velocity() < 0 or fish.get_rect().bottom + fish.get_vertical_velocity() > self._height:
                        fish.corner_vertical()

                    if fish.get_rect().left + fish.get_horizontal_velocity() < 0 or fish.get_rect().right + fish.get_horizontal_velocity() > self._width:
                        fish.corner_horizontal()

                    # if the other fish collides with jellyfish, it changes direction
                    if self._jelly_is_on:
                        if fish.get_rect().colliderect(self._jelly_fish.get_rect()):
                            if self._other_fish[fish][0] == False:
                                fish.change_direction()
                                self._other_fish[fish][0] = True

                    # if the other fish collides with octopus, it changes direction
                    if self._octopus_is_on:
                        if fish.get_rect().colliderect(self._octopus.get_rect()):
                            if self._other_fish[fish][0] == False:
                                fish.change_direction()
                                self._other_fish[fish][0] = True

                    # if the other fish collides with fishing net, it changes direction
                    if self._net_is_on:
                        if fish.get_rect().colliderect(self._net.get_rect()):
                            if self._other_fish[fish][0] == False:
                                fish.change_direction()
                                self._other_fish[fish][0] = True

                    # if the other fish collides with fishing rod, it changes direction
                    if self._rod_is_on:
                        if fish.get_rect().colliderect(self._rod.get_rect()):
                            if self._other_fish[fish][0] == False:
                                fish.change_direction()
                                self._other_fish[fish][0] = True

                    # if the other fish collides with size booster, it changes direction
                    if self._size_booster_is_on:
                        if fish.get_rect().colliderect(self._size_booster.get_rect()):
                            if self._other_fish[fish][0] == False:
                                fish.change_direction()
                                self._other_fish[fish][0] = True

                    # if the other fish collides with speed booster, it changes direction
                    if self._speed_booster_is_on:
                        if fish.get_rect().colliderect(self._speed_booster.get_rect()):
                            if self._other_fish[fish][0] == False:
                                fish.change_direction()
                                self._other_fish[fish][0] = True

                    if self._other_fish[fish][0]:
                        self._other_fish[fish][1] += time
                        if self._other_fish[fish][1] > 500:
                            self._other_fish[fish][1] = 0
                            self._other_fish[fish][0] = False

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
                            self._finish = True
                    # if our fish doesn't collide, game continues as usual
                    else:
                        # move the fish
                        fish.move()
                        if fish.get_horizontal_velocity() > 0: self._screen.blit(pygame.transform.flip(fish.get_image(), True, False), fish.get_rect())
                        else: self._screen.blit(fish.get_image(), fish.get_rect())

                # remove the fish that are eaten by our fish from the game
                for fish in remove_list:
                    self._other_fish.pop(fish)
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
                if self._main_fish.get_horizontal_velocity() < 0:
                    self._screen.blit(self._main_fish.get_image(), self._main_fish.get_rect())
                    self._left = True
                elif self._main_fish.get_horizontal_velocity() > 0:
                    self._screen.blit(pygame.transform.flip(self._main_fish.get_image(), True, False), self._main_fish.get_rect())
                    self._left = False
                else:
                    if self._left: self._screen.blit(self._main_fish.get_image(), self._main_fish.get_rect())
                    else: self._screen.blit(pygame.transform.flip(self._main_fish.get_image(), True, False), self._main_fish.get_rect())
                if self._rod_is_on:
                    self._rod.move(self._rod_timer)
                    if self._main_fish.get_rect().colliderect(self._rod.get_rect()):
                        self._finish = True

                if self._net_is_on:
                    self._net.move(self._net_timer)
                    if self._main_fish.get_rect().colliderect(self._net.get_rect()):
                        self._finish = True

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
                self._main_fish.zero_velocity()
                # we move our jellyfish if it is on the screen
                if self._jelly_is_on: self._jelly_fish.move()
                if self._octopus_is_on: self._octopus.move()

                if self._net_is_on: self._screen.blit(self._net.get_image(), self._net.get_rect())
                if self._rod_is_on: self._screen.blit(self._rod.get_image(), self._rod.get_rect())
                if self._jelly_is_on: self._screen.blit(self._jelly_fish.get_image(), self._jelly_fish.get_rect())
                if self._octopus_is_on: self._screen.blit(self._octopus.get_image(), self._octopus.get_rect())
                if self._speed_booster_is_on: self._screen.blit(self._speed_booster.get_image(), self._speed_booster.get_rect())
                if self._size_booster_is_on: self._screen.blit(self._size_booster.get_image(), self._size_booster.get_rect())

                # winning scenario for the game, if the score is bigger than 30, you win
                if self._score >= 30:
                    self._finish = True
                    self._win = 1

                if self._finish:
                    self.finish_game()

            # if the game is over, we display a screen that says game is over
            else:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                key_input = pygame.key.get_pressed()
                if self._win == 0:
                    text = self._font_game_over.render("GAME OVER", True, (255, 255, 255))
                    self._screen.blit(text, (440, 120))
                else:
                    text = self._font_game_over.render("YOU WON!", True, (255, 255, 255))
                    self._screen.blit(text, (460, 120))
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
                        self._win = 0
                    if 475 <= mouse[0] <= 775 and 350 <= mouse[1] <= 440:
                        self._start = True
                        self._game_is_on = True
                        self._win = 0
                # if the player presses "R" we restart the game again
                if key_input[pygame.K_r]:
                    self._start = True
                    self._game_is_on = True
                    self._win = 0
            # update the display
            pygame.display.flip()
            pygame.display.update()


game = Game()
game.run_game()
