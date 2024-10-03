# Python 3.12.6

# Game engine
import pygame
from pygame.locals import *
# Constants
import constant
from constant import RGB


### Initialize pygame
pygame.init()
pygame.font.init()

### Setup
# Clock 
clock = pygame.time.Clock()

# Screen
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Challangeweek")

# Display
frame = screen.get_rect()
camera = frame.copy()

# Text
font = pygame.font.SysFont(pygame.font.get_default_font(), 36)

# Floor
floor_list = [
    pygame.Rect(0, 800, 1600, 100),
    pygame.Rect(1700, 800, 1600, 100)
]

# Player
player = pygame.Rect(375, -1000, 50, 50)
player_vel_x = 0
player_vel_y = 0
player_new_x = player.x
player_new_y = player.y
player_collision_x = False
player_collision_y = False

dash_cooldown = constant.DASH_COOLDOWN_FRAMES

is_on_ground = False
can_double_jump = False
is_dashing = False
movement_direction = "right"

### Game loop
running = True

while running:
    ### Event handling
    for event in pygame.event.get():
        # Quiting
        if event.type == QUIT:
            running = False

    ### Handle keypresses
    keypress = pygame.key.get_pressed()

    # Player movement horizontal
    if keypress[K_LEFT]:
        movement_direction = "left"
        if player.left < 400:
            for floor in floor_list:
                floor.x += player_vel_x
        else:
            for floor in floor_list:
                player_new_x -= player_vel_x

    if keypress[K_RIGHT]:
        movement_direction = "right"
        if player.left > 1200:
            for floor in floor_list:
                floor.x -= player_vel_x
        else:
            for floor in floor_list:
                player_new_x += player_vel_x

    # Jumping and double jumping
    if keypress[K_UP] and is_on_ground:
        player_vel_y = -constant.JUMP_HEIGHT
        can_double_jump = True
    elif keypress[K_UP] and can_double_jump:
        player_vel_y = -constant.JUMP_HEIGHT
        can_double_jump = False

    # Dashing logic
    if keypress[K_e] and dash_cooldown >= constant.DASH_COOLDOWN_FRAMES and not is_dashing:
        is_dashing = True
        dash_cooldown = 0
        if movement_direction == "right":
            player_vel_x = constant.DASH_SPEED
        elif movement_direction == "left":
            player_vel_x = -constant.DASH_SPEED

    # Update dash state
    if is_dashing:
        for floor in floor_list:
            floor.x += player_vel_x * -1
        
        if player_vel_x > 0:
            player_vel_x -= 0.5
            if player_vel_x > 15:
                player_vel_y = 0
            if player_vel_x == 15:
                player_vel_x = 5

        elif player_vel_x < 0:
            player_vel_x += 0.5
            if player_vel_x < -15:
                player_vel_y = 0
            if player_vel_x == -15:
                player_vel_x = -5


    # Gravity and falling
    if not is_on_ground:
        player_vel_y = min(player_vel_y + constant.GRAVITY, constant.MAX_FALL_SPEED)
        player_new_y += player_vel_y
    else:
        player_new_y = 0

    # Floor collision
    # if player.colliderect(floor_rect):
    #     player.bottom = floor_rect.top
    #     is_on_ground = True
    # else:
    #     is_on_ground = False

    if player.collidelistall(floor_list):
        player_collision_y = True
    else:
        player_collision_y = False

    if not player_collision_x:
        player.x = player_new_x
    if not player_collision_y:
        player.y = player_new_y

    # Background and objects
    screen.fill(RGB.WHITE)

    for floor in floor_list:
        pygame.draw.rect(screen, RGB.GRAY, floor)
    
    pygame.draw.rect(screen, RGB.ORANGE, player)  # Player

    # HUD information
    text_timer = font.render(f"Time: {clock.get_time}s", True, RGB.BLACK)
    text_dashcooldown = font.render(f"Dashcooldown: {dash_cooldown}/{constant.DASH_COOLDOWN_FRAMES}", True, RGB.BLACK)
    x_velocity = font.render(f"X_Velocity: {player_vel_x:.2f}", True, RGB.BLACK)
    y_velocity = font.render(f"Y_velocity: {player_vel_y:.2f}", True, RGB.BLACK)

    # Draw HUD
    screen.blit(text_timer, (200, 500))
    screen.blit(text_dashcooldown, (200, 525))
    screen.blit(x_velocity, (200, 550))
    screen.blit(y_velocity, (200, 575))

    # Update display and clock
    pygame.display.flip()
    clock.tick(constant.FRAMES_PER_SECOND)

    # Update cooldowns
    dash_cooldown = min(dash_cooldown + 1, constant.DASH_COOLDOWN_FRAMES)
    if player_vel_x == 0:
        is_dashing = False
    
    ## DEBUG
    print()


### Cleanup and close game
pygame.quit()