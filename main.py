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
ENEMY_SPAWN_X = (0, 735)
ENEMY_SPAWN_Y = (50, 150)
ENEMY_X_MOVE = 0.5
ENEMY_Y_MOVE = 40
PLAYER_MOVE = 1
INIT_PLAYER_X = 370
INIT_PLAYER_Y = 500
LASER_PLAYER_MOVE = 4
FPS = 300


def set_player(x, y) -> None:
    # screen.fill((255, 255, 255))
    screen.blit(player_img, (x, y))  # blit() method draws the image (Surface) on the (x, y) coordinate


def set_enemy(x, y) -> None:
    screen.blit(enemy_1_img, (x, y))


def fire_player_laser(x, y) -> None:
    screen.blit(laser_player_img, (x, y))


def has_collided(x1, y1, x2, y2) -> bool:
    # we can check if two objects have collided by calculating the distance between them
    x_sq = math.pow((x2 - x1), 2)
    y_sq = math.pow((y2 - y1), 2)
    distance = math.sqrt(x_sq + y_sq)
    return distance < 50


def show_score(x, y, font, total_score):
    score = font.render("Score : " + str(total_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_loop() -> None:
    # player
    player_x = INIT_PLAYER_X
    player_y = INIT_PLAYER_Y
    player_x_change = 0

    # enemy
    # we are using random numbers to spawn enemies randomly on the screen
    enemy_x = []
    enemy_y = []
    enemy_x_change = ENEMY_X_MOVE  # initially the enemy will start to move in the right direction
    enemy_y_change = ENEMY_Y_MOVE  # enemy will never move up so always +40 downwards
    enemy_count = 6
    for _ in range(enemy_count):
        enemy_x.append(random.randint(ENEMY_SPAWN_X[0], ENEMY_SPAWN_X[1]))
        enemy_y.append(random.randint(ENEMY_SPAWN_Y[0], ENEMY_SPAWN_Y[1]))

    # laser_player
    laser_player_x = 0
    laser_player_y = INIT_PLAYER_Y    # initially same level as player
    laser_player_change_y = LASER_PLAYER_MOVE
    laser_player_fire = False   # true means laser has been fired

    # scores
    total_score = 0
    font = pygame.font.Font('freesansbold.ttf', 28)
    score_x = 10
    score_y = 10

    running = True  # tracks the running state of the window
    while running:
        # locking to a certain fps
        clock.tick(FPS)

        # every time we need to set the screen background before drawing players to remove ghosting
        # screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))

        # A loop to keep the window alive
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
                    player_x_change = -PLAYER_MOVE
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    # right movement
                    player_x_change = PLAYER_MOVE
                if event.key == pygame.K_SPACE:
                    # fire laser
                    if not laser_player_fire:
                        laser_player_fire = True
                        laser_player_x = player_x

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    player_x_change = 0

        # to prevent the out of screen issue
        new_player_x = player_x + player_x_change
        if new_player_x <= 0 or new_player_x >= 736:  # 800 - 64 = 736 as our player image is 64 x 64
            player_x_change = 0
        # updates the player's coordinates
        player_x += player_x_change

        # enemy movements
        for i in range(6):
            enemy_x[i] += enemy_x_change
            if enemy_x[i] <= 0:
                # moving enemy to down and right
                enemy_x_change = ENEMY_X_MOVE
                enemy_y[i] += enemy_y_change
            elif enemy_x[i] >= 736:
                # moving enemy to down and left
                enemy_x_change = -ENEMY_X_MOVE
                enemy_y[i] += enemy_y_change

            # player's laser collision
            if has_collided(enemy_x[i], enemy_y[i], laser_player_x, laser_player_y):
                # reset bullet, increase score by 1 and respawn enemy
                laser_player_x = 0
                laser_player_y = INIT_PLAYER_Y
                laser_player_fire = False
                total_score += 1
                enemy_x[i] = random.randint(ENEMY_SPAWN_X[0], ENEMY_SPAWN_X[1])
                enemy_y[i] = random.randint(ENEMY_SPAWN_Y[0], ENEMY_SPAWN_Y[1])
                print(total_score)

            set_enemy(enemy_x[i], enemy_y[i])

        # player's laser movement
        if laser_player_y <= 0:
            # laser crossed the screen so reset it
            laser_player_x = 0
            laser_player_y = INIT_PLAYER_Y
            laser_player_fire = False

        if laser_player_fire:
            laser_player_y -= laser_player_change_y
            # these constants +25 +10 are to align the laser with the player
            fire_player_laser(laser_player_x + 25, laser_player_y + 10)

        set_player(player_x, player_y)
        show_score(score_x, score_y, font, total_score)
        # display.update() will update any change happened on the screen
        pygame.display.update()


game_loop()
pygame.quit()
