import pyxel
from constants import *
from bullet import PlayerBullet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES
        self.shoot_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def update(self):
        # Keyboard movement
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_UP) and self.y > 0:
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN) and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        
        # Touch movement support
        game_instance = None
        for obj in pyxel._app._update_funcs:
            if hasattr(obj, 'touch_enabled'):
                game_instance = obj
                break
                
        if game_instance and game_instance.touch_enabled:
            # Calculate movement direction based on touch drag
            dx = game_instance.touch_current_x - game_instance.touch_start_x
            dy = game_instance.touch_current_y - game_instance.touch_start_y
            
            # Apply movement with deadzone
            if abs(dx) > 5:  # Small deadzone for better control
                self.x += (dx / 10) * self.speed
            if abs(dy) > 5:
                self.y += (dy / 10) * self.speed
            
            # Keep player within screen bounds
            self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
            self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
            
            # Handle shooting with touch
            if game_instance.touch_shoot and self.shoot_timer <= 0:
                self.shoot()
                self.shoot_timer = PLAYER_SHOOT_INTERVAL
        
        # Keyboard shooting
        self.shoot_timer -= 1
        if self.shoot_timer <= 0 and pyxel.btn(pyxel.KEY_Z):
            self.shoot()
            self.shoot_timer = PLAYER_SHOOT_INTERVAL
        
        # Invulnerability after being hit
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
    
    def shoot(self):
        # Create a bullet
        bullet = PlayerBullet(self.x + self.width // 2 - 1, self.y - 5)
        from game import Game
        # Get the current game instance to add the bullet
        import pyxel
        pyxel.play(0, 0)  # Play shoot sound
        
        # Access the game instance
        for obj in pyxel._app._update_funcs:
            if hasattr(obj, 'player_bullets'):
                obj.player_bullets.append(bullet)
                break
    
    def hit(self):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 60  # 1 second of invulnerability
    
    def draw(self):
        # Don't draw if dead
        if self.lives <= 0:
            return
        
        # Blink when invulnerable
        if self.invulnerable and pyxel.frame_count % 4 < 2:
            return
        
        # Draw player ship - triangle shape with thrusters
        pyxel.tri(
            self.x + self.width // 2, self.y,  # Top
            self.x, self.y + self.height,  # Bottom left
            self.x + self.width, self.y + self.height,  # Bottom right
            CYAN
        )
        
        # Draw thrusters (animated)
        thrust_length = 3 + (pyxel.frame_count % 3)
        pyxel.rect(self.x + 2, self.y + self.height, 1, thrust_length, RED)
        pyxel.rect(self.x + self.width - 3, self.y + self.height, 1, thrust_length, RED)
