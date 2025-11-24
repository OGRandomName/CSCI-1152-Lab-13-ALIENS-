import pygame
from source.ship import Ship
import constants as C
from source.background import BG
from source.enemyspawner import EnemySpawner
import pytest

def main(screen_width, screen_height):
    pygame.init()
    pygame.mixer.init()
    display = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Game")

    # --- Background music setup ---
    pygame.mixer.music.load("Assets/sound/background.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, fade_ms=2000)

    fps = 60
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    # --- Helper functions ---
    def restart_game(screen_width, screen_height):
        main(screen_width, screen_height)

    def game_over_screen(display, font, screen_width, screen_height):
        countdown = 3
        while countdown > 0:
            display.fill((0, 0, 0))
            text_surface = font.render(f"GAME OVER - Restarting in {countdown}", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            display.blit(text_surface, text_rect)
            pygame.display.update()
            pygame.time.delay(1000)
            countdown -= 1

    # --- Sprite setup ---
    bg = BG()
    bg_group = pygame.sprite.Group(bg)

    player = Ship()
    sprite_group = pygame.sprite.Group(player)

    enemy_spawner = EnemySpawner(player)
    sprite_group.add(enemy_spawner.enemy_group)

    # --- Main loop ---
    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_volume_keys(event)

        # --- Update objects ---
        bg_group.update()
        sprite_group.update()
        enemy_spawner.update()

        # --- Restart conditions ---
        # 1. Enemy hits bottom
        for enemy in enemy_spawner.enemy_group:
            if enemy.rect.bottom >= screen_height:
                player.impact_sound.play()
                game_over_screen(display, font, screen_width, screen_height)
                return restart_game(screen_width, screen_height)

        # 2. Enemy collides with player
        player_hits = pygame.sprite.spritecollide(player, enemy_spawner.enemy_group, False)
        if player_hits:
            if player.die():  # plays impact sound and signals game over
                game_over_screen(display, font, screen_width, screen_height)
                return restart_game(screen_width, screen_height)

        # --- Bullet vs Enemy collisions ---
        collided = pygame.sprite.groupcollide(
            player.bullets,
            enemy_spawner.enemy_group,
            True,   # kill bullet
            False   # don't auto-kill enemy
        )
        for bullet, enemies_hit in collided.items():
            for enemy in enemies_hit:
                enemy.get_hit()

        # --- Drawing ---
        display.fill((0, 0, 0))
        bg_group.draw(display)
        sprite_group.draw(display)
        enemy_spawner.draw(display)
        player.bullets.draw(display)

        # --- HUD overlay ---
        volume_text = f"Volume: {player.get_volume_percent()}%"
        text_surface = font.render(volume_text, True, (255, 255, 255))
        display.blit(text_surface, (10, 10))

        pygame.display.update()

    # Smooth fade-out when quitting
    pygame.mixer.music.fadeout(3000)
    pygame.quit()

if __name__ == "__main__":
    main(C.DISPLAY_WIDTH, C.DISPLAY_HEIGHT)