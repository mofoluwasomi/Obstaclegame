from datetime import time
import pygame


# Define player class, this handles the movement and the scoring of the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the image for the player and scale it
        self.image = pygame.image.load("mario.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 275
        # Initialized the players speed and score to 0
        self.speed = 0
        self.score = 0

    def update(self):
        # check which key is currently being pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:  # if  the up arrow is pressed, set the players speed to 5 and move up
            self.speed = -5
        elif keys[pygame.K_DOWN]:  # if  the down arrow is pressed, set the players speed to 5 and move down
            self.speed = 5
        else:
            self.speed = 0
        if keys[pygame.K_LEFT]:  # if  the left arrow is pressed, set the players speed to 5 and move to the left
            self.rect.x -= 5
        elif keys[pygame.K_RIGHT]: # if  the right arrow is pressed, set the players speed to 5 and move to the right
            self.rect.x += 5
        self.rect.y += self.speed
        if self.rect.bottom > 550:
            self.rect.bottom = 550
        elif self.rect.top < 0:
            self.rect.top = 0

    def jump(self):
        self.speed = -10
        time.sleep(0.5)  # Wait for 0.5 seconds before setting the player's speed to zero
        self.speed = 0
