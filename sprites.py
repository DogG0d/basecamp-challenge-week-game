import pygame
import constant
import globals
from inputstream import InputStream


class WorldObject(pygame.sprite.Sprite):
  def __init__(self, x:int=None, y:int=None, w:int=constant.PLAYER_WIDTH, h:int=constant.PLAYER_HEIGHT, color:tuple[int,int,int]=constant.RGB.BLACK) -> None:
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface([w,h])
    self.image.fill(color)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  

  def update(self) -> None:
    super().update(self)
  

  def move() -> None:
    pass


  def is_colliding() -> bool:
    return False


  def get_rect(self) -> pygame.rect.Rect:
    return self.rect


class Entity(WorldObject):
  def __init__(self, x: int = None, y: int = None, w: int = constant.PLAYER_WIDTH, h: int = constant.PLAYER_HEIGHT, color: tuple[int, int, int] = constant.RGB.BLACK, gravity: float = constant.GRAVITY) -> None:
    super().__init__(x, y, w, h, color)
    self.gravity = gravity
  

  def update(self) -> None:
    super().update(self)
  

  def is_on_ground(self) -> bool:
    dummy = self.get_rect().copy()
    dummy.x += 1
    # for base in globals.world.base_group:  # To Be Added
    #   dummy.colliderect(base.get_rect())
    return False
    
  
  def new_x_pos(self, dx: int = 0, object_group: pygame.sprite.Group = None):
      dummy_rect = self.rect.copy()
      dummy_rect.x += dx
      for floor in object_group.sprites():
          # Player collides with the right side of a floor
          if dummy_rect.colliderect(floor.rect):
              if dx > 0 and self.rect.right <= floor.rect.left:  # Moving right
                  dx = floor.rect.left - self.rect.right
              elif dx < 0 and self.rect.left >= floor.rect.right:  # Moving left
                  dx = floor.rect.right - self.rect.left
      return dx

      
  def new_y_pos(self, dy:int=0, object_group:pygame.sprite.Group=None):
    dummy_rect = self.rect.copy()
    dummy_rect.y += dy
    for floor in object_group.sprites():
      if floor.rect.colliderect(dummy_rect):
        if dummy_rect.bottom >= floor.rect.top:  #  Player collides with top of floor
          returnable = dummy_rect.bottom - floor.rect.top
          self.on_ground = True
          return returnable
        elif dummy_rect.top <= floor.rect.bottom:  # player collides with bottom of floor
          returnable = dummy_rect.top - floor.rect.bottom
          return returnable
    return dy



class Player(Entity):
  # vel_x = 10
  # vel_y = 0
  # flying_velocity_multiplier = 1.0
  # direction = None
  # on_ground = False

  def __init__(self, x:int=None, y:int=None, w:int=constant.PLAYER_WIDTH, h:int=constant.PLAYER_HEIGHT, color:tuple[int,int,int]=constant.RGB.BLACK, starting_health:float=constant.PLAYER_HEALTH) -> None:
    super().__init__(x, y, w, h, color)
    self.health = starting_health
    self.state = constant.PlayerState.IDLE
  

  def __init__(self, input_stream: InputStream):
     self.input = input_stream


  def update(self): # Add movement in here
    # Run parent method
    super().update()

    ### Move left
    if self.input.isKeyDown(pygame.K_a) or self.input.isKeyDown(pygame.K_LEFT):
      self.move()

    ### Move right
    if self.input.isKeyDown(pygame.K_d) or self.input.isKeyDown(pygame.K_RIGHT):
      self.move()
    
    ### Jump
    if self.input.isKeyPressed(pygame.K_w) or self.input.isKeyPressed(pygame.K_UP):
      self.move()

    ### Dash
    if self.input.isKeyPressed(pygame.K_e):
      self.move()


class Base(WorldObject):
  pass

