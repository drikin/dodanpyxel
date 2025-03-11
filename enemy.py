import pyxel
import math
import random
from constants import *
from bullet import EnemyBullet

class Enemy:
    def __init__(self, x, y, width, height, speed, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.move_pattern = random.choice(['straight', 'sine', 'zigzag'])
        self.shoot_timer = random.randint(30, ENEMY_SHOOT_INTERVAL)
        self.frame_count = 0
        self.amplitude = random.randint(20, 40)
        self.frequency = random.uniform(0.05, 0.1)
        self.start_x = x
    
    def update(self):
        # Move based on pattern
        if self.move_pattern == 'straight':
            self.y += self.speed
        elif self.move_pattern == 'sine':
            self.y += self.speed
            self.x = self.start_x + math.sin(self.frame_count * self.frequency) * self.amplitude
        elif self.move_pattern == 'zigzag':
            self.y += self.speed
            if (self.frame_count // 15) % 2 == 0:
                self.x += self.speed
            else:
                self.x -= self.speed
                
        # Keep within screen bounds
        if self.x < 0:
            self.x = 0
            self.move_pattern = 'sine'  # Change pattern if hit wall
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.move_pattern = 'sine'  # Change pattern if hit wall
        
        # Shooting
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.randint(30, ENEMY_SHOOT_INTERVAL)
        
        self.frame_count += 1
    
    def shoot(self):
        # Base enemy shooting logic - override in subclasses
        pass
    
    def hit(self):
        self.health -= 1
    
    def draw(self):
        # Base enemy drawing - override in subclasses
        pass

class SmallEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 8, 8, ENEMY_SMALL_SPEED, 1)
    
    def shoot(self):
        # Small enemies shoot single bullets
        bullet = EnemyBullet(self.x + self.width // 2 - 1, self.y + self.height)
        
        # Access the game instance via global
        from main import game_instance
        if game_instance and hasattr(game_instance, 'enemy_bullets'):
            game_instance.enemy_bullets.append(bullet)
    
    def draw(self):
        # Draw a small triangular enemy
        pyxel.tri(
            self.x + self.width // 2, self.y + self.height,  # Bottom
            self.x, self.y,  # Top left
            self.x + self.width, self.y,  # Top right
            RED
        )
        
        # Draw accent
        pyxel.pset(self.x + self.width // 2, self.y + self.height // 2, YELLOW)

class MediumEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 12, 12, ENEMY_MEDIUM_SPEED, 3)
    
    def shoot(self):
        # Medium enemies shoot two bullets
        bullet1 = EnemyBullet(self.x + 2, self.y + self.height)
        bullet2 = EnemyBullet(self.x + self.width - 3, self.y + self.height)
        
        # Access the game instance via global
        from main import game_instance
        if game_instance and hasattr(game_instance, 'enemy_bullets'):
            game_instance.enemy_bullets.append(bullet1)
            game_instance.enemy_bullets.append(bullet2)
    
    def draw(self):
        # Draw a medium rectangular enemy
        pyxel.rect(self.x, self.y, self.width, self.height, ORANGE)
        
        # Draw cockpit
        pyxel.rect(self.x + self.width // 2 - 2, self.y + 2, 4, 4, RED)
        
        # Draw engines
        pyxel.rect(self.x + 2, self.y + self.height - 3, 2, 3, YELLOW)
        pyxel.rect(self.x + self.width - 4, self.y + self.height - 3, 2, 3, YELLOW)

class LargeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16, ENEMY_LARGE_SPEED, 5)
    
    def shoot(self):
        # Large enemies shoot three bullets in a spread
        bullet1 = EnemyBullet(self.x + self.width // 2 - 1, self.y + self.height)
        bullet2 = EnemyBullet(self.x + 2, self.y + self.height - 2)
        bullet3 = EnemyBullet(self.x + self.width - 3, self.y + self.height - 2)
        
        # Set angle for side bullets (using integers since dx is defined as int)
        bullet2.dx = -1
        bullet3.dx = 1
        
        # Access the game instance via global
        from main import game_instance
        if game_instance and hasattr(game_instance, 'enemy_bullets'):
            game_instance.enemy_bullets.append(bullet1)
            game_instance.enemy_bullets.append(bullet2)
            game_instance.enemy_bullets.append(bullet3)
    
    def draw(self):
        # Draw a large diamond-shaped enemy
        pyxel.circ(self.x + self.width // 2, self.y + self.height // 2, self.width // 2, PURPLE)
        
        # Draw inner details
        pyxel.circ(self.x + self.width // 2, self.y + self.height // 2, self.width // 4, PINK)
        
        # Draw engine flares
        flare_size = 1 + (pyxel.frame_count % 3)
        pyxel.circ(self.x + self.width // 4, self.y + self.height - 3, flare_size, YELLOW)
        pyxel.circ(self.x + 3 * self.width // 4, self.y + self.height - 3, flare_size, YELLOW)
