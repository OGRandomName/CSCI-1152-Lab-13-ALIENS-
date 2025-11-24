import pygame
import constants as C
from source.bullet import Bullet
import pytest

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # --- Load ship image ---
        self.image = pygame.image.load("Assets/images/ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = C.DISPLAY_WIDTH // 2
        self.rect.bottom = C.DISPLAY_HEIGHT - 10

        # --- Movement ---
        self.speed = 5
        self.bullets = pygame.sprite.Group()

        # --- Shooting cooldown ---
        self.last_shot_time = 0
        self.shot_delay = 180  # ms between bullets

        # --- Sounds ---
        self.laser_sound = pygame.mixer.Sound("Assets/sound/laser.mp3")
        self.laser_sound.set_volume(1.0)

        self.impact_sound = pygame.mixer.Sound("Assets/sound/impactSound.mp3")
        self.impact_sound.set_volume(1.0)

        # --- Lives ---
        self.lives = 1  # or more if you want multiple hits before game over

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # --- Boundary checks ---
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > C.DISPLAY_WIDTH:
            self.rect.right = C.DISPLAY_WIDTH

        # --- Bullet firing with cooldown ---
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Update bullets
        self.bullets.update()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot_time = current_time
            self.laser_sound.play()

    def handle_volume_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:   # ` key
                self.laser_sound.set_volume(0.0)
                self.impact_sound.set_volume(0.0)
            elif event.key == pygame.K_1:
                self.set_volume(0.1)
            elif event.key == pygame.K_2:
                self.set_volume(0.2)
            elif event.key == pygame.K_3:
                self.set_volume(0.3)
            elif event.key == pygame.K_4:
                self.set_volume(0.4)
            elif event.key == pygame.K_5:
                self.set_volume(0.5)
            elif event.key == pygame.K_6:
                self.set_volume(0.6)
            elif event.key == pygame.K_7:
                self.set_volume(0.7)
            elif event.key == pygame.K_8:
                self.set_volume(0.8)
            elif event.key == pygame.K_9:
                self.set_volume(0.9)
            elif event.key == pygame.K_0:
                self.set_volume(1.0)

    def set_volume(self, value):
        self.laser_sound.set_volume(value)
        self.impact_sound.set_volume(value)

    def get_volume_percent(self):
        return int(self.laser_sound.get_volume() * 100)

    def die(self):
        """Called when an enemy collides with the ship."""
        self.impact_sound.play()
        self.lives -= 1
        if self.lives <= 0:
            self.kill()
            return True  # signal game over
        return False