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
# Game scripts
from scripts.utils import Animation
from scripts.screens import Screen, GameScreen, EditorScreen

class Game():
    def __init__(self) -> None:
        pygame.init()

        ### Main Setup
        self.BASE_TITLE = "Challengeweek - Name Unknown"

        # Game clock
        self.clock = pygame.time.Clock()

        # Game window
        self.display = pygame.display.set_mode(DISPLAY_SIZE)
        self.is_full_screen = False
        pygame.display.set_caption(self.BASE_TITLE)

        # Game input
        self.input = InputStream()

        # Assets
        self.assets = {}
        self.assets: pygame.Surface | list[pygame.Surface] | Animation

        # Game screens
        self.screens = {}
        self.screens: dict[str, Screen]
        self.current_screen: Screen | GameScreen
        
        self.screens.update({
            "game": GameScreen(game=self),
            "editor": EditorScreen(game=self)
            })
        
        self.current_screen = self.screens.get("editor")

        
    def run(self):
        while True:
            ### Current screen render logic
            self.current_screen.render()

            ### Event grabbing
            events = pygame.event.get()
            
            ### Update keypresses
            self.input.process_input(events)

            ### Event & keypress handling

            # Quit
            if self.input.get_keyboard().is_key_pressed(pygame.K_q) or list(filter(lambda event: event.type == pygame.QUIT, events)):
                pygame.quit()
                sys.exit()

            # Resize
            if self.input.get_keyboard().is_key_pressed(pygame.K_F11):
                if self.is_full_screen:
                    pygame.display.set_mode(pygame.display.get_window_size())
                    pygame.display.set_mode(constant.DISPLAY_SIZE)
                    self.is_full_screen = False
                else:
                    pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.FULLSCREEN)
                    self.is_full_screen = True
            
            ### Current screen update logic
            self.current_screen.update()

            # FINAL Updating display
            self.display.blit(pygame.transform.scale(self.current_screen.get_screen(), self.display.get_size()), (0, 0))

            pygame.display.update()

            ### Game clock update
            self.clock.tick(constant.FRAMES_PER_SECOND)
    

    def get_assets(self) -> dict[str, pygame.Surface]:
        return self.assets
    

    def get_entities(self) -> list:
        pass
