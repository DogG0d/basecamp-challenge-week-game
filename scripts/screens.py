import pygame
import game
from scripts.clouds import Clouds
from scripts.entities import PlayerEntity
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation
import constant
from constant import RGB

class Screen:
    def __init__(self, game: "game.Game", screen_size: tuple[int, int] = constant.GAME_SIZE):
        self.game = game
        self.assets = {}
        self.screen_size = screen_size
        self.screen = pygame.Surface(screen_size)

        ### Setup
        # Input stream
        self.input = self.game.input
    

    def render(self) -> None:
        pass


    def update(self) -> None:
        pass


    def get_screen(self) -> pygame.Surface:
        return self.screen
    

    def get_assets(self) -> dict[str, pygame.Surface | list[pygame.Surface] | Animation]:
        return self.assets
    

    def get_render_scale(self) -> float:
        return constant.DISPLAY_SIZE / self.screen_size
        

class GameScreen(Screen):
    def __init__(self, game: "game.Game", screen_size: tuple[int, int] = constant.GAME_SIZE):
        super().__init__(game=game, screen_size=screen_size)
        
        ### Setup
        pygame.display.set_caption(self.game.BASE_TITLE)
        
        # Assets
        self.assets = {
            "player": load_image("entities/player.png"),
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "grass": load_images("tiles/grass"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("entities/player/idle"), 6),
            "player/run": Animation(load_images("entities/player/run"), 4),
            "player/jump": Animation(load_images("entities/player/jump")),
            "player/slide": Animation(load_images("entities/player/slide")),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide"))
        }

        # Tilemap
        self.tilemap = Tilemap(self.game, tile_size=16)
        
        # Entities
        self.player = PlayerEntity(self.game, (50, 50), (8, 15))
        self.movement = [0, 0]

        # Clouds
        self.clouds = Clouds(self.game.assets["clouds"], count=16)

        # Camera offset
        self.scroll = [0, 0]


    def render(self):
        # Camera scroll
        self.scroll[0] += (self.player.copy_rect().centerx - self.screen.get_width() / 2 - self.scroll[0]) / 20
        self.scroll[1] += (self.player.copy_rect().centery - self.screen.get_height() / 2 - self.scroll[1]) / 20
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
        ...
    

    def update(self):
        ## Player move
        self.movement = [0, 0]

        # Walk right
        if self.input.get_keyboard().any_key_down([pygame.K_d, pygame.K_RIGHT]):
            self.movement[0] += 2
        
        # Walk left
        if self.input.get_keyboard().any_key_down([pygame.K_a, pygame.K_LEFT]):
            self.movement[0] -= 2
        
        # Jump
        if self.input.get_keyboard().any_key_pressed([pygame.K_w, pygame.K_SPACE, pygame.K_UP]):
            self.player.vel[1] = -constant.JUMP_HEIGHT

        ## Location updating

        self.player.update(self.tilemap, self.movement)


class EditorScreen(Screen):
    def __init__(self, game: "game.Game", screen_size: tuple[int, int] = constant.GAME_SIZE):
        super().__init__(game=game, screen_size=screen_size)

        ### Setup
        pygame.display.set_caption(self.game.BASE_TITLE + " - Editor")

        # Assets
        self.assets = {
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "grass": load_images("tiles/grass")
        }

        # Tilemap
        self.tilemap = Tilemap(self.game, tile_size=16)
        
        self.tile_list = list(self.game.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Camera movement
        self.scroll = [0, 0]
        self.movement = [0, 0]

    def render(self):
        # Camera scroll
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        # Reset screen
        self.screen.fill(RGB.WHITE)

        # Tilemap
        self.tilemap.render(surf=self.screen, offset=render_scroll)

        # HUD
        ...
    

    def update(self):
        ## Screen move
        self.movement = [0, 0]

        current_tile_img = self.game.assets[self.tile_list[self.tile_group]][self.tile_variant]
        current_tile_img.set_alpha(100)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] / self.get_render_scale(), mouse_pos[1] / self.get_render_scale())
        tile_pos = ((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size, (mouse_pos[1] + self.scroll[1])  // self.tilemap.tile_size)
        
        current_tile_img: pygame.Surface
        if self.input.get_keyboard().any_key_down([pygame.K_LSHIFT, pygame.K_RSHIFT]):
            if self.input.get_mouse().is_scrolling_up():
                self.tile_variant = (self.tile_variant - 1) % len(self.game.assets[self.tile_list[self.tile_group]])
            if self.input.get_mouse().is_scrolling_down():
                self.tile_variant = (self.tile_variant + 1) % len(self.game.assets[self.tile_list[self.tile_group]])
        else:
            if self.input.get_mouse().is_scrolling_up():
                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                self.tile_variant = 0
            if self.input.get_mouse().is_scrolling_down():
                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                self.tile_variant = 0
        
        self.screen.blit(current_tile_img, (5, 5))





        # Move right
        if self.input.get_keyboard().any_key_down([pygame.K_d, pygame.K_RIGHT]):
            self.movement[0] += 2
        
        # Walk left
        if self.input.get_keyboard().any_key_down([pygame.K_a, pygame.K_LEFT]):
            self.movement[0] -= 2
        
        # Walk down
        if self.input.get_keyboard().any_key_down([pygame.K_s, pygame.K_DOWN]):
            self.movement[1] += 2
        
        # Walk up
        if self.input.get_keyboard().any_key_down([pygame.K_w, pygame.K_UP]):
            self.movement[1] -= 2

        ## Location updating
