import pygame
import random

# initialisation
pygame.init()

# creating the display Surface of 800x600 size
screen = pygame.display.set_mode(size=(800, 600))

# setting title and icon
pygame.display.set_caption('Space Invader')  # setting the title
icon = pygame.image.load('assets/icon.png')  # loading the icon asset
pygame.display.set_icon(icon)

enemy_1_img = pygame.image.load('assets/enemy1.png')
player_img = pygame.image.load('assets/player.png')  # loads the image of player as a Surface


def set_player(x, y) -> None:
    screen.fill((255, 255, 255))
    screen.blit(player_img, (x, y))  # blit() method draws the image (Surface) on the (x, y) coordinate


def set_enemy(x, y) -> None:
    screen.blit(enemy_1_img, (x, y))


def game_loop() -> None:
    # A loop to keep the window alive
    player_x = 370
    player_y = 500
    player_x_change = 0
    player_y_change = 0

    enemy_x = random.randint(0, 800)
    enemy_y = random.randint(50, 150)
    enemy_x_change = 0.3
    enemy_y_change = 40

    running = True  # tracks the running state of the window
    while running:
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
                    player_x_change = -0.35
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    # event is a dict type object with a 'key' as a key and keyboard button code as the value
                    player_x_change = 0.35

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
        enemy_x += enemy_x_change
        if enemy_x <= 0:
            enemy_x_change = 0.3
            enemy_y += enemy_y_change
        elif enemy_x >= 736:
            enemy_x_change = -0.3
            enemy_y += enemy_y_change
        set_player(player_x, player_y)
        set_enemy(enemy_x, enemy_y)
        pygame.display.update()  # display.update() will update any change happened on the screen


game_loop()
pygame.quit()
