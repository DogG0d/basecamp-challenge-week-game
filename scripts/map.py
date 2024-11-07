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
    

    def load(self, path) -> None:
        ## Load file
        if not os.path.exists(path):
            return


        with open(path, 'r') as file:
            map_data: dict[str, any | dict] = json.load(file)

            ### Import map attributes
            self.name = map_data["name"]
            self.constants = map_data["constants"]
            self.background = map_data["background"]
            
            json_tilemap: dict[str, int | list | dict] = map_data["tilemap"]

            ## Decode tilemap
            # On grid
            on_grid = json_tilemap["on_grid"]
            decoded_on_grid = dict()
            for loc, tile in on_grid.items():
                tile["loc"] = tuple(tile["loc"])
                decoded_on_grid[loc_from_json(loc)] = tile
            
            # Off grid
            off_grid = json_tilemap["off_grid"]
            for tile in off_grid:
                tile["pos"] = tuple(tile["pos"])

            # Import tilemap attributes
            self.tilemap.tile_size = json_tilemap["tile_size"]
            self.tilemap.physics_types = json_tilemap["physics_types"]
            self.tilemap.tilemap = decoded_on_grid
            self.tilemap.offgrid_tiles = off_grid


    def save(self, path) -> None:
        with open(path, 'w') as file:
            # Encode tilemap
            encoded_tilemap = dict()
            for loc, tile in self.tilemap.tilemap.items():
                encoded_tilemap[loc_to_json(loc)] = tile


            json.dump({
                "name": self.name,
                "constants": self.constants,
                "background": self.background,
                "tilemap": {
                    "tile_size": self.tilemap.tile_size,
                    "physics_types": self.tilemap.physics_types,
                    "on_grid": encoded_tilemap,
                    "off_grid": self.tilemap.offgrid_tiles
                }
            }, file)


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
        self.tilemap[(0, 0)] = {"type": "stone", "variant": 1, "loc": (0, 0)}
    

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
            self.tilemap[tile_loc] = {"type": tile_type, "variant": tile_variant, "loc": tile_loc}
        else:
            self.offgrid_tiles.append({"type": tile_type, "variant": tile_variant, "pos": map_pos})
    

    def remove_tile(self, pos: tuple[int, int], offset: tuple[int, int]) -> None:
        tile_loc = (int((pos[0] + offset[0]) // self.tile_size), int((pos[1] + offset[1]) // self.tile_size))
        if tile_loc in self.tilemap:
            del self.tilemap[tile_loc]
            print(f"{tile_loc} removed.")
    

    def highlight_tile(self) -> None:
        pass


    def render(self, surf: pygame.Surface, assets: dict[str, pygame.Surface | list[pygame.Surface] | scripts.entities.Animation], offset: tuple[int, int] = (0,0), zoom: float = 0):
        # Zoom system
        x_zoom_comp = int(-(surf.get_width() * zoom * 0.5))
        y_zoom_comp = int(-(surf.get_height() * zoom * 0.5))

        # Render off grid tiles
        for tile in self.offgrid_tiles:
            surf.blit(assets[tile["type"]][tile["variant"]], (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))
        
        # Render on grid tiles
        for tile_x in range(int((offset[0] + x_zoom_comp) // self.tile_size), int((offset[0] + surf.get_width() - x_zoom_comp) // self.tile_size) + 1):
            for tile_y in range(int((offset[1] + y_zoom_comp) // self.tile_size), int((offset[1] + surf.get_height() - y_zoom_comp) // self.tile_size) + 1):
                loc = (tile_x, tile_y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(assets[tile["type"]][tile["variant"]], (tile["loc"][0] * self.tile_size - offset[0], tile["loc"][1] * self.tile_size - offset[1]))
