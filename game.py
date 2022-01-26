import random
import pygame
import sys
pygame.init()
# importing the necessary classes from classes.py
from classes import FishingRod, FishingNet, MainFish, OtherFish, SpeedBooster, SizeBooster, Octapus, JellyFish, UserInput

# main game class, our game skeleton is inside this class.
class Game:
    # initializing the Game class.
    def __init__(self):
        # difficult level, 0 for easy, 1 for medium and 2 for hard
        self._difficulty = 0
        # width of the game screen
        self._width = 1300
        # height of the game screen
        self._height = 590
        # pygame main game screen
        self._screen = pygame.display.set_mode((self._width, self._height))
        # loading background image
        self._background = pygame.image.load("game_assets/background/background.jpg").convert()
        # scaling the background image to fit our game screen
        self._background = pygame.transform.scale(self._background, (self._width, self._height))
        # other fish dictionary, keys are the OtherFish objects, they map to a list defining some attributes of OtherFish
        # we keep the OtherFish (these are the fish that our MainFish can eat or get eaten by
        self._other_fish = dict()
        # score as integer, basically the number of fish eaten by our MainFish
        self._score = 0
        # we use "monospace" as our main font style
        # sizes of the fonts differ by the use case
        self._font_score = pygame.font.SysFont("monospace", 25)
        self._font_game_over = pygame.font.SysFont("monospace", 70)
        self._font_restart = pygame.font.SysFont("monospace", 40)
        # clock object, we keep track of the time passed and use it to control the internals of the game
        self._clock = pygame.time.Clock()
        # game time controls the main time, every 4 seconds we introduce an additional OtherFish to game.
        # we set game time to 0 every 4 seconds after introducing the OtherFish to game.
        self._game_time = 0
        # boolean, if True, main menu opens
        self._main_menu = True
        # boolean, if True, the actual game will start
        self._game_is_on = True
        # boolean, if True, JellyFish is in the game
        self._jelly_is_on = False
        # boolean, if True, Octopus is in the game
        self._octopus_is_on = False
        # boolean, if True, SpeedBooster is in the game
        self._speed_booster_is_on = False
        # boolean, if True, SizeBooster is in the game
        self._size_booster_is_on = False
        # boolean, if True, our MainFish's speed is boosted
        self._speed_boosted = False
        # boolean, if True, our MainFish's size is boosted
        self._size_boosted = False
        # speed boost duration, if the SpeedBooster is taken by our MainFish..
        # .. speed is boosted for only a limited amount of time.
        # if the speed is boosted a count-up begins to reach self._speed_boosted_duration
        # when it is reached, the speed will not be boosted anymore ant turn to normal
        self._speed_boosted_duration = 0
        # size boost duration, if the SizeBooster is taken by our MainFish..
        # .. size is boosted for only a limited amount of time.
        # if the size is boosted a count-up begins to reach self._size_boosted_duration
        # when it is reached, the size will not be boosted anymore ant turn to normal.
        self._size_boosted_duration = 0
        # SpeedBooster objects will appear in the game periodically.
        # self._speed_booster_time is the value of this period in milliseconds.
        self._speed_booster_time = random.uniform(20000, 40000)
        # SizeBooster objects will appear in the game periodically.
        # self._size_booster_time is the value of this period in milliseconds.
        self._size_booster_time = random.uniform(20000, 40000)
        # if the SpeedBooster is not in the game, this counter will count-up, when its value is equal to..
        # ..the value of self._speed_booster_time, the SpeedBooster will be introduced in the game
        self._speed_booster_timer = 0
        # if the SizeBooster is not in the game, this counter will count-up, when its value is equal to..
        # ..the value of self._size_booster_time, the SizeBooster will be introduced in the game
        self._size_booster_timer = 0
        # if our MainFish collides with the JellyFish, MainFish will be freezed by JellyFish for a certain amount of time.
        # when so, a count-up begins. when the time is up, our MainFish will be able to move again.
        self._freeze_timer = 0
        # self._freeze, binary value, if freezed 0, if not 1
        # helps us to adjust the speed of our MainFish by simply multiplying by it.
        self._freeze = 1
        # boolean, if True, 5 OtherFish will be introduced into the game
        # REMARK: Initially we introduce 5 OtherFish in the game
        self._start = True
        # FishingRod timer, rod will stay a certain amount of time in the game,
        # when its time is up, it will exit the game
        self._rod_timer = 0
        # FishingNet timer, rod will stay a certain amount of time in the game,
        # when its time is up, it will exit the game
        self._net_timer = 0
        # boolean, if True, FishingRod is in the game
        self._rod_is_on = False
        # boolean, if True, FishingNet is in the game
        self._net_is_on = False
        # FishingRod will enter the game periodically, self._rod_time sets this time.
        # when its randomly determined time comes (between 20-40 seconds), FishingRod will enter the game.
        self._rod_time = random.uniform(20000, 40000)
        # FishingNet will enter the game periodically, self._net_time sets this time.
        # when its randomly determined time comes (between 20-40 seconds), FishingNet will enter the game.
        self._net_time = random.uniform(20000, 40000)
        # SizeBooster's variable, initially no SizeBooster is in the game, so set to None
        # a SizeBooster object will be assigned periodically inside the game
        self._size_booster = None
        # SpeedBooster's variable, initially no SpeedBooster is in the game, so set to None
        # a SpeddBooster object will be assigned periodically inside the game
        self._speed_booster = None
        # JellyFish's variable, initially no JellyFish is in the game, so set to None
        # a JellyFish object will be assigned periodically inside the game
        self._jelly_fish = None
        # Octopus's variable, initially no Octopus is in the game, so set to None
        # a Octopus object will be assigned periodically inside the game
        self._octopus = None
        # FishingNet's variable, initially no FishingNet is in the game, so set to None
        # a FishingNet object will be assigned periodically inside the game
        self._net = None
        # FishingRod's variable, initially no FishingRod is in the game, so set to None
        # a FishingRod object will be assigned periodically inside the game
        self._rod = None
        # self._win, binary variable, if the player wins the game, set to 1, if not, to 0
        self._win = 0
        # boolean, determines whether the left or right side of the MainFish should be on the screen
        # by side, we mean the right and left perspective of the MainFish
        self._left = True
        # boolean, if True game is finished, if not, game will continue
        self._finish = False

    # the function that builds the initial state of the game
    # it will introduce the MainFish and 5 OtherFish to the game
    def start_game(self, start):
        if start == False: return 0
        # creating the MainFish
        self._main_fish = MainFish()
        for i in range(5):
            # making sure that the OtherFish objects we are going to create does not collide ..
            # .. with our MainFish at the time of creation.
            while True:
                fish = OtherFish(self._main_fish.get_width(), self.get_difficulty())
                # if it collides with our MainFish at the time of creation, we simply ..
                # delete it and create it again until it does not collide with our MainFish.
                if self._main_fish.get_rect().colliderect(fish.get_rect()):
                    del fish
                    continue
                # adding the OtherFish object that we just created to the dictionary with its initial value [False, 0, 0]
                self._other_fish[OtherFish(self._main_fish.get_width(), self.get_difficulty())] = [False, 0, 0]
                break

    # when the game is finished, we reset all the pareameters inside the game to their initial values ..
    # and prepare the game for a possible restart
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

    # updating all the timers by the time elapsed in the game loop
    def update_timers(self, time):
        self._game_time += time
        self._speed_booster_timer += time
        self._size_booster_timer += time
        self._rod_timer += time
        self._net_timer += time
        # we update self._freeze_timer only if our MainFish is currently frozen
        if self._freeze == 0: self._freeze_timer += time
        # we update self._speed_boosted only if the speed of our MainFish is boosted
        if self._speed_boosted: self._speed_boosted_duration += time
        # we update self._size_boosted only if the size of our MainFish is boosted
        if self._size_boosted: self._size_boosted_duration += time

    # main menu of the game
    # player can choose the difficulty level she wants
    def main_menu(self, mouse, click=False):
        # if mouse is hovered over the rectangle, we highlight it by changing its color slightly
        if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 140 <= mouse[1] <= 230:
            pygame.draw.rect(self._screen, (144, 238, 144), [self._width / 3 + 15, 140, 300, 90],
                             border_radius=20)
        else:
            pygame.draw.rect(self._screen, (127, 255, 0), [self._width / 3 + 15, 140, 300, 90],
                             border_radius=20)
        # if mouse is hovered over the rectangle, we highlight it by changing its color slightly
        if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 255 <= mouse[1] <= 345:
            pygame.draw.rect(self._screen, (255, 255, 102), [self._width / 3 + 15, 255, 300, 90],
                             border_radius=20)
        else:
            pygame.draw.rect(self._screen, (255, 255, 0), [self._width / 3 + 15, 255, 300, 90], border_radius=20)
        # if mouse is hovered over the rectangle, we highlight it by changing its color slightly
        if self._width / 3 + 15 <= mouse[0] <= self._width / 3 + 315 and 370 <= mouse[1] <= 460:
            pygame.draw.rect(self._screen, (255, 127, 127), [self._width / 3 + 15, 370, 300, 90], border_radius=20)
        else:
            pygame.draw.rect(self._screen, (255, 0, 0), [self._width / 3 + 15, 370, 300, 90], border_radius=20)
        # blitting the texts on the screen
        self._screen.blit(self._font_restart.render("EASY", True, (0, 0, 0)), (self._width / 3 + 111, 168))
        self._screen.blit(self._font_restart.render("MEDIUM", True, (0, 0, 0)),
                          (self._width / 3 + 100, 283))
        self._screen.blit(self._font_restart.render("HARD", True, (0, 0, 0)),
                          (self._width / 3 + 111, 398))
        # if the player clicked on a rectangle we check if he chose a difficulty level ..
        # if so, main menu screen will close and game will begin with the chosen difficulty
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

    # simply returns the difficulty level of the game that is currently running
    def get_difficulty(self):
        return self._difficulty

    # MAIN GAME LOOP
    # this is method that the actual body (while loop) of the game is in
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

            # if the self._main_menu attribute is True ..
            # .. we are in the main menu part of the game
            if self._main_menu:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                self.main_menu(mouse, click=click[0])

            # if self._main_menu is False, we check if the game ..
            # .. is live, continue if so
            elif self._game_is_on:
                # score_text is our live score that we display on the screen
                score_text = self._font_score.render("SCORE : " + str(self._score), True, (255, 255, 255))
                self._screen.blit(score_text, (1100, 50))
                # measure the time elapsed
                time = self._clock.get_time()
                # update all the timers
                self.update_timers(time)

                # MainFish will freeze for 3 seconds if it collides with a JellyFish
                # if 3 seconds elapsed since collisions, our MainFish is free to go
                if self._freeze_timer >= 3000:
                    self._freeze_timer = 0
                    self._freeze = 1
                # speed boosted duration, if MainFish is speed boosted, after a certain amount of time ..
                # its speed will return to normal.
                if self._speed_boosted_duration >= self._main_fish.get_boost_duration():
                    self._speed_boosted = False
                    self._speed_boosted_duration = 0
                # size boosted duration, if MainFish is size boosted, after a certain amount of time ..
                # its size will return to normal.
                if self._size_boosted_duration >= self._main_fish.get_boost_duration():
                    self._main_fish.reboost_size()
                    self._size_boosted = False
                    self._size_boosted_duration = 0

                # adding boosters if the time has come for them to be introduced in the game
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

                # if speed booster is in the game for a certain amount of time and has not been taken ..
                # by our MainFish, it will disappear from the screen
                if self._speed_booster_is_on:
                    if self._speed_booster_timer >= self._speed_booster.get_duration():
                        self._speed_booster_is_on = False
                        self._speed_booster_timer = 0
                        del self._speed_booster
                        self._speed_booster = None

                # if size booster is in the game for a certain amount of time and has not been taken ..
                # by our MainFish, it will disappear from the screen
                if self._size_booster_is_on:
                    if self._size_booster_timer >= self._size_booster.get_duration():
                        self._size_booster_is_on = False
                        self._size_booster_timer = 0
                        del self._size_booster
                        self._size_booster = None

                # we will introduce the JellyFish to the game if the score is more than 10
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
                        # when the jelly fish is created, the parameter "jellyfish_is_on" becomes True
                        self._jelly_is_on = True
                        break

                # we will introduce the Octopus to the game if the score is more than 10
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
                        # when the jelly fish is created, the parameter "octopus_is_on" becomes True
                        self._octopus_is_on = True
                        break
                # we add an OtherFish to the game every 4 seconds
                if self._game_time >= 4000:
                    self._game_time = 0
                    while True:
                        fish = OtherFish(self._main_fish.get_width(), self.get_difficulty())
                        # we again check if it collides with our fish
                        # if so we don't initialize the OtherFish and continue on random assignment
                        if self._main_fish.get_rect().colliderect(fish.get_rect()):
                            del fish
                            continue
                        self._other_fish[fish] = [False, 0, 0]
                        break
                # we update the velocities of all fish every 5 seconds
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

                # speed booster will disappear after a certain of amount time if it has not eaten by our fish
                if self._speed_booster_is_on:
                    if self._main_fish.get_rect().colliderect(self._speed_booster.get_rect()):
                        self._speed_boosted = True
                        self._speed_booster_is_on = False
                        del self._speed_booster
                        self._speed_booster = None
                        self._speed_booster_timer = 0

                # size booster will disappear after a certain of amount time if it has not eaten by our fish
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

                    # if a fish changed its direction lately (in 0.5 seconds) it will not be able to change its direction again
                    # this line prevents bugs like fish getting stuck inside an object
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
