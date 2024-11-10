import os
import pygame
import json
import constant
from constant import RGB
from scripts.entities import Animation


def load_image(path: str) -> pygame.Surface | None:
    try:
        returnable = pygame.image.load(constant.IMAGE_PATH + path).convert()
        returnable.set_colorkey(RGB.BLACK)
        return returnable
    except:
        return None


def load_images(path: str) -> list[pygame.Surface] | None:
    try:
        return [load_image(path + '/' + img_name) for img_name in os.listdir(constant.IMAGE_PATH + path)]
    except:
        return None


# Version 1.0
def load_assets(path: str) -> dict[str, pygame.Surface | list[pygame.Surface] | Animation] | None:
    assets = {}
    with open(BASE_PATH + path, "r") as file:
        data = json.load(file)
        for asset in data["assets"]:
            properties = data["assets"][asset]
            match properties["type"]:
                case "animation":
                    assets.update({asset: Animation(load_images(properties["path"]), properties["frame_duration"], properties["looping"])})
                case "folder":
                    assets.update({asset: load_images(properties["path"])})
                case "file":
                    assets.update({asset: load_image(properties["path"])})
                case "particle":
                    assets.update({asset: Animation(load_images(properties["path"]), properties["frame_duration"], properties["looping"])})
                case _:
                    raise Exception(f"Asset named \"{properties["type"]}\" is invalid.")
    
    
    return assets


# Version 1.0
def save_assets(path: str, assets: dict[str, pygame.Surface | list[pygame.Surface] | Animation]) -> None:
    if path in os.listdir(constant.BASE_PATH):
        with open(path) as file:
            data = json.load(file)


def loc_from_json(loc: str) -> tuple[int, int]:
    x, y = map(int, loc.split(','))
    return (x, y)


def loc_to_json(loc: tuple[int, int]) -> str:
    return f"{loc[0]},{loc[1]}"
