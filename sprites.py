import pygame
import constant

class Player(pygame.sprite.Sprite):
  vel_x = 10
  vel_y = 0
  flying_velocity_multiplier = 1.0
  direction = None
  on_ground = False

  def __init__(self, x:int=None, y:int=None, w:int=constant.PLAYER_WIDTH, h:int=constant.PLAYER_HEIGHT, color:tuple[int,int,int]=constant.RGB.BLACK, starting_health:float=constant.PLAYER_HEALTH) -> None:
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface([w,h])
    self.image.fill(color)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.health = starting_health


  def update(self, dx:int=0, dy:int=0, dhealth:float=0.0, collision_group:pygame.sprite.Group=None):
    pygame.sprite.Sprite.update(self)
    self.rect.x += dx
    self.rect.y += dy
    self.health += dhealth
  
  def x_collision_compensation(self, dx:int=0, object_group:pygame.sprite.Group=None):
    dummy_rect = self.rect.copy()
    dummy_rect.x += dx
    for floor in object_group.sprites():
      if floor.rect.colliderect(dummy_rect):
        if dummy_rect.left <= floor.right:  #  Player collides with right side of floor
          return  dummy_rect.left - floor.rect.right - 1
        elif dummy_rect.right >= floor.left:  # Player collides with left side of floor
          return dummy_rect.right - floor.rect.left + 1
    return dx
      
  def y_collision_compensation(self, dy:int=0, object_group:pygame.sprite.Group=None):
    dummy_rect = self.rect.copy()
    dummy_rect.y += dy
    for floor in object_group.sprites():
      if floor.rect.colliderect(dummy_rect):
        if dummy_rect.bottom >= floor.rect.top:  #  Player collides with top of floor
          returnable = floor.rect.top - dummy_rect.bottom
          print(dummy_rect.bottom, floor.rect.top, returnable)
          self.on_ground = True
          return returnable
        elif dummy_rect.top <= floor.rect.bottom:  # player collides with bottom of floor
          returnable = floor.rect.bottom - dummy_rect.top
          print(dummy_rect.bottom, floor.rect.top, returnable)
          return returnable
    return dy



class Base(pygame.sprite.Sprite):
  def __init__(self, x:int=None, y:int=None, w:int=None, h:int=None, color:tuple[int,int,int]=constant.RGB.BLACK) -> None:
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface([w,h])
    self.image.fill(color)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y


  def update(self, dx:int=0, dy:int=0):
    pygame.sprite.Sprite.update(self)
    print(f"{self}\nUPDATED")
    self.rect.x += dx
    self.rect.y += dy

