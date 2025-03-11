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
        self.auto_shoot = True  # 自動発射をデフォルトで有効化
        
    def update(self):
        # AUTO-SHOOT MODE - Always fire when cooldown is ready
        self.auto_shoot = True
        
        # 強制的に発射
        if self.shoot_timer <= 0:
            print("DEBUG: Forcing shoot in player update")
            self.shoot()
            self.shoot_timer = PLAYER_SHOOT_INTERVAL
        
        # Keyboard movement with multiple method detection for better compatibility
        left_pressed = False
        right_pressed = False
        up_pressed = False
        down_pressed = False
        
        # Method 1: Try standard constants
        try:
            left_pressed = pyxel.btn(KEY_LEFT)
            right_pressed = pyxel.btn(KEY_RIGHT)
            up_pressed = pyxel.btn(KEY_UP)
            down_pressed = pyxel.btn(KEY_DOWN)
        except:
            pass
            
        # Method 2: Try custom key_press function if available (more reliable across versions)
        if hasattr(pyxel, 'key_press'):
            try:
                if not left_pressed:
                    left_pressed = pyxel.key_press('left') or pyxel.key_press('a')
                if not right_pressed:
                    right_pressed = pyxel.key_press('right') or pyxel.key_press('d')
                if not up_pressed:
                    up_pressed = pyxel.key_press('up') or pyxel.key_press('w')
                if not down_pressed: 
                    down_pressed = pyxel.key_press('down') or pyxel.key_press('s')
            except:
                pass
        
        # Apply movement
        if left_pressed and self.x > 0:
            self.x -= self.speed
        if right_pressed and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if up_pressed and self.y > 0:
            self.y -= self.speed
        if down_pressed and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        
        # Touch movement support - get game instance via global
        from main import game_instance
        
        if game_instance and hasattr(game_instance, 'touch_enabled') and game_instance.touch_enabled:
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
        
        # Keyboard shooting - multiple methods for better compatibility
        self.shoot_timer -= 1
        
        # Use our unified key detection method if available
        z_pressed = False
        
        # Try our custom multi-platform function first
        if hasattr(pyxel, 'key_press'):
            try:
                z_pressed = pyxel.key_press('z')
            except:
                pass
                
        # Method 1: Using KEY_Z constant from our constants as fallback
        if not z_pressed:
            try:
                z_pressed = pyxel.btn(KEY_Z)
            except:
                pass
            
        # Method 2: Try direct ASCII code (122 = 'z')
        if not z_pressed:
            try:
                z_pressed = pyxel.btn(122)
            except:
                pass
                
        # Method 3: Try lowercase 'z' string (works in some versions)
        if not z_pressed:
            try:
                z_pressed = pyxel.btn('z')
            except:
                pass
                
        # Method 4: Check if x key is pressed as alternative (in case keyboard layouts are different)
        if not z_pressed:
            try:
                if hasattr(pyxel, 'key_press'):
                    z_pressed = pyxel.key_press('x')
            except:
                pass
                
        # Method 5: Check if space is pressed as a fallback control
        if not z_pressed:
            try:
                if hasattr(pyxel, 'key_press'):
                    z_pressed = pyxel.key_press(' ')
                else:
                    z_pressed = pyxel.btn(KEY_SPACE)
            except:
                pass
                
        # Method 6: Check for touch_shoot flag
        try:
            from main import game_instance
            if game_instance and hasattr(game_instance, 'touch_shoot') and game_instance.touch_shoot:
                z_pressed = True
        except:
            pass
        
        # AUTO-SHOOT: Always fire when ready + normal trigger
        if self.shoot_timer <= 0 and (self.auto_shoot or z_pressed):
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
        
        # Play shoot sound
        import pyxel
        try:
            pyxel.play(0, 0)  # Play shoot sound
        except:
            pass  # サウンドエラーを無視
        
        # Access the game instance via global
        from main import game_instance
        if game_instance and hasattr(game_instance, 'player_bullets'):
            print("DEBUG: Adding bullet to game_instance.player_bullets")  # デバッグログ
            game_instance.player_bullets.append(bullet)
        else:
            print("DEBUG: game_instance is None or doesn't have player_bullets attribute")  # デバッグログ
    
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
