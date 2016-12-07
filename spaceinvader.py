#!/usr/bin/python
"""
Simple Space Invaders like game

This code is a little example for using pygame to create 2D computer games.
It was created after watching some tutorials, I found on Youtube.

Just search for "pygame tutorial" on Youtube.

It's astounding how easy it is to create games with python and pygame.
A programm like this you can create in less then one workday, without much
experience with python and without any experiences with pygame.

Please don't use this script as an example for good game development. This is
code of an beginner and it is not more than an example for absolute beginners.
"""

# Impotrting some modules
# Be shure to have pygame installed
import sys, pygame, time
from pygame.locals import *



##################################################
#                                                #
#   Please read ahead at the end of this file,   #
#   where you'll find the "main function".       #
#                                                #
##################################################


pygame.init()
# Because we want to have several enemies,
# it's a good idea to create an object for each
class Enemy:
    # Intialize each enemy with a list of images, representing different states
    # and an individual position
    def __init__(self, images, position):
        # There is a whole list of images used for an enemy.
        # Each image represents a state
        # Most of them are for an animated explosion
        self.__images = images
        # Tehre is a basic position for each enemy
        self.__position = position
        # Set state to vital
        self.__state = 0
        # Initilize movement offset with zero
        self.__x_offset = 0
        self.__y_offset = 0
        # Start with moving to the right
        self.__xmove = 1

    # This method is called to verify and perform a hit by players shot
    def hit(self):
        # Only vital enemies can be hit
        if self.__state == 0:
            # Set state to first step of the explosion
            self.__state = 1
            # Confirm hit
            return True
        else:
            # Enemy can't be hit
            return False

    # This method is called in each time the game loops
    # it updates everything that happens automaticly
    def update(self):
        # A vital enemy moves
        if (self.__state == 0):
            # Change movement direction to right
            # if moved at least 40 pixels to the left
            if (self.__x_offset <= -40):
                self.__xmove = 1
            # Change movement direction to left
            # if moved at least 40 pixels to the right
            elif (self.__x_offset >= 40):
                self.__xmove = -1
            # Move sideward
            self.__x_offset += self.__xmove
            # Always move downward
            self.__y_offset += 1
        # If explowing the state chages
        # wich results in a different images for each step
        elif (self.__state < 8):
            self.__state += 1

    # An enemy can be moved by the main programm
    # Thats necessary when it has moved out of the screen
    def move_y(self, y):
        self.__y_offset += y

    # Returns the image which represents the enemy on the screen
    def get_image(self):
        # Return the right image for current state
        return self.__images[self.__state]

    # Returns the position, wehre the image of this object should be drawen
    def get_position(self):
        # Calculate upper left corner for drawing
        x = self.__position[0] - (self.__images[self.__state].get_width() / 2) + self.__x_offset
        y = self.__position[1] - (self.__images[self.__state].get_height() / 2) + self.__y_offset
        return [x, y]

    # Returns the objects center point
    # This is used for collition detection
    def get_center(self):
        x = self.__position[0] + self.__x_offset
        y = self.__position[1] + self.__y_offset
        return [x, y]


# Using an more or less object orientated programming style,
# the application or better game it self is an a class, where
# you create a single object from.
class Game:
    # Initalize the game
    def score(self):
        score = 0
        pygame.display.flip()
        pygame.display.update()

        # Player Name

    def name(self):
        name = 'Kevin'
        font = pygame.font.SysFont('monospace', 18)
        text_name = font.render('Name : ' + str(name), 1, (255, 255, 255))

        self.__screen.blit(text_name, (50, 10))
        pygame.display.update()

    def __init__(self):
        # Initialize display
        self.__display_size = [1024, 768]
        self.__screen = pygame.display.set_mode(self.__display_size)
        # Initialize clock to prevent game from running to fast
        self.__clock = pygame.time.Clock()
        # Initialize sound system
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)

        # Set image and position for players space ship
        self.__img_player = pygame.image.load("images/player.png")
        self.__pos_player = [0, 0]
        self.__pos_player[1] = self.__display_size[1] - self.__img_player.get_height()

        # Set image position and sounds for shot (Yes, this game is violent. ;-)
        self.__img_shot = pygame.image.load("images/shot.png")
        self.__pos_shot = [0, 0]
        self.__snd_shoot = pygame.mixer.Sound("sounds/laser.wav")
        self.__snd_explode = pygame.mixer.Sound("sounds/explode.wav")

        # Set images for enemies
        self.__img_enemy = [pygame.image.load("images/enemy.png"),
                            pygame.image.load("images/enemy1.png"),
                            pygame.image.load("images/enemy2.png"),
                            pygame.image.load("images/enemy3.png"),
                            pygame.image.load("images/enemy4.png"),
                            pygame.image.load("images/enemy5.png"),
                            pygame.image.load("images/enemy6.png"),
                            pygame.image.load("images/enemy7.png"),
                            pygame.image.load("images/enemy8.png")]
        # Set a list of enemy objects
        # and initialize 10 enemies with different positions for each
        self.__obj_enemies = list()
        for i in range(10):
            # Calculate individual position
            x = (50 + i * 100)
            y = 100 + (50 * (i % 2))
            # Initialize an enemy object
            self.__obj_enemies.append(Enemy(
                self.__img_enemy,
                [x, y]))

        # Load background image
        self.__img_backgroud = pygame.transform.scale(
            pygame.image.load("images/background.jpg"),
            self.__display_size)
        self.__screen.blit(self.__img_backgroud, [0, 0])
        # Set mouse cursor to be inviseble within the game window
        pygame.mouse.set_visible(False)

    def _action_shoot(self, x, y):
        # There can be just one shot at once
        if (self.__pos_shot[1] <= 0):
            # Make a sound when shooting
            self.__snd_shoot.play()
            # Set position of the shot centred right over
            # players space shipo
            self.__pos_shot = [x - (self.__img_shot.get_width() / 2),
                               self.__pos_player[1] - (self.__img_shot.get_height() / 2)]

    # Save a screenshot
    def _screenshot(self):
        # Yes, you can create screenshots from your game that easy
        pygame.image.save(self.__screen, "screenshot.png")

    # This method processes all events (user input)
    def _event_loop(self):
        # Get mouse cursor position
        x, y = pygame.mouse.get_pos()
        # Set the x-Position of the player
        # according to the mouse cursor position
        self.__pos_player[0] = x - (self.__img_player.get_width() / 2)
        # Process events
        for event in pygame.event.get():
            # Exit the game, when user klicks close window
            if event.type == pygame.QUIT:
                sys.exit(0)
            # Shoot when left mouse button is clicked
            elif event.type == MOUSEBUTTONDOWN:
                if (event.button == 1):
                    self._action_shoot(x, y)
            # Process keyboard events
            elif event.type == KEYDOWN:
                # Exit with [ESC] key
                if event.key == K_ESCAPE:
                    sys.exit(0)
                # Exit with [Q] key
                elif event.key == K_q:
                    sys.exit(0)
                # Take a screenshot with [S] key
                elif event.key == K_s:
                    sys.exit(0)
    # This method updates all things that are changing automaticly
    def _update(self):
        # Move enemies
        for enemy in self.__obj_enemies:
            # The enemy object has its own movement algorithm
            enemy.update()
            # If an enemy moves out of the bottom of the screen
            # it will be placed back to above the view port
            x, y = enemy.get_position()
            if (y > self.__display_size[1] + 100):
                enemy.move_y(0 - self.__display_size[1] - 200)
        # Move shoot if its on the way
        if (self.__pos_shot[1] > 0):
            self.__pos_shot[1] -= 10
            # Test if it hits an enemy
            for enemy in self.__obj_enemies:
                # Calculate distance between the enemy and the shot
                x, y = enemy.get_center()
                delta_x = self.__pos_shot[0] - x
                delta_y = self.__pos_shot[1] - y
                # If x and y distance between an enemy and shot
                # is less than 40 pixels the enemy is hit
                if (delta_x < 40) and (delta_x > -40) and (delta_y < 40) and (delta_y > -40):
                    # Is enemy really hit (if its not destroyed yet)
                    if (enemy.hit() == True):
                        # The shot must be reseted
                        self.__pos_shot[1] = 0
                        # A hit makes a sound
                        self.__snd_explode.play()
                        # One hit is enouth, other enemies
                        # don't need to be tested
                        break

    # This one brings everything to the screen, so that the user can see it.
    def _draw_screen(self):
        # Draw background
        self.__screen.fill([0, 0, 0])
        self.__screen.blit(self.__img_backgroud, [0, 0])
        # Draw enemies
        for enemy in self.__obj_enemies:
            self.__screen.blit(enemy.get_image(), enemy.get_position())
        # Draw player
        self.__screen.blit(self.__img_player, self.__pos_player)
        # Draw shot, if it is on its way to kill
        if (self.__pos_shot[1] > 0):
            self.__screen.blit(self.__img_shot, self.__pos_shot)
        # Update display
        pygame.display.update()


    # Runs the game
    def run(self):
        font = pygame.font.SysFont('monospace', 18)
        score = 0
        # Main loop, loops as long as the game runs
        while True:
            #vn = str(e1)

            # Clock time
            lt = time.localtime()
            stunde, minute, sekunde = lt[3:6]
            zeit = font.render("{0:02d}:{1:02d}:{2:02d}".format(stunde, minute, sekunde), 1, (255, 255, 255))
            pygame.display.flip()

            # Score
            fscore = round(score, 0)
            scoretext = font.render("Score : {0}".format(fscore), 1, (255, 255, 255))
            self.__screen.blit(zeit, (800, 10))
            self.__screen.blit(scoretext, (400, 10))
            score += 0.1

            # Zugriffsversuch Datei
            try:
                d = open("score_list.ods", "w")
            except:
                print("Dateizugriff nicht erfolgreich")
                sys.exit(0)

            # Schreiben
            li = (score)
            d.write(str(score).replace(".", ",") + "\n")

            # Schliessen
            d.close()
            if score >= 99.0:
                print("Du hast gewonnen")
            else:
                print("")

            pygame.display.update()

            # The clock preventing the game from doing more
            # than 60 loops per second.
            # It regulates game speed limits CPU usage
            self.__clock.tick(60)
            # The event loop processes events (user input)
            self._event_loop()
            # The update function for everything that moves automaticly
            self._update()
            # All chages done in one mainloop are drawen to the screen at last
            self._draw_screen()

# Main function
# The game starts here!
if __name__ == "__main__":
    # Initalice the game instance
    app = Game()
    # Run the game
    app.run()