import pygame
import random


# Define obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the images and store them in a list
        self.obstacle_images = [
            pygame.image.load('obstacle1.png'),
            pygame.image.load('obstacle2.png'),
            pygame.image.load('obstacle3.png'),
            pygame.image.load('obstacle4.png'),
            pygame.image.load('obstacle5.png'),
            pygame.image.load('obstacle6.png'),
            pygame.image.load('obstacle8.png'),
        ]
        # select an image from the list randomly
        self.image = random.choice(self.obstacle_images)

        self.image = pygame.transform.scale(self.image, (50, 50))  # sprite scale
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = random.randint(0, 550)
        # set the sprites speed to a random value within the range.
        # this will handle the speed of the obstacle moving  from the right part of the window to the left
        self.speed = random.randint(2, 4)
        # Initialize the score and the is coin to 0 and false respectively
        self.scored = False
        self.is_coin = False  # this is a boolean variable that would be used to tell if
        # the player hit a coin or an obstacle

    def update(self):
        # This update handles  movement of the obstacle
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()  # the sprite is killed once it gets the end  of the window
