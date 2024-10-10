import pygame
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
        self.collision_direction = {"up": False, "down": False, "left": False, "right": False}
    
    def copy_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap: "game.Tilemap", movement: tuple[int, int] = (0,0)):
        dif_pos = (movement[0] + self.vel[0], movement[1] + self.vel[1])
        self.collision_direction = {"up": False, "down": False, "left": False, "right": False}

        self.pos[0] += dif_pos[0]
        entity_rect = self.copy_rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if dif_pos[0] > 0:  # Right collision
                    entity_rect.right = rect.left
                    self.collision_direction["right"] = True
                if dif_pos[0] < 0:  # Left collision
                    entity_rect.left = rect.right
                    self.collision_direction["left"] = True
                self.pos[0] = entity_rect.x


        self.pos[1] += dif_pos[1]
        entity_rect = self.copy_rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if dif_pos[1] > 0:  # Bottom collision
                    entity_rect.bottom = rect.top
                    self.collision_direction["down"] = True
                if dif_pos[1] < 0:  # Top collision
                    entity_rect.top = rect.bottom
                    self.collision_direction["up"] = True
                self.pos[1] = entity_rect.y
        
        self.vel[1] = min(self.terminal_vel, self.vel[1] + constant.GRAVITY)

        if self.collision_direction["down"] or self.collision_direction["up"]:
            self.vel[1] = 0
    

    def render(self, surf: pygame.surface.Surface, offset: tuple[int, int] = (0,0)):
        surf.blit(self.game.get_assets()['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class PlayerEntity():
    def __init__(self):
        pass