# Game Constants
import pyxel
import datetime

# Version information
VERSION = "1.0"
BUILD_NUMBER = "25032025.2"  # 日付とビルド番号（年月日.ビルド番号）
BUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
VERSION_DISPLAY = f"v{VERSION} (Build {BUILD_NUMBER})"

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
PLAYER_BULLET_SPEED = -4  # 負の値で上に移動
PLAYER_SHOOT_INTERVAL = 15  # 自動発射用に少し長めにしました
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

# Boss settings
BOSS_DISTANCE_INTERVAL = 3000  # ボスが出現するまでの距離間隔
BOSS_DISTANCE_MAX = 30000  # ゲーム全体の距離（10体のボスと通常ステージ）
BOSS_EXTRA_LIFE = 1  # ボスを倒した時に得られる追加ライフ
BOSS_CLEAR_BONUS = 50000  # すべてのボスを倒した時のボーナス得点
BOSS_CYCLE_ENABLED = True  # ボスを倒した後、次のボスまでのサイクルを有効にするか

# Score settings
ENEMY_SMALL_SCORE = 100
ENEMY_MEDIUM_SCORE = 200
ENEMY_LARGE_SCORE = 300

# Game states
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_INTRO = 3  # イントロアニメーション用の状態追加

# パワーアップタイプ
POWERUP_YELLOW = 0  # 黄色アイテム（連射速度アップ→複数方向発射）
POWERUP_POWER = 1   # 赤アイテム（弾のパワーアップ：敵を一撃で倒せる）
POWERUP_SPEED = 2   # 水色アイテム（プレイヤーの移動速度アップ）
POWERUP_SHIELD = 3  # 緑アイテム（一定時間無敵になる）

# 旧命名でも動作するようにエイリアスを設定
POWERUP_SPREAD = POWERUP_YELLOW  # 下位互換性のため

# パワーアップ設定
POWERUP_DURATION = 600    # パワーアップの効果持続時間（フレーム数）
POWERUP_DROP_CHANCE = 0.2  # 敵を倒した時にアイテムが出る確率

# 音量設定
MIN_VOLUME = 0            # 最小音量
MAX_VOLUME = 7            # 最大音量
DEFAULT_VOLUME = 4        # 初期音量（中間）
VOLUME_CHANGE_COOLDOWN = 10  # 音量変更の連続入力を防止するクールダウン（フレーム数）
KEY_MINUS = pyxel.KEY_MINUS if hasattr(pyxel, 'KEY_MINUS') else 45  # ASCII for minus '-'
KEY_PLUS = pyxel.KEY_PLUS if hasattr(pyxel, 'KEY_PLUS') else 43     # ASCII for plus '+'
KEY_EQUAL = pyxel.KEY_EQUAL if hasattr(pyxel, 'KEY_EQUAL') else 61   # ASCII for equal '='（プラスキーの代わりに使用可能）
