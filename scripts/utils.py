import os
import pygame
from constant import RGB

BASE_IMAGE_PATH = 'data/images/'


def load_image(path) -> pygame.Surface | None:
    try:
        returnable = pygame.image.load(BASE_IMAGE_PATH + path).convert()
        returnable.set_colorkey(RGB.BLACK)
        return returnable
    except:
        return None


def load_images(path) -> list[pygame.Surface] | None:
    try:
        return [load_image(path + '/' + img_name) for img_name in os.listdir(BASE_IMAGE_PATH + path)]
    except:
        return None