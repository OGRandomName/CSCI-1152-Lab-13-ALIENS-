import pygame
import constants as C
import pytest
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Assets/images/laserBlast.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8

        # Bullet speed (negative because it moves upward)
        self.speed = -8

    def update(self):
        # Move bullet upward
        self.rect.y += self.speed

        # Remove bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()