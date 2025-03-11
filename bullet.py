import pyxel
from constants import *

class Bullet:
    def __init__(self, x, y, speed, color, width=2, height=5):
        self.x = x
        self.y = y
        self.dx = 0  # Horizontal movement (for angled shots)
        self.speed = speed
        self.color = color
        self.width = width
        self.height = height
    
    def update(self):
        # Movement logic
        self.y += self.speed
        self.x += self.dx
    
    def draw(self):
        # Draw bullet
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

class PlayerBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, -PLAYER_BULLET_SPEED, CYAN)
    
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
