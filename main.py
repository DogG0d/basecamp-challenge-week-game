import time
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 36)

while not pygame.display.get_init():
    time.sleep(1)

# window size
screen = pygame.display.set_mode(size=(1920, 1080)) 
pygame.display.set_caption("Challangeweek")

timer = pygame.time.Clock()

FRAMES_PER_SECOND = 60
gravity = .1
player_velocity_y = 0
is_on_ground = False
jumpheight = 4
player_velocity_x = 0
player_jump_count = 0

# color
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (220, 50, 110)

player_width = 50
player_height = 50
player_x = 375 
player_y = -1000 
player_speed = 1
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)


dashing = False
runtime = True

# Main loop
while runtime:
    # check for runtime
    for event in pygame.event.get():
        if event.type == QUIT:
            runtime = False

    # timer += 1/FRAMES_PER_SECOND

    if player_velocity_y > 4:
        player_velocity_y = 4

    keypress = pygame.key.get_pressed()  # Get the state of all keyboard singular presses_pressed()
    if keypress[K_LEFT]:
        player_rect.x -= player_speed  # Move left
    if keypress[K_RIGHT]:
        player_rect.x += player_speed  # Move right
    if keypress[K_UP] and player_jump_count < 2:
        player_velocity_y -= jumpheight
        player_jump_count += 1
    if keypress[K_e] and not dashing:
        dashing = True
        if player_velocity_x > 0:
            player_velocity_x += 1
        if player_velocity_x < 0:
            player_velocity_x += 1
        else:
            pass
        dashing = False


    
    # background
    screen.fill(WHITE)

    # Floor
    floor_rect = pygame.Rect(0, 900, 1920, 100)  # x, y, width, height
    pygame.draw.rect(screen, GRAY, floor_rect)

    if player_rect.colliderect(floor_rect):
        player_rect.bottom = floor_rect.top
        is_on_ground = True
        player_jump_count = 0
    else:
        is_on_ground = False 
    
    if not is_on_ground:
        player_velocity_y += gravity 
    else:
        player_velocity_y = 0 

    player_rect.y += player_velocity_y  
    player_rect.x += player_velocity_x

    #player
    pygame.draw.rect(screen, ORANGE, player_rect)   

    text_timer = font.render(f"Time: {10}s", True, (0, 0, 0))
    text_fps = font.render(f"FPS: {timer.get_fps()}s", True, (0, 0, 0))

    screen.blit(text_timer, (200, 500))
    screen.blit(text_fps, (200, 550))
    
    # update
    pygame.display.flip()

pygame.quit()