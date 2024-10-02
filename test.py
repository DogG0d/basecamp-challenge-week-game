import time
import pygame
from pygame.locals import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int], pos: tuple[int, int], color: tuple[int, int, int]) -> None:
        print("Sprite created")
        pygame.sprite.Sprite.__init__(self= self)

        self.image = pygame.Surface(pos[0], pos[1], size)
        self.image.fill(color)

        self.image.get_rect()
    

    def update():
        pass


# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
FRAMES_PER_SECOND = 60
GRAVITY = 1
JUMP_HEIGHT = 20
PLAYER_SPEED = 10
MAX_FALL_SPEED = 10
DASH_SPEED = 25
DASH_DECAY = 0.5
DASH_COOLDOWN_FRAMES = 120

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
ORANGE = (220, 50, 110)

# Screen Setup
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Challangeweek")
font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
clock = pygame.time.Clock()
frame = screen.get_rect()
camera = frame.copy()



# Player Variables

player_rect = pygame.Rect(375, -1000, 50, 50)

floor = pygame.Rect(0, 800, 1600, 100)
floor2 = pygame.Rect(1700, 800, 1600, 100)

floor_list = [floor, floor2]

test = ((screen, GRAY, pygame.Rect(1610, 800, 1600, 100)),(screen, GRAY, pygame.Rect(0, 800, 1600, 100)))

player_rect = pygame.Rect(375, -1000, 50, 50)
player_velocity_x = 0
player_velocity_y = 0
is_on_ground = False
can_double_jump = False
dashing = False
dash_cooldown = DASH_COOLDOWN_FRAMES
movement_direction = "right"

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Handle keypresses
    keypress = pygame.key.get_pressed()

    # Player movement - horizontal
    if keypress[K_LEFT]:
        movement_direction = "left"
        if player_rect.left < 400:
            for rect in floor_list:
                rect.x += PLAYER_SPEED
        else:
            player_rect.x -= PLAYER_SPEED

    if keypress[K_RIGHT]:
        movement_direction = "right"
        if player_rect.left > 1200:
            for rect in floor_list:
                rect.x -= PLAYER_SPEED
        else:
            player_rect.x += PLAYER_SPEED

    # Jumping and double jumping
    if keypress[K_UP] and is_on_ground:
        player_velocity_y = -JUMP_HEIGHT
        can_double_jump = True
    elif keypress[K_UP] and can_double_jump:
        player_velocity_y = -JUMP_HEIGHT
        can_double_jump = False

    # Dashing logic
    if keypress[K_e] and dash_cooldown >= DASH_COOLDOWN_FRAMES and not dashing:
        dashing = True
        dash_cooldown = 0
        if movement_direction == "right":
            player_velocity_x = DASH_SPEED
        elif movement_direction == "left":
            player_velocity_x = -DASH_SPEED

    # Update dash state
    if dashing:
        for rect in floor_list:
            rect.x += (player_velocity_x * -1)
        if player_velocity_x > 0:
            player_velocity_x -= 0.5
            if player_velocity_x > 15:
                player_velocity_y = 0
            if player_velocity_x == 15:
                player_velocity_x = 5

        elif player_velocity_x < 0:
            player_velocity_x += 0.5
            if player_velocity_x < -15:
                player_velocity_y = 0
            if player_velocity_x == -15:
                player_velocity_x = -5


    # Gravity and falling
    if not is_on_ground:
        player_velocity_y = min(player_velocity_y + GRAVITY, MAX_FALL_SPEED)
        player_rect.y += player_velocity_y
    else:
        player_velocity_y = 0

    # Floor collision
    if player_rect.collidelist(floor_list):
        player_rect.bottom = floor_list[player_rect.collidelist(floor_list)].top
        is_on_ground = True
    
    print(is_on_ground)

    # Background and objects
    screen.fill(WHITE)
    pygame.draw.rect(screen, ORANGE, player_rect)  # Player

    for floor_rect in floor_list:
        pygame.draw.rect(screen, GRAY, floor_rect)  # Floor


    # HUD information
    text_timer = font.render(f"Time: {10}s", True, (0, 0, 0))
    text_dashcooldown = font.render(f"Dashcooldown: {dash_cooldown}/{DASH_COOLDOWN_FRAMES}", True, (0, 0, 0))
    x_velocity = font.render(f"X_Velocity: {player_velocity_x:.2f}", True, (0, 0, 0))
    y_velocity = font.render(f"Y_velocity: {player_velocity_y:.2f}", True, (0, 0, 0))

    # Draw HUD
    screen.blit(text_timer, (200, 500))
    screen.blit(text_dashcooldown, (200, 525))
    screen.blit(x_velocity, (200, 550))
    screen.blit(y_velocity, (200, 575))

    # Update display and clock
    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)

    # Update cooldowns
    dash_cooldown = min(dash_cooldown + 1, DASH_COOLDOWN_FRAMES)
    if player_velocity_x == 0:
        dashing = False
    
# Quit pygame
pygame.quit()