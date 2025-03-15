import pyxel
import math
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
        
        # 射撃関連
        self.base_shoot_interval = PLAYER_SHOOT_INTERVAL  # 基本射撃間隔
        self.shoot_timer = 0
        self.shoot_interval = self.base_shoot_interval     # 現在の射撃間隔
        
        # 無敵状態
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.auto_shoot = True  # 自動発射をデフォルトで有効化
        self.game_ref = game_ref  # ゲームインスタンスへの直接参照
        
        # パワーアップ状態
        self.powerup_type = None
        self.powerup_timer = 0
        
        # 黄色パワーアップの段階管理
        self.yellow_level = 0       # 黄色パワーアップのレベル（0-2）
        self.shot_direction = 1     # 弾の発射方向数
        self.max_yellow_level = 2   # 最大レベル（3段階なので0-2）
        
        self.has_power_shot = False  # 赤アイテム効果
        self.has_shield = False      # 緑アイテム効果
        
    def update(self):
        # AUTO-SHOOT MODE - Always fire when cooldown is ready
        self.auto_shoot = True
        
        # パワーアップタイマーの更新
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.reset_powerups()
        
        # 黄色パワーアップが適用されている場合、射撃間隔を調整
        # 通常はPLAYER_SHOOT_INTERVALが使われるが、黄色パワーアップのレベルに応じて短縮
        if self.shoot_timer <= 0:
            current_interval = self.shoot_interval if hasattr(self, 'shoot_interval') else PLAYER_SHOOT_INTERVAL
            self.shoot_timer = current_interval
            print(f"DEBUG: Using shoot interval: {current_interval}")
        
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
        
        # キーボードモード専用 - 画面内に自機を維持
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
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
                
        # Method 6: Check for auto_shoot flag from game instance
        try:
            from main import game_instance
            if game_instance and hasattr(game_instance, 'auto_shoot') and game_instance.auto_shoot:
                z_pressed = True
        except:
            pass
        
        # AUTO-SHOOT: Always fire when ready + normal trigger
        print(f"DEBUG: auto_shoot flag: {self.auto_shoot}, z_pressed: {z_pressed}, timer: {self.shoot_timer}")
        if self.shoot_timer <= 0 and (self.auto_shoot or z_pressed):
            print("DEBUG: Shooting condition met, calling shoot()")
            self.shoot()
            # 黄色パワーアップが適用されている場合、射撃間隔を調整
            current_interval = self.shoot_interval if hasattr(self, 'shoot_interval') else PLAYER_SHOOT_INTERVAL
            self.shoot_timer = current_interval
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
        if powerup_type == POWERUP_YELLOW:
            # 黄色アイテム: 射撃レベルか方向数を増加
            self.apply_yellow_powerup()
            print(f"DEBUG: YELLOW POWERUP - Level {self.yellow_level}, Directions {self.shot_direction}")
            
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
            
    def apply_yellow_powerup(self):
        """黄色パワーアップの段階的処理"""
        # 現在のレベルを一段階上げる
        self.yellow_level += 1
        
        # レベルが最大に達したかチェック
        if self.yellow_level > self.max_yellow_level:
            # レベルをリセットして弾の方向数を増やす
            self.yellow_level = 0
            self.shot_direction += 1
            print(f"DEBUG: Shot directions increased to {self.shot_direction}")
            
            # 射撃間隔を初期値に戻す
            self.shoot_interval = self.base_shoot_interval
        else:
            # レベルに応じて射撃間隔を短くする (最大3段階)
            # レベル0で基本値、レベル2で最速（基本値の1/3）
            factor = 1.0 - (self.yellow_level / (self.max_yellow_level + 1) * 0.7)
            self.shoot_interval = int(self.base_shoot_interval * factor)
            print(f"DEBUG: Shoot interval decreased to {self.shoot_interval} (factor: {factor:.2f})")
    
    def reset_powerups(self):
        """パワーアップ効果をリセットする"""
        self.powerup_type = None
        self.has_power_shot = False
        self.has_shield = False
        self.speed = self.base_speed
        # 黄色パワーアップの段階はリセットしない（永続的効果）
        print("DEBUG: Powerups reset")
    
    def shoot(self):
        print("DEBUG: shoot() method called!") # 追加デバッグ
        try:
            bullet_x = self.x + self.width // 2 - 1
            bullet_y = self.y - 5
            
            # 発射音は無効化（消音設定）
            # 以前はここで発射音を鳴らしていました
            
            # ゲームインスタンスの参照があるか確認
            if not (self.game_ref and hasattr(self.game_ref, 'player_bullets')):
                print("DEBUG: game_ref is None or doesn't have player_bullets attribute")
                return
                
            print(f"DEBUG: Shot direction count: {self.shot_direction}")
                
            # 複数方向弾発射の場合（黄色パワーアップ）
            if self.shot_direction > 1:
                # 発射方向数に応じた角度の弾を生成
                angle_step = 30  # 初期値は左右30度ずつ
                
                # 方向数が増えるほど、発射角度の範囲を広げる
                if self.shot_direction >= 6:  # 6方向以上なら360度全周に
                    angle_step = 360 / self.shot_direction
                elif self.shot_direction >= 4:  # 4-5方向なら120度の扇状に
                    angle_step = 30
                else:  # 2-3方向の場合は左右30度に
                    angle_step = 25
                
                bullets_created = 0
                
                # まず前方（上向き）の弾を必ず発射
                # 真上方向の弾を作成
                forward_bullet = PlayerBullet(bullet_x, bullet_y, 0.0)
                forward_bullet.speed = -abs(forward_bullet.speed) * 1.2  # 強制的に上向き、速度を少し速く
                
                # パワーショットの場合は強化
                if self.has_power_shot:
                    forward_bullet.damage = 2
                    forward_bullet.width = 4
                    forward_bullet.color = RED
                
                # 弾を追加
                self.game_ref.player_bullets.append(forward_bullet)
                bullets_created = 1  # 必ず1発は発射される
                print("DEBUG: Added forward shot")
                
                # 方向数が2以上なら追加の方向にも発射
                if self.shot_direction > 1:
                    # 残りの方向に発射
                    for i in range(self.shot_direction - 1):  # 前方弾は既に発射済みなので-1
                        # 角度を計算（ラジアン）
                        PI = 3.14159
                        
                        if self.shot_direction >= 6:  # 全周発射の場合
                            # 全周360度に均等配置するが、前方位置を開ける
                            total_angles = self.shot_direction - 1
                            # スタート角度をずらして前方に弾を集中させない
                            start_offset = 30  # 度数
                            # 前方を含まない角度で等間隔に配置
                            angle = ((i * (360 - start_offset) / total_angles) + start_offset) * (PI / 180)
                        elif self.shot_direction >= 4:  # 4-5方向の場合は広い扇状に
                            # 扇形の角度を広げる（240度の範囲）
                            total_spread = 240
                            angle_per_shot = total_spread / (self.shot_direction - 1)
                            # 左右対称に配置
                            offset = total_spread / 2
                            angle = ((i * angle_per_shot) - offset / 2) * (PI / 180)
                        else:  # 2-3方向の場合は少し狭い扇状に
                            # 左右対称に配置（約120度の扇状）
                            total_spread = 120
                            angle_per_shot = total_spread / (self.shot_direction - 1)
                            # 左右対称に配置
                            offset = total_spread / 2
                            angle = ((i * angle_per_shot) - offset / 2) * (PI / 180)
                                
                        # 角度から速度を計算
                        speed_x = math.sin(angle) * 0.5
                        speed_y = -math.cos(angle)  # 上向きを基準とするため -cos
                        
                        # 弾を生成
                        bullet = PlayerBullet(bullet_x, bullet_y, speed_x)
                        
                        # 弾の方向補正（上向き基準）
                        bullet.speed = bullet.speed * speed_y
                        
                        # パワーショットの場合は強化
                        if self.has_power_shot:
                            bullet.damage = 2
                            bullet.width = 4
                            bullet.color = RED
                        
                        # 弾を追加
                        self.game_ref.player_bullets.append(bullet)
                        bullets_created += 1
                    # 追加コードは不要（ループ内で処理済み）
                
                print(f"DEBUG: Multi-directional shot fired ({bullets_created} bullets)")
                
            else:
                # 通常の弾を発射（単一方向）
                bullet = PlayerBullet(bullet_x, bullet_y)
                
                # パワーショットの場合は強化
                if self.has_power_shot:
                    bullet.damage = 2  # 通常の2倍のダメージ
                    bullet.width = 4   # 弾のサイズを大きく
                    bullet.color = RED # 色を変える
                    print("DEBUG: Power shot fired")
                
                # 弾を追加
                print(f"DEBUG: Player bullets before append: {len(self.game_ref.player_bullets)}")
                self.game_ref.player_bullets.append(bullet)
                print(f"DEBUG: Player bullets after append: {len(self.game_ref.player_bullets)}")
                print("DEBUG: Single shot fired")
                
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
