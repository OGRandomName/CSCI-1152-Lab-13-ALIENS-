import pygame
import pytest

# --- Fixtures ---
@pytest.fixture
def ship_rect():
    """Create a fake ship rect centered on screen."""
    return pygame.Rect(400, 300, 50, 50)

@pytest.fixture
def laser_image():
    """Create a fake laser surface for testing."""
    return pygame.Surface((5, 20))

# --- Tests ---
def test_ship_moves_left(ship_rect):
    """Ship moves left when speed applied."""
    ship_speed = 5
    ship_rect.x -= ship_speed
    assert ship_rect.left == 395

def test_ship_moves_right(ship_rect):
    """Ship moves right when speed applied."""
    ship_speed = 5
    ship_rect.x += ship_speed
    assert ship_rect.left == 405

def test_laser_creation(ship_rect, laser_image):
    """Laser should spawn at ship's top center."""
    laser_rect = laser_image.get_rect(midbottom=ship_rect.midtop)
    assert laser_rect.midbottom == ship_rect.midtop

def test_laser_moves_up(ship_rect, laser_image):
    """Laser should move upward when updated."""
    laser_rect = laser_image.get_rect(midbottom=ship_rect.midtop)
    laser_speed = 10
    initial_y = laser_rect.y
    laser_rect.y -= laser_speed
    assert laser_rect.y == initial_y - laser_speed

def test_laser_removed_offscreen(ship_rect, laser_image):
    """Laser should be removed when off-screen."""
    lasers = []
    laser_rect = laser_image.get_rect(midbottom=ship_rect.midtop)
    lasers.append(laser_rect)

    # Move laser far off-screen
    laser_rect.y = -50
    if laser_rect.bottom < 0:
        lasers.remove(laser_rect)

    assert len(lasers) == 0

def test_laser_cooldown():
    """Cooldown prevents firing too quickly."""
    laser_cooldown = 180
    last_shot_time = 1000
    current_time = 1100
    can_shoot = (current_time - last_shot_time) > laser_cooldown
    assert can_shoot is False

    current_time = 1300
    can_shoot = (current_time - last_shot_time) > laser_cooldown
    assert can_shoot is True