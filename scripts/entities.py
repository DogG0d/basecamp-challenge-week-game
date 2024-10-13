import pygame
from scripts.utils import Animation
import constant
import game

class PhysicsEntity():
    def __init__(self, game: "game.Game", type: str, pos: tuple[int, int], size: tuple[int, int]):
        self.game = game
        self.type = type
        self.pos = list(pos)
        self.size = size

        self.vel = [0,0]
        self.terminal_vel = 5
        self.max_walk_vel = 3

        self.collision_direction = {"up": False, "down": False, "left": False, "right": False}

        self.action = ""
        self.animation_offset = (-3, -3)
        self.x_flip = False
        self.y_flip = False
        self.animation: Animation
        self.set_action("idle")
    
    def copy_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

    def set_action(self, action: str) -> None:
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()



    def update(self, tilemap: "game.Tilemap", movement: tuple[int, int] = (0,0)) -> None:
        dif_pos = (movement[0] + self.vel[0], movement[1] + self.vel[1])
        self.collision_direction = {"up": False, "down": False, "left": False, "right": False}

        # Horizontal movement
        self.pos[0] += dif_pos[0]
        entity_rect = self.copy_rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if dif_pos[0] > 0:  # Right collision
                    entity_rect.right = rect.left
                    self.collision_direction["right"] = True
                elif dif_pos[0] < 0:  # Left collision
                    entity_rect.left = rect.right
                    self.collision_direction["left"] = True
                self.pos[0] = entity_rect.x

        # Vertical movement
        self.pos[1] += dif_pos[1]
        entity_rect = self.copy_rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if dif_pos[1] > 0:  # Bottom collision
                    entity_rect.bottom = rect.top
                    self.collision_direction["down"] = True
                elif dif_pos[1] < 0:  # Top collision
                    entity_rect.top = rect.bottom
                    self.collision_direction["up"] = True
                self.pos[1] = entity_rect.y
        
        if movement[0] > 0:
            self.x_flip = False
        elif movement[0] < 0:
            self.x_flip = True


        # Velocity
        self.vel[1] = min(self.terminal_vel, self.vel[1] + constant.GRAVITY)

        # Set velocity to 0 when colliding from below or above
        if self.collision_direction["down"] or self.collision_direction["up"]:
            self.vel[1] = 0

        self.animation.update()
    

    def render(self, surf: pygame.surface.Surface, offset: tuple[int, int] = (0,0)) -> None:
        surf.blit(pygame.transform.flip(self.animation.get_image(), self.x_flip, self.y_flip), (self.pos[0] - offset[0] + self.animation_offset[0], self.pos[1] - offset[1] + self.animation_offset[1]))


class PlayerEntity(PhysicsEntity):
    def __init__(self, game: "game.Game", pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        pass


    def update(self, tilemap: "game.Tilemap", movement: tuple[int, int] = (0,0)) -> None:
        super().update(tilemap, movement)

        self.air_time += 1
        if self.collision_direction["down"]:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action("jump")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")
