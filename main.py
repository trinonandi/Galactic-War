import pygame
import random
import math

# initialisation
pygame.init()
# setting the CPU clock
# setting the clock is necessary as it prevents fast gameplay in powerful cpu
clock = pygame.time.Clock()

# creating the display Surface of 800x600 size
screen = pygame.display.set_mode(size=(800, 600))

# setting title and icon
pygame.display.set_caption('Space Invader')  # setting the title
icon = pygame.image.load('assets/icon.png')  # loading the icon asset
pygame.display.set_icon(icon)

# loading the image assets
enemy_1_img = pygame.image.load('assets/enemy1.png').convert_alpha()
player_img = pygame.image.load('assets/player.png').convert_alpha()
background_img = pygame.image.load('assets/background.png').convert_alpha()
laser_player_img = pygame.image.load('assets/laser_player.png').convert_alpha()

# setting constant fields

# we are using random numbers to spawn enemies randomly on the screen
ENEMY_SPAWN_X = (0, 735)
ENEMY_SPAWN_Y = (50, 150)
ENEMY_X_MOVE = 0.5  # initially the enemy will start to move in the right direction
ENEMY_Y_MOVE = 40   # enemy will never move up so always +40 downwards

PLAYER_MOVE = 1
INIT_PLAYER_X = 370
INIT_PLAYER_Y = 500
LASER_PLAYER_MOVE = 4

SCREEN_BOUND = 736  # 800 - 64 = 736 as our player image is 64 x 64
FPS = 300


def has_collided(x1: int, y1: int, x2: int, y2: int) -> bool:
    """
    checks if two object has collided or not
    we can do this by calculating the distance between the two objects
    :param x1: x coordinate of 1st object
    :param y1: y coordinate of 1st object
    :param x2: x coordinate of 2nd object
    :param y2: y coordinate of 2nd object
    :return: boolean
    """

    x_sq = math.pow((x2 - x1), 2)
    y_sq = math.pow((y2 - y1), 2)
    distance = math.sqrt(x_sq + y_sq)
    return distance < 50


class Score:
    """
    A class to contain the score information
    ...
    Attributes
    ----------
    total_score : int   total score of the game
    font : pygame Font  holds the font of the displayed score
    score_x : int       x coordinate of the displayed score
    score_y : int       y coordinate of the displayed  score

    Methods
    -------
    show_score() -> None    renders and draws the score on the screen
    """
    def __init__(self):
        self.total_score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.score_x = 10
        self.score_y = 10

    def show_score(self) -> None:
        rendered_score = self.font.render("Score : " + str(self.total_score), True, (255, 255, 255))
        screen.blit(rendered_score, (self.score_x, self.score_y))


class Enemy:
    def __init__(self):

        self.enemy_x = []
        self.enemy_y = []
        self.enemy_x_change = ENEMY_X_MOVE
        self.enemy_y_change = ENEMY_Y_MOVE
        self.enemy_count = 6
        self.make_enemy_list()

    def make_enemy_list(self):
        for _ in range(self.enemy_count):
            self.enemy_x.append(random.randint(ENEMY_SPAWN_X[0], ENEMY_SPAWN_X[1]))
            self.enemy_y.append(random.randint(ENEMY_SPAWN_Y[0], ENEMY_SPAWN_Y[1]))

    def set_enemy(self, index) -> None:
        screen.blit(enemy_1_img, (self.enemy_x[index], self.enemy_y[index]))


class Player:
    def __init__(self):
        self.player_x = INIT_PLAYER_X
        self.player_y = INIT_PLAYER_Y
        self.player_x_change = 0

    def set_player(self) -> None:
        # blit() method draws the image (Surface) on the (x, y) coordinate
        screen.blit(player_img, (self.player_x, self.player_y))


class PlayerLaser:
    def __init__(self):
        self.laser_player_x = 0
        self.laser_player_y = INIT_PLAYER_Y  # initially same level as player
        self.laser_player_change_y = LASER_PLAYER_MOVE
        self.laser_player_fire = False  # true means laser has been fired

    def fire_player_laser(self) -> None:
        screen.blit(laser_player_img, (self.laser_player_x + 25, self.laser_player_y + 10))

    def reset_player_laser(self):
        self.laser_player_x = 0
        self.laser_player_y = INIT_PLAYER_Y
        self.laser_player_fire = False


player = Player()
player_laser = PlayerLaser()
enemy = Enemy()
score = Score()

# tracks the running state of the window
running = True
# game loop, A loop to keep the window alive starts
while running:
    # locking to a certain fps
    clock.tick(FPS)

    # every time we need to set the screen background before drawing players to remove ghosting
    # screen.fill((255, 255, 255))
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        # pygame.event.get() gets event from the Event Queue
        if event.type == pygame.WINDOWCLOSE:
            # checks if the event is a window close button pressed event
            running = False

        # checking for keyboard key stroke events
        if event.type == pygame.KEYDOWN:
            # KEYDOWN is used to check a button down (press) event
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                # event is a dict type object with a 'key' as a key and keyboard button code as the value
                # left movement
                player.player_x_change = -PLAYER_MOVE
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                # right movement
                player.player_x_change = PLAYER_MOVE
            if event.key == pygame.K_SPACE:
                # fire laser
                if not player_laser.laser_player_fire:
                    player_laser.laser_player_fire = True
                    player_laser.laser_player_x = player.player_x

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player.player_x_change = 0

    # to prevent the out of screen issue
    new_player_x = player.player_x + player.player_x_change
    if new_player_x <= 0 or new_player_x >= SCREEN_BOUND:
        player.player_x_change = 0
    # updates the player's coordinates
    player.player_x += player.player_x_change

    # enemy movements
    for i in range(6):
        enemy.enemy_x[i] += enemy.enemy_x_change
        if enemy.enemy_x[i] <= 0:
            # moving enemy to down and right
            enemy.enemy_x_change = ENEMY_X_MOVE
            enemy.enemy_y[i] += enemy.enemy_y_change
        elif enemy.enemy_x[i] >= SCREEN_BOUND:
            # moving enemy to down and left
            enemy.enemy_x_change = -ENEMY_X_MOVE
            enemy.enemy_y[i] += enemy.enemy_y_change

        # player's laser collision
        if has_collided(enemy.enemy_x[i], enemy.enemy_y[i], player_laser.laser_player_x, player_laser.laser_player_y):
            # reset player's laser, increase score by 1 and respawn enemy
            player_laser.reset_player_laser()
            score.total_score += 1
            enemy.enemy_x[i] = random.randint(ENEMY_SPAWN_X[0], ENEMY_SPAWN_X[1])
            enemy.enemy_y[i] = random.randint(ENEMY_SPAWN_Y[0], ENEMY_SPAWN_Y[1])

        enemy.set_enemy(i)

    # player's laser movement
    if player_laser.laser_player_y <= 0:
        # laser crossed the screen so reset it
        player_laser.reset_player_laser()

    if player_laser.laser_player_fire:
        player_laser.laser_player_y -= player_laser.laser_player_change_y
        # these constants +25 +10 are to align the laser with the player
        player_laser.fire_player_laser()

    player.set_player()
    score.show_score()
    # display.update() will update any change happened on the screen
    pygame.display.update()

pygame.quit()
