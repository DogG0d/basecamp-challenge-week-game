import pygame
import game

NEIGHBOUR_OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass", "stone"}

class Tilemap():
    def __init__(self, game: "game.Game", tile_size: int = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.game

        ### Test map generator
        # for i in range(10):
        #     self.tilemap[f"{3 + i};10"] = {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
        #     self.tilemap[f"10;{5 + i}"] = {"type": "stone", "variant": 1, "pos": (10, 5 + i)}
    
    def get_tiles_around(self, pos: tuple[int, int]) -> list[dict]:
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOUR_OFFSETS:
            if (check_loc := f"{tile_loc[0] + offset[0]};{tile_loc[1] + offset[1]}") in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        
        return tiles


    def physics_rect_around(self, pos: tuple[int, int]) -> list[pygame.Rect]:
        rects = []
        for tile in self.get_tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects


    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0,0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.get_assets()[tile["type"]][tile["variant"]], (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

        for tile_x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for tile_y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = f"{tile_x};{tile_y}"
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.get_assets()[tile["type"]][tile["variant"]], (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))
