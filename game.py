# Python 3.12.6

# Locals
import sys
import os
# import time
# Game engine
import pygame
# Game logics
import constant
from constant import *
from inputstream import InputStream
import sprites
# Game scripts
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from scripts.entities import PhysicsEntity
from scripts.clouds import Clouds

class Game():
    def __init__(self) -> None:
        pygame.init()
        # pygame.font.init()

        ### Setup
        # Game clock
        self.clock = pygame.time.Clock()

        # Game window
        self.display = pygame.display.set_mode(DISPLAY_SIZE)
        self.is_full_screen = False
        pygame.display.set_caption("Challangeweek - Name Unknown")

        # Game surface
        self.screen = pygame.Surface(constant.GAME_SIZE)

        # Assets
        self.assets = {  # Be careful with photos that contain a lot of black: Black is CHROMA KEYED OUT for transparency
            "player": load_image("entities/player.png"),
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "grass": load_images("tiles/grass"),
            "clouds": load_images("clouds")
        }

        # Tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        
        # Entities
        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))

        # Clouds
        self.clouds = Clouds(self.assets["clouds"], count=16)

        # Input stream
        self.input = InputStream()

        # Camera offset
        self.scroll = [0, 0]
    

    def run(self):
        while True:
            ### START Game rendering

            # Camera scroll
            self.scroll[0] += (self.player.copy_rect().centerx - self.screen.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.copy_rect().centery - self.screen.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Reset screen
            self.screen.fill(RGB.SKY_BLUE)

            # Clouds
            self.clouds.update()
            self.clouds.render(self.screen, render_scroll)

            # Tilemap
            self.tilemap.render(surf=self.screen, offset=render_scroll)

            # Entities
            self.player.render(surf=self.screen, offset=render_scroll)

            # HUD

            ### END Game rendering

            ### Event grabbing
            events = pygame.event.get()
            
            ### Update keypresses
            self.input.processInput()

            ### Event handling

            # Quit
            if self.input.isKeyPressed(pygame.K_q) or list(filter(lambda event: event.type == pygame.QUIT, events)):
                pygame.quit()
                sys.exit()
            
            ### Keypress handling

            # Resize
            if self.input.isKeyPressed(pygame.K_F11):
                if self.is_full_screen:
                    pygame.display.set_mode(pygame.display.get_window_size(), 0)
                    pygame.display.set_mode(constant.DISPLAY_SIZE, 0)
                    self.is_full_screen = False
                else:
                    pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.FULLSCREEN)
                    self.is_full_screen = True
            
            ## Player move
            move_x = move_y = 0

            # Walk right
            if self.input.isKeyDown(pygame.K_d) or self.input.isKeyDown(pygame.K_RIGHT):
                move_x += 2
            
            # Walk left
            if self.input.isKeyDown(pygame.K_a) or self.input.isKeyDown(pygame.K_LEFT):
                move_x -= 2
            
            # Jump
            if self.input.isKeyPressed(pygame.K_SPACE) or self.input.isKeyPressed(pygame.K_UP) or self.input.isKeyPressed(pygame.K_w):
                self.player.vel[1] = -constant.JUMP_HEIGHT

            ### Location updating

            self.player.update(self.tilemap, (move_x, move_y))


            # FINAL Updating display
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))

            pygame.display.update()

            ### Game clock update
            self.clock.tick(constant.FRAMES_PER_SECOND)
    

    def get_assets(self) -> dict[str, pygame.surface.Surface]:
        return self.assets


# frame = display.get_rect()
# camera = frame.copy()
# font_36 = pygame.font.SysFont(pygame.font.get_default_font(), 36)

# # Input manager
# input = InputStream()

# # Floor
# floor_group = pygame.sprite.Group()
# floor_group.add(sprites.Base(0, 800, 1600, 100, RGB.GRAY))
# floor_group.add(sprites.Base(1700, 800, 1600, 100, RGB.GRAY))
# floor_group.add(sprites.Base(1200, 700, 1600, 100, RGB.GRAY))

# # Playersdddddddd
# player_group = pygame.sprite.Group()
# player_one = sprites.Player(400, 100, 50, 50, RGB.ORANGE, constant.PLAYER_HEALTH)
# player_group.add(player_one)

# player = pygame.Rect(375, 100, 50, 50)
# player_vel_x = 0
# player_vel_y = 0
# player_new_x = player.x
# player_new_y = player.y
# player_collision_x = False
# player_collision_y = False

# dash_cooldown = constant.DASH_COOLDOWN_FRAMES

# is_on_ground = False
# can_double_jump = False
# is_dashing = False
# movement_direction = "right"