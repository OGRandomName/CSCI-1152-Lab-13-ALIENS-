import pygame
import random
import constants as C 
import pytest
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Random size between 1–4 pixels
        self.width = random.randrange(1, 4)
        self.height = self.width
        self.size = (self.width, self.height)

        # Create a surface for the star
        self.image = pygame.Surface(self.size)
        # Random color (tutorial used white, but you can make rainbow stars)
        self.color = (
            random.randrange(0, 256),
            random.randrange(0, 256),
            random.randrange(0, 256)
        )
        self.image.fill(self.color)

        # Rect for positioning
        self.rect = self.image.get_rect()
        # Random X position across the screen width
        self.rect.x = random.randrange(0, C.DISPLAY_WIDTH)
        # Start at the top
        self.rect.y = 0

        # Velocity
        self.velocity_x = 0
        self.velocity_y = random.randrange(4, 25)

    def update(self):
        # Move star down the screen
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # If star goes off bottom, reset to top
        if self.rect.y > C.DISPLAY_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(0, C.DISPLAY_WIDTH)