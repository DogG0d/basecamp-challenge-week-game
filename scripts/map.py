import pygame
import os
import json
import scripts.entities
from scripts.utils import loc_from_json, loc_to_json

NEIGHBOUR_OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

class Map():
    def __init__(self, name: str, tilesize: int = 16, path: str = None) -> None:
        self.name = name
        self.tilemap = Tilemap(tilesize)
        self.path = path
        self.constants = {}
        self.background = {}
        if path is not None:
            self.load(path)
    

    def load(self, path):
        ## Load file
        file = open(path, 'r')
        map_data: dict[str, any | dict] = json.load(file) 
        file.close()

        ### Import map attributes
        self.name = map_data["name"]
        self.constants = map_data["constants"]
        self.background = map_data["background"]
        
        json_tilemap: dict[str, int | list | dict] = map_data["tilemap"]

        ## Decode tilemap
        # On grid
        for loc in json_tilemap["on_grid"]:
            json_tilemap[loc_from_json(loc)] = json_tilemap["on_grid"].pop(loc)
        
        # Off grid
        for loc in json_tilemap["off_grid"]:
            loc["loc"] = tuple(loc["loc"])

        # Import tilemap attributes
        self.tilemap.tile_size = json_tilemap["tile_size"]
        self.tilemap.tilemap = json_tilemap["on_grid"]
        self.tilemap.offgrid_tiles = json_tilemap["off_grid"]


    def save(self, path):
        file = open(path, 'w')

        # Encode tilemap
        encoded_tilemap = dict()
        for loc, tile in self.tilemap.tilemap.items():
            encoded_tilemap[loc_to_json(loc)] = tile


        json.dump({
            "name": self.name,
            "constants": self.constants,
            "background": self.background,
            "tilemap": {
                "tilesize": self.tilemap.tile_size,
                "on_grid": encoded_tilemap,
                "off_grid": self.tilemap.offgrid_tiles
            }
        }, file)

        file.close()

        if not os.path.exists(path):
            return



class Tilemap():
    def __init__(self, tile_size: int = 16):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.physics_types = ["grass", "stone"]

        ### Test map generator
        # for i in range(10):
        #     self.tilemap[(3 + i, 10)] = {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
        #     self.tilemap[(10, 5 + i)] = {"type": "stone", "variant": 1, "pos": (10, 5 + i)}
        
        # Middle block
        self.tilemap[(0, 0)] = {"type": "stone", "variant": 1, "pos": (0, 0)}
    

    def get_tiles_around(self, pos: tuple[int, int]) -> list[dict]:
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOUR_OFFSETS:
            check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles


    def physics_rect_around(self, pos: tuple[int, int]) -> list[pygame.Rect]:
        rects = []
        for tile in self.get_tiles_around(pos):
            if tile["type"] in self.physics_types:
                rects.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    

    def add_tile(self, pos: tuple[int, int], offset: tuple[int, int], tile_type: str, tile_variant: int, is_on_grid: bool = True) -> None:
        map_pos = (pos[0] + offset[0], pos[1] + offset[1])

        if is_on_grid:
            tile_loc = (int(map_pos[0] // self.tile_size), int(map_pos[1] // self.tile_size))
            self.tilemap[tile_loc] = {"type": tile_type, "variant": tile_variant, "pos": tile_loc}
        else:
            self.offgrid_tiles.append({"type": tile_type, "variant": tile_variant, "pos": map_pos})
    

    def remove_tile(self, pos: tuple[int, int], offset: tuple[int, int]) -> None:
        tile_loc = (int((pos[0] + offset[0]) // self.tile_size), int((pos[1] + offset[1]) // self.tile_size))
        self.tilemap.pop(tile_loc)
    

    def highlight_tile(self) -> None:
        pass


    def render(self, surf: pygame.Surface, assets: dict[str, pygame.Surface | list[pygame.Surface] | scripts.entities.Animation], offset: tuple[int, int] = (0,0), zoom: float = 0):
        x_zoom_comp = int(-(surf.get_width() * zoom * 0.5))
        y_zoom_comp = int(-(surf.get_height() * zoom * 0.5))

        for tile in self.offgrid_tiles:
            surf.blit(assets[tile["type"]][tile["variant"]], (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

        for tile_x in range(int((offset[0] + x_zoom_comp) // self.tile_size), int((offset[0] + surf.get_width() - x_zoom_comp) // self.tile_size) + 1):
            for tile_y in range(int((offset[1] + y_zoom_comp) // self.tile_size), int((offset[1] + surf.get_height() - y_zoom_comp) // self.tile_size) + 1):
                loc = (tile_x, tile_y)
                if loc in self.tilemap:
                    tile = self.tilemap.get(loc)
                    surf.blit(assets[tile["type"]][tile["variant"]], (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))
