# Game Constants
import pyxel

# Screen dimensions
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 240

# Colors
BLACK = 0
NAVY = 1
PURPLE = 2
GREEN = 3
BROWN = 4
DARK_BLUE = 5
LIGHT_BLUE = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
LIME = 11
CYAN = 12
GRAY = 13
PINK = 14
PEACH = 15

# Keyboard/input constants - to support different Pyxel versions
KEY_Z = pyxel.KEY_Z if hasattr(pyxel, 'KEY_Z') else 122  # ASCII for 'z'
KEY_SPACE = pyxel.KEY_SPACE if hasattr(pyxel, 'KEY_SPACE') else 32  # ASCII for space
KEY_LEFT = pyxel.KEY_LEFT if hasattr(pyxel, 'KEY_LEFT') else 37  # ASCII for left arrow
KEY_RIGHT = pyxel.KEY_RIGHT if hasattr(pyxel, 'KEY_RIGHT') else 39  # ASCII for right arrow
KEY_UP = pyxel.KEY_UP if hasattr(pyxel, 'KEY_UP') else 38  # ASCII for up arrow
KEY_DOWN = pyxel.KEY_DOWN if hasattr(pyxel, 'KEY_DOWN') else 40  # ASCII for down arrow
MOUSE_BUTTON_LEFT = pyxel.MOUSE_BUTTON_LEFT if hasattr(pyxel, 'MOUSE_BUTTON_LEFT') else 0  # Left mouse button

# Player settings
PLAYER_SPEED = 2
PLAYER_BULLET_SPEED = 4
PLAYER_SHOOT_INTERVAL = 5
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_LIVES = 3

# Enemy settings
ENEMY_SMALL_SPEED = 1
ENEMY_MEDIUM_SPEED = 0.7
ENEMY_LARGE_SPEED = 0.5
ENEMY_SPAWN_INTERVAL = 30
ENEMY_SHOOT_INTERVAL = 60

# Game settings
SCROLL_SPEED = 1

# Score settings
ENEMY_SMALL_SCORE = 100
ENEMY_MEDIUM_SCORE = 200
ENEMY_LARGE_SCORE = 300

# Game states
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
