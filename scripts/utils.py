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


class Animation:
    def __init__(self, images: list[pygame.Surface], frame_duration: int = 5, looping: bool = True):
        self.images = images
        self.looping = looping
        self.duration = frame_duration
        self.finished = False
        self.frame = 0
    

    def copy(self) -> "Animation":
        return Animation(self.images, self.duration, self.looping)
    
    def update(self):
        if self.looping:
            self.frame = (self.frame + 1) % (self.duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.duration * len(self.images) - 1)
            if self.frame == self.duration * len(self.images) - 1:
                self.finished = True

    def get_image(self):
        return self.images[int(self.frame / self.duration)]


