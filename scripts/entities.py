import pygame
import scripts.map
import constant


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


class PhysicsEntity():
    def __init__(self, assets: dict[str, "pygame.Surface | list[pygame.Surface] | Animation"], type: str, pos: tuple[int, int], size: tuple[int, int]):
        self.assets = assets
        self.type = type
        self.pos = list(pos)
        self.size = list(size)

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

        self.last_movement = [0, 0]
    
    def copy_rect(self):
        return pygame.Rect(*self.pos, *self.size)
    

    def set_action(self, action: str) -> None:
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.type + "/" + self.action].copy()


    def update(self, tilemap: "scripts.map.Tilemap", movement: tuple[int, int] = (0,0)) -> None:
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

        self.last_movement = movement


        # Velocity
        self.vel[1] = min(self.terminal_vel, self.vel[1] + constant.GRAVITY)

        # Set velocity to 0 when colliding from below or above
        if self.collision_direction["down"] or self.collision_direction["up"]:
            self.vel[1] = 0

        self.animation.update()
    

    def render(self, surf: pygame.surface.Surface, offset: tuple[int, int] = (0,0)) -> None:
        surf.blit(pygame.transform.flip(self.animation.get_image(), self.x_flip, self.y_flip), (self.pos[0] - offset[0] + self.animation_offset[0], self.pos[1] - offset[1] + self.animation_offset[1]))


class PlayerEntity(PhysicsEntity):
    def __init__(self, assets: dict[str, "pygame.Surface | list[pygame.Surface] | Animation"], pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(assets, "player", pos, size)
        self.air_time = 0
        self.jumps = 2
        self.dashing = 0
        self.wall_slide = False


    def update(self, tilemap: "scripts.map.Tilemap", movement: tuple[int, int] = (0,0)) -> None:
        super().update(tilemap, movement)

        self.air_time += 1
        if self.collision_direction["down"]:
            self.air_time = 0
            self.jumps = 2
            
        
        if(self.collision_direction["right"] or self.collision_direction["left"]) and self.air_time > 4:
            self.wall_slide = True
            self.vel[1] = min(self.vel[1], 0.5)
            if self.collision_direction["right"]:
                self.flip = False
            else:
                self.flip = True

            self.set_action("wall_slide")
        else:
            self.wall_slide = False


        if self.wall_slide == False:
            if self.air_time > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")


        if self.dashing > 0:
            self.dashing = max(0, self.dashing -1)
        elif self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        if abs(self.dashing) > 50:
            self.vel[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.vel[0] *= 0.1

        if self.vel[0] > 0:
            self.vel[0] = max(self.vel[0] - 0.1, 0)
        else:
            self.vel[0] = min(self.vel[0] + 0.1, 0)
        # TODO: Introduce constant



    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.vel[0] = 4
                self.vel[1] = -2.5
            elif not self.flip and self.last_movement[0] > 0:
                self.vel[0] = -4
                self.vel[1] = -2.5

        elif self.jumps:
            self.vel[1] = -3 
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        if not self.dashing:
            if self.x_flip:
                self.dashing = -60
            else:
                self.dashing = 60