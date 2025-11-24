import pygame
import random
import constants as C
from source.star import Star
import pytest

class BG(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Background surface (same size as display)
        self.image = pygame.Surface(C.DISPLAY_SIZE)
        # Slightly bluish black background
        self.color = (0, 0, 15)
        self.image.fill(self.color)

        # Rect for positioning
        self.rect = self.image.get_rect()

        # Group to hold stars
        self.stars = pygame.sprite.Group()

        # Timer for spawning stars
        self.timer = random.randrange(1, 10)

    def update(self):
        # Update all stars
        self.stars.update()

        # Spawn new star when timer hits zero
        if self.timer == 0:
            new_star = Star()
            self.stars.add(new_star)
            # Reset timer to a new random value
            self.timer = random.randrange(1, 10)
        else:
            self.timer -= 1

        # Clear background each frame
        self.image.fill(self.color)

        # Draw stars onto background surface
        self.stars.draw(self.image)