import pygame
import random
from source.enemy import Enemy
import constants as C
import pytest

class EnemySpawner:
    def __init__(self, player):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = random.randint(30, 120)
        self.player = player  # reference to player for dive patterns

    def update(self):
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = random.randint(60, 150)  # reset timer

        self.enemy_group.update()

    def spawn_enemy(self):
        # Decide whether to spawn a single enemy or a formation
        formations = ["single", "vshape", "grid", "line"]
        choice = random.choice(formations)

        if choice == "single":
            # Pick a random movement pattern
            patterns = ["straight", "dive", "zigzag", "wave", "spiral", "diagonal"]
            pattern = random.choice(patterns)
            new_enemy = Enemy(self.player, pattern=pattern)
            self.enemy_group.add(new_enemy)

        elif choice == "vshape":
            self.spawn_vshape()

        elif choice == "grid":
            self.spawn_grid()

        elif choice == "line":
            self.spawn_line()

    def spawn_vshape(self):
        center_x = C.DISPLAY_WIDTH // 2
        start_y = -40
        spacing = 40
        for i in range(5):
            # Left side
            enemy_left = Enemy(self.player, pattern="straight")
            enemy_left.rect.topleft = (center_x - i * spacing, start_y - i * spacing)
            self.enemy_group.add(enemy_left)

            # Right side
            enemy_right = Enemy(self.player, pattern="straight")
            enemy_right.rect.topleft = (center_x + i * spacing, start_y - i * spacing)
            self.enemy_group.add(enemy_right)

    def spawn_grid(self):
        rows, cols = 3, 6
        spacing_x, spacing_y = 60, 50
        start_x, start_y = 100, -150
        for row in range(rows):
            for col in range(cols):
                enemy = Enemy(self.player, pattern="zigzag")
                enemy.rect.topleft = (start_x + col * spacing_x, start_y + row * spacing_y)
                self.enemy_group.add(enemy)

    def spawn_line(self):
        spacing = 80
        start_y = -50
        for i in range(8):
            enemy = Enemy(self.player, pattern="wave")
            enemy.rect.topleft = (i * spacing, start_y)
            self.enemy_group.add(enemy)

    def draw(self, surface):
        self.enemy_group.draw(surface)