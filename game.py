# Python 3.12.6

# Locals
import sys
# import time
# Game engine
import pygame
# Game logics
import constant
from constant import *
from inputstream import InputStream
import sprites
from scripts.clouds import Clouds

class Game():
    def __init__(self) -> None:
        pygame.init()
        # pygame.font.init()

        ### Setup
        # Game clock
        self.clock = pygame.time.Clock()

        # Display
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Challangeweek - Name Unknown")
            "grass": load_images("tiles/grass"),
            "clouds": load_images("clouds")
        # Clouds
        self.clouds = Clouds(self.assets["clouds"], count=16)
    

    def run(self):
        while True:
            # Clouds
            self.clouds.update()
            self.clouds.render(self.screen, render_scroll)
            pygame.display.update()
            self.clock.tick(constant.FRAMES_PER_SECOND)

            # Update cooldowns
            dash_cooldown = min(dash_cooldown + 1, constant.DASH_COOLDOWN_FRAMES)
            if player_one.vel_x == 0:
                is_dashing = False
            
            ## DEBUG
            # print()


# frame = display.get_rect()
# camera = frame.copy()
font_36 = pygame.font.SysFont(pygame.font.get_default_font(), 36)

# Input manager
input = InputStream()

# Floor
floor_group = pygame.sprite.Group()
floor_group.add(sprites.Base(0, 800, 1600, 100, RGB.GRAY))
floor_group.add(sprites.Base(1700, 800, 1600, 100, RGB.GRAY))
floor_group.add(sprites.Base(1200, 700, 1600, 100, RGB.GRAY))

# Playersdddddddd
player_group = pygame.sprite.Group()
player_one = sprites.Player(400, 100, 50, 50, RGB.ORANGE, constant.PLAYER_HEALTH)
player_group.add(player_one)

# player = pygame.Rect(375, 100, 50, 50)
# player_vel_x = 0
# player_vel_y = 0
# player_new_x = player.x
# player_new_y = player.y
# player_collision_x = False
# player_collision_y = False

dash_cooldown = constant.DASH_COOLDOWN_FRAMES

is_on_ground = False
can_double_jump = False
is_dashing = False
movement_direction = "right"

