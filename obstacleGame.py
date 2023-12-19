import pygame
import random
import time
import threading
from obstacle import Obstacle
from player import Player
from PIL import Image
import numpy as np

# Initialize Pygame
pygame.init()

# Set screen size and title
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Obstacle Game (Mario Edition)")
screen_width = 640
screen_height = 480

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#Load the background images for the game.
pictureOne = Image.open("bg1.jpeg")
pictureTwo = Image.open("bg2.jpeg")
pictureThree = Image.open("bg3.jpeg")
pictureFour = Image.open("bg4.jpeg")


def get_background_image(time_of_day):
    """
    this function selects a different background at certain intervals
    :param time_of_day:
    :return: backGround Image
    """
    if time_of_day < 0.2:
        return pictureOne
    elif time_of_day < 0.4:
        return Image.blend(pictureOne, pictureTwo, (time_of_day - 0.2) * 4)
    elif time_of_day < 0.6:
        return Image.blend(pictureTwo, pictureThree, (time_of_day - 0.4) * 4)
    else:
        return Image.blend(pictureThree, pictureFour, (time_of_day - 0.6) * 4)


def update_background(time_of_day):
    background_image = get_background_image(time_of_day)
    background_array = np.array(background_image)  # convert PIL image to NumPy array
    background_surface = pygame.surfarray.make_surface(background_array)  # convert NumPy array to Pygame surface
    background_surface = pygame.transform.scale(background_surface, (800, 600))  # scale the image to the screen size
    return background_surface


# Start the background thread
bg_thread = threading.Thread(target=update_background)
bg_thread.start()
# Define function to spawn obstacles
running = True


def spawn_obstacle():
    """
    This function spawns obstacles and adds them  to the game sprite
    It also has a 20% chance of spawning a coin instead of an obstacle.

    """
    while True:
        if not running:
            break

        obstacle_count =  random.randint(1, 5)  # spawn 1-3 obstacles at once
        for i in range(obstacle_count):
            obstacle = Obstacle()

            if random.random() < 0.2:  # 20% chance of spawning a coin
                obstacle.is_coin = True
                obstacle.image = pygame.image.load('coin.png')  # load a coin image
                obstacle.image = pygame.transform.scale(obstacle.image, (40, 40))
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
        time.sleep(random.randint(1, 2))


# Initialize game variables
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
spawn_thread = threading.Thread(target=spawn_obstacle)
spawn_thread.start()
font = pygame.font.SysFont(None, 36)

time_of_day = 0  # initialize time of day
# This loop will run until the user exits or chooses to restart the game
while True:
    running = True
    player.score = 0

    while running:  # loop through all events in the queue
        for event in pygame.event.get():
            # handles the different cases of users inputs
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.USEREVENT:
                obstacle = Obstacle() # create a new obstacle
                if random.random() < 0.2: # 20% chance of obstacle being a coin
                    obstacle.is_coin = True
                    obstacle.image = pygame.image.load('coin.png')
                    obstacle.image = pygame.transform.scale(obstacle.image, (50, 50))
                all_sprites.add(obstacle)
                obstacles.add(obstacle)

        all_sprites.update() # update all sprite
        hits = pygame.sprite.spritecollide(player, obstacles, False) # check  for collision between player and obstacle
        for obstacle in hits:
            if obstacle.is_coin:
                player.score += 10  # increase score by 10 for each coin
                obstacle.kill()
            else:
                running = False # set flag to false to end the game
        else:
            for obstacle in obstacles: # for the obstacle in the obstacle group , if it has passed the  the player and
                # has not been scored add one to players score
                if obstacle.rect.right < player.rect.left and not obstacle.scored:
                    obstacle.scored = True
                    player.score += 1

        time_of_day += 0.0005  # increase time of day
        if time_of_day >= 1:
            time_of_day = 0  # reset time of day
        background_surface = update_background(time_of_day)  # update the background surface
        screen.blit(background_surface, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {player.score}", True, WHITE) # create text to display players score
        screen.blit(score_text, (10, 10))
        clock.tick(60) # limit to 60 frames per second
        pygame.display.flip()
    # fill screen with black when player loses
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE) # display game over
    screen.blit(game_over_text, (250, 200))
    pygame.display.flip()

    # wait for player to resart or end the game

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    running = True
                    break
                elif event.key == pygame.K_n:
                    pygame.quit()
                    quit()
        if running:
            break
