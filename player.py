import pyxel
from constants import *
from bullet import PlayerBullet

class Player:
    def __init__(self, x, y, game_ref=None):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.base_speed = PLAYER_SPEED  # 基本速度を保存
        self.speed = self.base_speed
        self.lives = PLAYER_LIVES
        self.shoot_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.auto_shoot = True  # 自動発射をデフォルトで有効化
        self.game_ref = game_ref  # ゲームインスタンスへの直接参照
        
        # パワーアップ状態
        self.powerup_type = None
        self.powerup_timer = 0
        self.has_spread_shot = False
        self.has_power_shot = False
        self.has_shield = False
        
    def update(self):
        # AUTO-SHOOT MODE - Always fire when cooldown is ready
        self.auto_shoot = True
        
        # パワーアップタイマーの更新
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.reset_powerups()
        
        # 直接弾を作成して強制的に追加（デバッグ用）
        if self.shoot_timer <= 0:
            print("DEBUG: Forcing direct bullet creation")
            try:
                # 弾を直接ゲームインスタンスに追加
                bullet = PlayerBullet(self.x + self.width // 2 - 1, self.y - 5)
                if self.game_ref and hasattr(self.game_ref, 'player_bullets'):
                    print(f"DEBUG: Direct bullet add via game_ref - before count: {len(self.game_ref.player_bullets)}")
                    self.game_ref.player_bullets.append(bullet)
                    print(f"DEBUG: Direct bullet add - after count: {len(self.game_ref.player_bullets)}")
                    self.shoot_timer = PLAYER_SHOOT_INTERVAL
                else:
                    print("DEBUG: No valid game_ref, trying global instance")
                    # フォールバック：グローバルインスタンスも試す
                    try:
                        from main import game_instance
                        if game_instance and hasattr(game_instance, 'player_bullets'):
                            game_instance.player_bullets.append(bullet)
                            self.shoot_timer = PLAYER_SHOOT_INTERVAL
                    except Exception as e:
                        print(f"DEBUG: Global fallback failed: {e}")
            except Exception as e:
                print(f"DEBUG: Direct bullet creation failed: {e}")
        
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
        print(f"DEBUG: self.shoot_timer before decrement: {self.shoot_timer}")
        self.shoot_timer -= 1
        print(f"DEBUG: self.shoot_timer after decrement: {self.shoot_timer}")
        
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
        print(f"DEBUG: auto_shoot flag: {self.auto_shoot}, z_pressed: {z_pressed}, timer: {self.shoot_timer}")
        if self.shoot_timer <= 0 and (self.auto_shoot or z_pressed):
            print("DEBUG: Shooting condition met, calling shoot()")
            self.shoot()
            self.shoot_timer = PLAYER_SHOOT_INTERVAL
        else:
            print("DEBUG: Shooting condition NOT met")
        
        # Invulnerability after being hit
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
    
    def apply_powerup(self, powerup_type):
        """パワーアップアイテムを適用する"""
        self.powerup_type = powerup_type
        self.powerup_timer = POWERUP_DURATION
        
        # パワーアップタイプに応じた効果適用
        if powerup_type == POWERUP_SPREAD:
            self.has_spread_shot = True
            print("DEBUG: POWERUP - SPREAD SHOT activated")
        elif powerup_type == POWERUP_POWER:
            self.has_power_shot = True
            print("DEBUG: POWERUP - POWER SHOT activated")
        elif powerup_type == POWERUP_SPEED:
            self.speed = self.base_speed * 1.5  # 速度1.5倍
            print("DEBUG: POWERUP - SPEED BOOST activated")
        elif powerup_type == POWERUP_SHIELD:
            self.has_shield = True
            self.invulnerable = True
            self.invulnerable_timer = POWERUP_DURATION
            print("DEBUG: POWERUP - SHIELD activated")
    
    def reset_powerups(self):
        """パワーアップ効果をリセットする"""
        self.powerup_type = None
        self.has_spread_shot = False
        self.has_power_shot = False
        self.has_shield = False
        self.speed = self.base_speed
        print("DEBUG: Powerups reset")
    
    def shoot(self):
        print("DEBUG: shoot() method called!") # 追加デバッグ
        try:
            bullet_x = self.x + self.width // 2 - 1
            bullet_y = self.y - 5
            
            # Play shoot sound
            import pyxel
            try:
                pyxel.play(0, 0)  # Play shoot sound
            except:
                pass  # サウンドエラーを無視
                
            # スプレッドショット（散弾）の場合
            if self.has_spread_shot and self.game_ref and hasattr(self.game_ref, 'player_bullets'):
                # 中央弾
                center_bullet = PlayerBullet(bullet_x, bullet_y)
                # 左斜め弾
                left_bullet = PlayerBullet(bullet_x, bullet_y)
                left_bullet.x_speed = -0.5  # 左に少し移動
                # 右斜め弾
                right_bullet = PlayerBullet(bullet_x, bullet_y)
                right_bullet.x_speed = 0.5  # 右に少し移動
                
                # 全ての弾を追加
                self.game_ref.player_bullets.append(center_bullet)
                self.game_ref.player_bullets.append(left_bullet)
                self.game_ref.player_bullets.append(right_bullet)
                print("DEBUG: Spread shot fired")
            else:
                # 通常の弾
                bullet = PlayerBullet(bullet_x, bullet_y)
                # パワーショットの場合は強化
                if self.has_power_shot:
                    bullet.damage = 2  # 通常の2倍のダメージ
                    bullet.width = 4   # 弾のサイズを大きく
                    bullet.color = RED # 色を変える
                    print("DEBUG: Power shot fired")
                
                # Use direct game reference instead of global import
                print(f"DEBUG: self.game_ref: {self.game_ref}")  # デバッグログ
                if self.game_ref and hasattr(self.game_ref, 'player_bullets'):
                    print(f"DEBUG: Player bullets before append: {len(self.game_ref.player_bullets)}")  # デバッグログ
                    self.game_ref.player_bullets.append(bullet)
                    print(f"DEBUG: Player bullets after append: {len(self.game_ref.player_bullets)}")  # デバッグログ
                else:
                    print("DEBUG: game_ref is None or doesn't have player_bullets attribute")  # デバッグログ
                    
                    # フォールバック：グローバルインスタンスを試す
                    try:
                        from main import game_instance
                        if game_instance and hasattr(game_instance, 'player_bullets'):
                            game_instance.player_bullets.append(bullet)
                    except:
                        pass
        except Exception as e:
            print(f"DEBUG: Exception in shoot(): {e}")  # 例外をキャッチして表示
    
    def hit(self):
        # シールドか無敵状態ならダメージを受けない
        if self.has_shield or self.invulnerable:
            return False
            
        # 通常時はダメージを受ける
        self.lives -= 1
        self.invulnerable = True
        self.invulnerable_timer = 60  # 1 second of invulnerability
        return True
    
    def draw(self):
        # Don't draw if dead
        if self.lives <= 0:
            return
        
        # Blink when invulnerable (シールドは点滅しない)
        if self.invulnerable and not self.has_shield and pyxel.frame_count % 4 < 2:
            return
            
        # シールド効果の描画
        if self.has_shield:
            # 円形のシールドエフェクト
            pyxel.circb(
                self.x + self.width // 2,
                self.y + self.height // 2,
                max(self.width, self.height),
                LIGHT_BLUE
            )
        
        # Draw player ship - triangle shape with thrusters
        pyxel.tri(
            self.x + self.width // 2, self.y,  # Top
            self.x, self.y + self.height,  # Bottom left
            self.x + self.width, self.y + self.height,  # Bottom right
            CYAN
        )
        
        # Draw thrusters (animated)
        thrust_length = 3 + (pyxel.frame_count % 3)
        
        # パワーアップ状態の視覚的表示（スラスター色を変更）
        thruster_color = RED  # デフォルト色
        if self.powerup_type is not None:
            if self.powerup_type == POWERUP_SPREAD:
                thruster_color = YELLOW
            elif self.powerup_type == POWERUP_POWER:
                thruster_color = RED
            elif self.powerup_type == POWERUP_SPEED:
                thruster_color = CYAN
                
        pyxel.rect(self.x + 2, self.y + self.height, 1, thrust_length, thruster_color)
        pyxel.rect(self.x + self.width - 3, self.y + self.height, 1, thrust_length, thruster_color)
