import pyxel
from constants import *

class Bullet:
    def __init__(self, x, y, speed, color, width=2, height=5):
        self.x = x
        self.y = y
        self.dx = 0  # Horizontal movement (for angled shots) - integer value
        self.speed = speed
        self.color = color
        self.width = width
        self.height = height
        self.damage = 1  # デフォルトダメージ
    
    def update(self):
        # Movement logic
        self.y += self.speed
        self.x += self.dx
    
    def draw(self):
        # Draw bullet
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

class PlayerBullet(Bullet):
    def __init__(self, x, y, x_speed=0.0):
        # 速度を直接指定して確実に上方向に移動
        super().__init__(x, y, PLAYER_BULLET_SPEED, CYAN)
        self.x_speed = float(x_speed)  # 横方向の速度設定（float型に明示的に変換）
    
    def update(self):
        # 弾の上方向への移動 (speed値はマイナス = 上向き)
        self.y += self.speed
        
        # 横方向の移動を適用（x_speedが設定されている場合、斜めに移動）
        if self.x_speed != 0:
            self.x += self.x_speed
    
    def draw(self):
        # Special drawing for player bullet
        pyxel.rect(self.x, self.y, self.width, self.height, YELLOW)
        pyxel.rect(self.x, self.y + self.height - 2, self.width, 2, WHITE)

class EnemyBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, 2, RED, 2, 4)
    
    def draw(self):
        # Special drawing for enemy bullet
        pyxel.rect(self.x, self.y, self.width, self.height, ORANGE)
        pyxel.rect(self.x, self.y, self.width, 2, RED)
