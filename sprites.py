import pygame
import constant

class WorldObject(pygame.sprite.Sprite):
  def __init__(self, x:int=None, y:int=None, w:int=constant.PLAYER_WIDTH, h:int=constant.PLAYER_HEIGHT, color:tuple[int,int,int]=constant.RGB.BLACK) -> None:
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface([w,h])
    self.image.fill(color)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  

  def update(self, dx:int=0, dy:int=0):
    super().update(self)
    self.rect.x += dx
    self.rect.y += dy


  def get_rect(self) -> pygame.rect.Rect:
    return self.rect


class Entity(WorldObject):
  def __init__(self, x: int = None, y: int = None, w: int = constant.PLAYER_WIDTH, h: int = constant.PLAYER_HEIGHT, color: tuple[int, int, int] = constant.RGB.BLACK, gravity: float = constant.GRAVITY) -> None:
    super().__init__(x, y, w, h, color)
    self.gravity = gravity
  

  def update(self): # Add physics system in here
    pass
  



class Player(Entity):
  vel_x = 10
  vel_y = 0
  flying_velocity_multiplier = 1.0
  direction = None
  on_ground = False

  def __init__(self, x:int=None, y:int=None, w:int=constant.PLAYER_WIDTH, h:int=constant.PLAYER_HEIGHT, color:tuple[int,int,int]=constant.RGB.BLACK, starting_health:float=constant.PLAYER_HEALTH) -> None:
    super().__init__(x, y, w, h, color)
    self.health = starting_health


  def update(self, dx:int=0, dy:int=0, dhealth:float=0.0): # Add movement in here
    super().update(dx, dy)
    self.health += dhealth
  
  # def new_x_pos(self, dx: int = 0, object_group: pygame.sprite.Group = None):
  #     dummy_rect = self.rect.copy()
  #     dummy_rect.x += dx
  #     for floor in object_group.sprites():
  #         # Player collides with the right side of a floor
  #         if dummy_rect.colliderect(floor.rect):
  #             if dx > 0 and self.rect.right <= floor.rect.left:  # Moving right
  #                 dx = floor.rect.left - self.rect.right
  #             elif dx < 0 and self.rect.left >= floor.rect.right:  # Moving left
  #                 dx = floor.rect.right - self.rect.left
  #     return dx

      
  # def new_y_pos(self, dy:int=0, object_group:pygame.sprite.Group=None):
  #   dummy_rect = self.rect.copy()
  #   dummy_rect.y += dy
  #   for floor in object_group.sprites():
  #     if floor.rect.colliderect(dummy_rect):
  #       if dummy_rect.bottom >= floor.rect.top:  #  Player collides with top of floor
  #         returnable = dummy_rect.bottom - floor.rect.top
  #         self.on_ground = True
  #         return returnable
  #       elif dummy_rect.top <= floor.rect.bottom:  # player collides with bottom of floor
  #         returnable = dummy_rect.top - floor.rect.bottom
  #         return returnable
  #   return dy


class Base(WorldObject):
  pass

