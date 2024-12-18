# Colors
class RGB:
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  GRAY = (128, 128, 128)
  ORANGE = (255, 165, 0)
  SKY_BLUE = (135, 206, 235)

class Direction:
  LEFT = 1
  RIGHT = 2


class PlayerState:
   IDLE = 0
   MOVING = 1


class Mouse:
  LEFT = 0
  MIDDLE = 1
  RIGHT = 2
  BACKWARD = 4
  FORWARD = 5
  SCROLL_UP = -1
  SCROLL_DOWN = -2


# OS
BASE_PATH = "data/"
IMAGE_PATH = BASE_PATH + "images/"

# Screen
DISPLAY_SIZE = (864, 486)
GAME_SIZE = (432, 243)
# SCREEN_SIZE = (640, 480)
FRAMES_PER_SECOND = 60

# Logic
GRAVITY = 0.1
MAX_FALL_SPEED = 12

### Player
# Attributes and defaults
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_HEALTH = 10.0

# Movement
PLAYER_SPEED = 10
JUMP_HEIGHT = 3
DASH_SPEED = 25
DASH_DECAY = 0.5
DASH_COOLDOWN_FRAMES = 120