import pygame
import random
import math
import constants as C
import pytest
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, pattern="straight"): 
        super().__init__()
        self.image = pygame.image.load("Assets/images/enemy_4.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Spawn position
        self.rect.x = random.randint(0, C.DISPLAY_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        # Movement pattern
        self.pattern = pattern
        self.velocity_y = random.randint(3, 6)

        # Dive attack variables
        self.player = player # reference to player ship
        self.angle = 0
        self.radius = random.randint(50, 120)
        self.center_x = self.rect.x

        # --- Collision/HP setup ---
        self.hp = 3
        # Load sounds
        self.sound_hit = pygame.mixer.Sound("Assets/sound/tick1.mp3")
        self.sound_death = pygame.mixer.Sound("Assets/sound/enemy-die.ogg")

    def update(self):
        if self.pattern == "straight":
            self.rect.y += self.velocity_y
        elif self.pattern == "dive":
            target_x = self.player.rect.centerx
            self.center_x += (target_x - self.center_x) * 0.05
            self.angle += 0.08
            self.rect.x = self.center_x + int(self.radius * math.sin(self.angle))
            self.rect.y += self.velocity_y

    def get_hit(self):
        """Called when a bullet collides with this enemy."""
        self.hp -= 1
        self.sound_hit.play()
        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        """Handle enemy destruction with sound and particles."""
        self.sound_death.play()
        self.kill()
        # Later: trigger explosion animation or particle spawner