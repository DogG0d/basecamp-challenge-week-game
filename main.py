import time
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 36)

while not pygame.display.get_init():
    time.sleep(1)

# window size
screen = pygame.display.set_mode(size=(1600, 900)) 
pygame.display.set_caption("Challangeweek")

clock = pygame.time.Clock()

dashing = False


FRAMES_PER_SECOND = 60
gravity = 1
player_velocity_y = 0
is_on_ground = False
jumpheight = 10
player_velocity_x = 0
Can_Double_Jump = 0

# color
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (220, 50, 110)

player_width = 50
player_height = 50
player_x = 375 
player_y = -1000 
player_speed = 10
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# COOLDOWNS
Dashcooldown = 0



runtime = True

# Main loop
while runtime:

    # check for runtime
    for event in pygame.event.get():
        if event.type == QUIT:
            runtime = False

    # timer += 1/FRAMES_PER_SECOND

    if player_velocity_y > 10:
        player_velocity_y = 10

    keypress = pygame.key.get_pressed()  # Get the state of all keyboard singular presses_pressed()
    if keypress[K_LEFT]:
        player_rect.x -= player_speed  # Move left
    if keypress[K_RIGHT]:
        player_rect.x += player_speed  # Move right
    if keypress[K_UP]:
        if is_on_ground:
            player_velocity_y -= jumpheight
            Can_Double_Jump = True
        elif Can_Double_Jump:
            player_velocity_y -= jumpheight
            Can_Double_Jump = False

    if keypress[K_e] and not dashing:
        if keypress[K_RIGHT]:
            dashing = True
            Dashcooldown = 0
            player_velocity_x = player_speed + 20
        if keypress[K_LEFT]:
            dashing = True
            Dashcooldown = 0
            player_velocity_x = (player_speed + 20) * -1


    #update player dash location
    if dashing:
        player_rect.x += player_velocity_x
        if player_velocity_x > 0:
            player_velocity_x -= 0.5
            if player_velocity_x == 15:
                player_velocity_x = 5
        
        elif player_velocity_x < 0:
            player_velocity_x += 0.5
            if player_velocity_x == -15:
                player_velocity_x = -5


    
    # background
    screen.fill(WHITE)

    # Floor
    floor_rect = pygame.Rect(0, 800, 1600, 100)  # x, y, width, height
    pygame.draw.rect(screen, GRAY, floor_rect)

    if player_rect.colliderect(floor_rect):
        player_rect.bottom = floor_rect.top
        is_on_ground = True
    else:
        is_on_ground = False 
    
    if not is_on_ground:
        player_velocity_y += gravity
        player_rect.y += player_velocity_y 
    else:
        player_velocity_y = 0 



    #player
    pygame.draw.rect(screen, ORANGE, player_rect)   

    text_timer = font.render(f"Time: {10}s", True, (0, 0, 0))
    text_dashcooldown = font.render(f"Dashcooldown: {Dashcooldown}/120", True, (0, 0, 0))
    X_veloc = font.render(f"X_Velocity: {player_velocity_x}", True, (0, 0, 0))
    Y_veloc = font.render(f"Y_velocity: {player_velocity_y}", True, (0, 0, 0))


    screen.blit(text_timer, (200, 500))
    screen.blit(text_dashcooldown, (200, 525))
    screen.blit(X_veloc, (200, 550))
    screen.blit(Y_veloc, (200, 575))
    

    
    # update
    pygame.display.flip()
    clock.tick(60)

    # ADD ALL COOLDOWNS
    Dashcooldown += 1
    if Dashcooldown > 120:
        dashing = False


pygame.quit()