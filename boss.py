import pyxel
import random
import math
from constants import *

# 色の定数
WHITE = 7
BLACK = 0
RED = 8
YELLOW = 10

from bullet import EnemyBullet

class Boss:
    """ボスの基本クラス - すべてのボスの共通動作を定義"""
    
    def __init__(self, x, y, boss_number):
        self.x = x
        self.y = y
        self.boss_number = boss_number  # 1-10のボス番号
        
        # ボス番号に応じたサイズ計算（最初が50%で徐々に大きくなる）
        size_percent = 50 + (boss_number - 1) * 5  # 5%ずつ増加（50%〜95%）
        
        # 画面サイズを基準にしたサイズ計算
        self.width = int(SCREEN_WIDTH * size_percent / 100)
        self.height = int(SCREEN_HEIGHT * size_percent / 100)
        
        # 体力はボス番号に応じて2倍ずつ増加
        base_health = 100  # ボス1の基本体力
        # 2^(boss_number-1) の計算で2倍ずつ増加
        self.max_health = base_health * (2 ** (boss_number - 1))  
        self.health = self.max_health
        
        # 移動パターン用の変数
        self.speed = 0.5 + boss_number * 0.1  # ボス番号によって徐々に速くなる
        self.move_time = 0
        self.move_pattern = 0
        self.target_x = x
        self.target_y = y
        
        # 攻撃パターン用の変数
        self.attack_timer = 0
        self.attack_interval = max(60 - boss_number * 3, 20)  # ボス番号が上がるほど頻繁に攻撃
        
        # 状態関連
        self.active = True  # ボスが行動可能かどうか
        self.entry_phase = True  # 登場フェーズ中か
        self.exit_phase = False  # 退場フェーズ中か
        self.exit_bgm_changed = False  # 退場時BGM切り替えフラグ
        self.explosion_timer = 0  # 爆発エフェクト用
        self.flash_timer = 0      # ダメージ表現用
        
        # ボスの色情報（ボスごとに異なる）
        self.color_main = (boss_number % 8) + 8  # 8-15のいずれかの色
        self.color_sub = (boss_number % 8)       # 0-7のいずれかの色
        
        # 攻撃レベル（ボス番号によって高くなる）
        self.attack_level = boss_number
        
    def update(self, player_bullets, enemy_bullets, player):
        """ボスを更新する（プレイヤーの弾との当たり判定）"""
        if not self.active:
            return 0  # スコア変化なし
            
        # プレイヤーの弾との衝突判定
        for bullet in player_bullets[:]:
            if (bullet.x + bullet.width > self.x and
                bullet.x < self.x + self.width and
                bullet.y + bullet.height > self.y and
                bullet.y < self.y + self.height):
                
                # 弾のダメージ（パワーショットなら2、通常は1）
                damage = getattr(bullet, 'damage', 1)
                
                # ダメージ処理
                self.health -= damage
                self.flash_timer = 3  # ダメージ表現用
                
                # 弾を削除
                if bullet in player_bullets:
                    player_bullets.remove(bullet)
                    
                # ボスを倒した場合
                if self.health <= 0:
                    self.exit_phase = True
                    # ボス撃破時のボーナス得点
                    return 1000 * self.boss_number  # ボス番号に応じたスコア
                    
        return 0  # スコア変化なし
        
    def update_movement(self):
        """ボスの移動パターンを更新"""
        self.move_time += 1
        
        # 20秒ごとに移動パターンを変更
        if self.move_time >= 1200:
            self.move_time = 0
            self.move_pattern = (self.move_pattern + 1) % 3
            
        # パターン0: 左右移動
        if self.move_pattern == 0:
            self.x += math.sin(self.move_time / 60) * self.speed
            
        # パターン1: 円運動
        elif self.move_pattern == 1:
            center_x = SCREEN_WIDTH / 2
            center_y = 80
            radius = 50
            self.x = center_x + math.cos(self.move_time / 120) * radius
            self.y = center_y + math.sin(self.move_time / 120) * radius / 2
            
        # パターン2: 八の字
        elif self.move_pattern == 2:
            center_x = SCREEN_WIDTH / 2
            center_y = 80
            self.x = center_x + math.sin(self.move_time / 60) * 60
            self.y = center_y + math.sin(self.move_time / 30) * 20
            
        # 画面外に出ないように制限
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT / 2, self.y))
        
    def attack(self, enemy_bullets, player):
        """ボスの攻撃パターン"""
        # 基本パターン: 複数の弾を発射
        center_x = self.x + self.width / 2
        bottom_y = self.y + self.height
        
        # 攻撃レベルに応じた弾の数
        bullet_count = min(3 + self.attack_level, 12)
        
        # 基本的な放射状の弾
        for i in range(bullet_count):
            angle = (i * (360 / bullet_count)) * (math.pi / 180)
            bullet_x = center_x + math.cos(angle) * 10
            bullet_y = bottom_y + math.sin(angle) * 10
            
            # 弾の速度計算（プレイヤー方向を優先）
            dx = player.x + player.width/2 - bullet_x
            dy = player.y + player.height/2 - bullet_y
            
            # 全方向に撃つか、プレイヤー方向に集中するかをボスレベルで変える
            player_homing = min(self.boss_number / 10, 0.7)  # 最大70%まで誘導性を高める
            random_spread = 1.0 - player_homing
            
            # 速度計算（プレイヤー追尾と全方向のブレンド）
            if dx != 0 or dy != 0:
                length = math.sqrt(dx*dx + dy*dy)
                dx = dx / length
                dy = dy / length
                
                # プレイヤー方向と全方向をブレンド
                vx = dx * player_homing + math.cos(angle) * random_spread
                vy = dy * player_homing + math.sin(angle) * random_spread
                
                # 正規化
                vlength = math.sqrt(vx*vx + vy*vy)
                if vlength > 0:
                    vx = vx / vlength * 2  # 速度係数
                    vy = vy / vlength * 2
                    
                # ボスレベルに応じて弾の速度を上げる
                speed_factor = 1.0 + 0.1 * self.boss_number
                
                # 弾を作成して追加
                bullet = EnemyBullet(bullet_x, bullet_y)
                bullet.speed_x = vx * speed_factor
                bullet.speed_y = vy * speed_factor
                enemy_bullets.append(bullet)
        
    def draw(self):
        """ボスを描画する"""
        if not self.active:
            return
            
        # 退場フェーズで爆発エフェクト
        if self.exit_phase:
            # 複数の爆発を表示
            for _ in range(3):
                explosion_x = self.x + random.randint(0, self.width)
                explosion_y = self.y + random.randint(0, self.height)
                size = random.randint(3, 8)
                pyxel.circ(explosion_x, explosion_y, size, RED)
                pyxel.circ(explosion_x, explosion_y, size-1, YELLOW)
            return
            
        # ダメージ時の点滅
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer % 2 == 0:
                return  # 点滅して一瞬表示しない
        
        # 共通描画処理
        self.draw_boss_shape()
        
        # 体力ゲージ（より目立つように改良）
        health_ratio = self.health / self.max_health
        bar_width = self.width
        filled_width = int(bar_width * health_ratio)
        
        # ゲージの背景（黒）
        pyxel.rect(self.x, self.y - 7, bar_width, 5, BLACK)
        
        # 現在の体力（赤）
        pyxel.rect(self.x, self.y - 7, filled_width, 5, RED)
        
        # ゲージの枠線
        pyxel.rectb(self.x - 1, self.y - 8, bar_width + 2, 7, WHITE)
        
        # 体力の段階に応じて色を変える
        if health_ratio < 0.2:  # 残り20%未満で点滅
            if pyxel.frame_count % 4 < 2:
                pyxel.rect(self.x, self.y - 7, filled_width, 5, YELLOW)
                
        # ボスの名前と体力値を表示
        boss_name = getattr(self, 'name', f"Boss {self.boss_number}")
        health_text = f"{int(health_ratio * 100)}%"
        
        # 画面上部にボス情報を表示
        pyxel.text(5, 5, f"{boss_name}", WHITE)
        pyxel.text(SCREEN_WIDTH - 40, 5, f"HP: {health_text}", 
                  YELLOW if health_ratio < 0.3 else WHITE)
        
    def draw_boss_shape(self):
        """ボスの基本形状を描画する（派生クラスでオーバーライド）"""
        # 基本的な直方体ロボットを描画
        pyxel.rect(self.x, self.y, self.width, self.height, self.color_main)
        
        # 頭部
        head_width = self.width * 0.6
        head_height = self.height * 0.3
        head_x = self.x + (self.width - head_width) / 2
        head_y = self.y
        pyxel.rect(head_x, head_y, head_width, head_height, self.color_sub)
        
        # 目
        eye_size = max(2, int(self.width * 0.05))
        eye_y = head_y + head_height * 0.3
        eye_space = head_width * 0.3
        pyxel.rect(head_x + head_width/2 - eye_space - eye_size, eye_y, eye_size*2, eye_size, RED)
        pyxel.rect(head_x + head_width/2 + eye_space - eye_size, eye_y, eye_size*2, eye_size, RED)
        
        # 胴体
        body_width = self.width * 0.8
        body_height = self.height * 0.5
        body_x = self.x + (self.width - body_width) / 2
        body_y = self.y + head_height
        pyxel.rect(body_x, body_y, body_width, body_height, self.color_main)
        
        # 装甲部分
        armor_width = body_width * 0.6
        armor_height = body_height * 0.3
        armor_x = body_x + (body_width - armor_width) / 2
        armor_y = body_y + body_height * 0.3
        pyxel.rect(armor_x, armor_y, armor_width, armor_height, self.color_sub)
        
        # 下部
        bottom_width = self.width * 0.7
        bottom_height = self.height * 0.2
        bottom_x = self.x + (self.width - bottom_width) / 2
        bottom_y = self.y + head_height + body_height
        pyxel.rect(bottom_x, bottom_y, bottom_width, bottom_height, self.color_main)

# 10種類のボスクラスを定義（各ボスは特有の形状と攻撃パターンを持つ）
class Boss1(Boss):
    """ボス1: スピードタイプ - 素早い動きと単発攻撃"""
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.name = "Speed Demon"
        self.speed = 1.2  # 速い
        
    def draw_boss_shape(self):
        # 細長いスピード型ボスデザイン
        # 基本形状
        pyxel.rect(self.x, self.y, self.width, self.height, self.color_main)
        
        # 先端部（とがった形状）
        pyxel.tri(
            self.x + self.width/2, self.y,  # 上部中央
            self.x, self.y + self.height/3,  # 左下
            self.x + self.width, self.y + self.height/3,  # 右下
            self.color_sub
        )
        
        # 胴体
        body_width = self.width * 0.8
        body_x = self.x + (self.width - body_width)/2
        pyxel.rect(body_x, self.y + self.height/3, body_width, self.height * 0.4, self.color_main)
        
        # エンジン部
        engine_width = self.width * 0.5
        engine_x = self.x + (self.width - engine_width)/2
        pyxel.rect(engine_x, self.y + self.height * 0.7, engine_width, self.height * 0.3, self.color_sub)
        
        # 発光部（目）
        eye_size = max(2, self.width * 0.06)
        pyxel.circ(self.x + self.width * 0.3, self.y + self.height * 0.25, eye_size, RED)
        pyxel.circ(self.x + self.width * 0.7, self.y + self.height * 0.25, eye_size, RED)
        
    def attack(self, enemy_bullets, player):
        # 速い単発ショット（プレイヤーの方向に）
        bullet_count = 3
        center_x = self.x + self.width/2
        bottom_y = self.y + self.height
        
        for i in range(bullet_count):
            offset = (i - bullet_count//2) * 10
            bullet = EnemyBullet(center_x + offset, bottom_y)
            
            # プレイヤー方向に発射
            dx = player.x + player.width/2 - (center_x + offset)
            dy = player.y + player.height/2 - bottom_y
            
            if dx != 0 or dy != 0:
                length = math.sqrt(dx*dx + dy*dy)
                bullet.speed_x = dx / length * 3  # 高速弾
                bullet.speed_y = dy / length * 3
                enemy_bullets.append(bullet)

class Boss2(Boss):
    """ボス2: 拡散タイプ - 複数の弾を一度に発射"""
    def __init__(self, x, y):
        super().__init__(x, y, 2)
        self.name = "Spreading Terror"
        self.attack_interval = 90  # 攻撃頻度を低く
        
    def draw_boss_shape(self):
        # 六角形のような形状
        # 六角形の中心点
        cx = self.x + self.width/2
        cy = self.y + self.height/2
        
        # 六角形の各頂点
        r = min(self.width, self.height) * 0.4
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points.append((px, py))
        
        # 六角形の描画
        for i in range(6):
            pyxel.tri(
                cx, cy,  # 中心
                points[i][0], points[i][1],  # 現在の頂点
                points[(i+1)%6][0], points[(i+1)%6][1],  # 次の頂点
                self.color_main
            )
        
        # 中心の円
        pyxel.circ(cx, cy, r * 0.5, self.color_sub)
        
        # 円の中の十字
        line_length = r * 0.3
        pyxel.line(cx - line_length, cy, cx + line_length, cy, RED)
        pyxel.line(cx, cy - line_length, cx, cy + line_length, RED)
        
    def attack(self, enemy_bullets, player):
        # 扇状に広がる弾幕
        bullet_count = 12
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        for i in range(bullet_count):
            angle = (i * (360 / bullet_count)) * (math.pi / 180)
            bullet = EnemyBullet(center_x, center_y)
            bullet.speed_x = math.cos(angle) * 1.5
            bullet.speed_y = math.sin(angle) * 1.5
            enemy_bullets.append(bullet)

class Boss3(Boss):
    """ボス3: 追尾タイプ - プレイヤーを追いかける弾"""
    def __init__(self, x, y):
        super().__init__(x, y, 3)
        self.name = "Tracking Eye"
        
    def draw_boss_shape(self):
        # 目玉のような形状
        cx = self.x + self.width/2
        cy = self.y + self.height/2
        
        # 外側の白目
        r_outer = min(self.width, self.height) * 0.45
        pyxel.circ(cx, cy, r_outer, WHITE)
        
        # 虹彩
        r_iris = r_outer * 0.7
        pyxel.circ(cx, cy, r_iris, self.color_sub)
        
        # 黒目
        r_pupil = r_iris * 0.6
        pyxel.circ(cx, cy, r_pupil, BLACK)
        
        # ハイライト
        r_highlight = r_pupil * 0.3
        pyxel.circ(cx - r_pupil*0.3, cy - r_pupil*0.3, r_highlight, WHITE)
        
    def attack(self, enemy_bullets, player):
        # プレイヤーをしっかり追尾する弾
        bullet_count = 4
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        for i in range(bullet_count):
            bullet = EnemyBullet(center_x, center_y)
            
            # プレイヤー方向に発射
            dx = player.x + player.width/2 - center_x
            dy = player.y + player.height/2 - center_y
            
            if dx != 0 or dy != 0:
                length = math.sqrt(dx*dx + dy*dy)
                bullet.speed_x = dx / length * 1.8
                bullet.speed_y = dy / length * 1.8
                enemy_bullets.append(bullet)

class Boss4(Boss):
    """ボス4: シールドタイプ - 高耐久力で防御力が高い"""
    def __init__(self, x, y):
        super().__init__(x, y, 4)
        self.name = "Iron Fortress"
        # 基本体力に追加の係数を掛ける（すでに2^3=8倍になっているものを1.5倍に）
        self.max_health = int(self.max_health * 1.5)  
        self.health = self.max_health
        
    def draw_boss_shape(self):
        # 重装甲タイプの四角いロボット
        # 基本形状
        pyxel.rect(self.x, self.y, self.width, self.height, self.color_sub)
        
        # 装甲プレート（複数の長方形で表現）
        plate_count = 5
        plate_height = self.height / plate_count
        for i in range(plate_count):
            y = self.y + i * plate_height
            if i % 2 == 0:
                pyxel.rect(self.x, y, self.width, plate_height, self.color_main)
        
        # 中央の砲台
        turret_size = min(self.width, self.height) * 0.2
        cx = self.x + self.width/2
        cy = self.y + self.height/2
        
        pyxel.rect(cx - turret_size/2, cy - turret_size/2, 
                  turret_size, turret_size, RED)
        
        # 砲身
        pyxel.rect(cx - turret_size/4, cy - turret_size/4, 
                  turret_size/2, self.height/2, self.color_main)
        
    def attack(self, enemy_bullets, player):
        # 放射状の弾と直線的な弾の組み合わせ
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # 放射状の弾
        for angle in range(0, 360, 60):
            rad = angle * (math.pi / 180)
            bullet = EnemyBullet(center_x, center_y)
            bullet.speed_x = math.cos(rad) * 1.5
            bullet.speed_y = math.sin(rad) * 1.5
            enemy_bullets.append(bullet)
        
        # プレイヤー方向に直線弾
        bullet = EnemyBullet(center_x, center_y)
        dx = player.x + player.width/2 - center_x
        dy = player.y + player.height/2 - center_y
        
        if dx != 0 or dy != 0:
            length = math.sqrt(dx*dx + dy*dy)
            bullet.speed_x = dx / length * 2
            bullet.speed_y = dy / length * 2
            enemy_bullets.append(bullet)

class Boss5(Boss):
    """ボス5: 分裂タイプ - 弾が途中で分裂する特徴を持つ"""
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.name = "Division Matrix"
        self.split_bullets = []
        
    def draw_boss_shape(self):
        # 細胞分裂のような形状
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # 複数の球体
        radius = min(self.width, self.height) * 0.25
        offsets = [
            (0, 0),
            (radius*0.8, radius*0.8),
            (-radius*0.8, radius*0.8),
            (radius*0.8, -radius*0.8),
            (-radius*0.8, -radius*0.8)
        ]
        
        for ox, oy in offsets:
            pyxel.circ(center_x + ox, center_y + oy, radius, self.color_main)
            pyxel.circb(center_x + ox, center_y + oy, radius, self.color_sub)
            
            # 内部の模様
            r2 = radius * 0.6
            pyxel.circ(center_x + ox, center_y + oy, r2, self.color_sub)
            
    def update(self, player_bullets, enemy_bullets, player):
        result = super().update(player_bullets, enemy_bullets, player)
        
        # 分裂弾の処理
        for bullet in self.split_bullets[:]:
            bullet['timer'] -= 1
            if bullet['timer'] <= 0:
                self.split_bullets.remove(bullet)
                
                # 弾を分裂させる
                for angle in range(0, 360, 60):
                    rad = angle * (math.pi / 180)
                    new_bullet = EnemyBullet(bullet['x'], bullet['y'])
                    new_bullet.speed_x = math.cos(rad) * 1.5
                    new_bullet.speed_y = math.sin(rad) * 1.5
                    enemy_bullets.append(new_bullet)
        
        return result
        
    def attack(self, enemy_bullets, player):
        # 分裂する弾を発射
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # プレイヤー方向に弾を発射
        dx = player.x + player.width/2 - center_x
        dy = player.y + player.height/2 - center_y
        
        if dx != 0 or dy != 0:
            length = math.sqrt(dx*dx + dy*dy)
            
            # 分裂タイマーとともに弾情報を記録
            self.split_bullets.append({
                'x': center_x + dx/length * 40,  # 少し前に進んだ位置で分裂
                'y': center_y + dy/length * 40,
                'timer': 30  # 30フレーム後に分裂
            })
            
            # 最初の弾
            bullet = EnemyBullet(center_x, center_y)
            bullet.speed_x = dx / length * 2
            bullet.speed_y = dy / length * 2
            enemy_bullets.append(bullet)

# ボス6〜10の実装 - それぞれユニークな形状と攻撃パターンを持つ
class Boss6(Boss):
    """ボス6: レーザータイプ - 直線的で強力なレーザーを発射"""
    def __init__(self, x, y):
        super().__init__(x, y, 6)
        self.name = "Laser Overlord"
        self.laser_charge = 0
        self.laser_active = False
        self.laser_direction = 0
        self.laser_width = 5
        
    def draw_boss_shape(self):
        # とがった形状のロボット
        # 基本三角形
        pyxel.tri(
            self.x + self.width/2, self.y,  # 上部
            self.x, self.y + self.height,  # 左下
            self.x + self.width, self.y + self.height,  # 右下
            self.color_main
        )
        
        # 内部の機械部分
        inner_width = self.width * 0.6
        inner_height = self.height * 0.6
        inner_x = self.x + (self.width - inner_width)/2
        inner_y = self.y + (self.height - inner_height)/2
        
        pyxel.rect(inner_x, inner_y, inner_width, inner_height, self.color_sub)
        
        # レーザー射出口
        canon_width = self.width * 0.2
        canon_height = self.height * 0.1
        canon_x = self.x + (self.width - canon_width)/2
        canon_y = self.y + self.height - canon_height
        
        pyxel.rect(canon_x, canon_y, canon_width, canon_height, RED)
        
        # レーザー充電中の表現
        if self.laser_charge > 0:
            charge_radius = self.laser_charge / 60 * (self.width * 0.1)
            pyxel.circ(self.x + self.width/2, canon_y + canon_height/2, 
                      charge_radius, RED)
        
        # レーザー発射中の表現
        if self.laser_active:
            laser_length = SCREEN_HEIGHT
            end_x = self.x + self.width/2 + math.cos(self.laser_direction) * laser_length
            end_y = canon_y + canon_height/2 + math.sin(self.laser_direction) * laser_length
            
            pyxel.line(self.x + self.width/2, canon_y + canon_height/2,
                      end_x, end_y, RED)
            
    def update(self, player_bullets, enemy_bullets, player):
        result = super().update(player_bullets, enemy_bullets, player)
        
        # レーザー充電中
        if self.laser_charge > 0:
            self.laser_charge -= 1
            
            # 充電完了
            if self.laser_charge == 0:
                self.laser_active = True
                
                # プレイヤー方向にレーザーを発射
                center_x = self.x + self.width/2
                bottom_y = self.y + self.height
                
                dx = player.x + player.width/2 - center_x
                dy = player.y + player.height/2 - bottom_y
                
                if dx != 0 or dy != 0:
                    self.laser_direction = math.atan2(dy, dx)
        
        # レーザー発射中
        if self.laser_active:
            # レーザーに当たっているかチェック
            center_x = self.x + self.width/2
            canon_y = self.y + self.height - self.height * 0.1
            
            laser_end_x = center_x + math.cos(self.laser_direction) * SCREEN_HEIGHT
            laser_end_y = canon_y + math.sin(self.laser_direction) * SCREEN_HEIGHT
            
            # プレイヤーとレーザーの衝突判定（単純化）
            player_center_x = player.x + player.width/2
            player_center_y = player.y + player.height/2
            
            # 直線と点の距離を計算
            a = laser_end_y - canon_y
            b = center_x - laser_end_x
            c = laser_end_x * canon_y - center_x * laser_end_y
            
            distance = abs(a * player_center_x + b * player_center_y + c) / math.sqrt(a*a + b*b)
            
            if distance < self.laser_width + player.width/2:
                # レーザーに当たった
                player.hit()
            
            # レーザー発射は1フレームのみ
            self.laser_active = False
        
        return result
        
    def attack(self, enemy_bullets, player):
        # 通常弾発射
        super().attack(enemy_bullets, player)
        
        # レーザー充電開始
        if random.random() < 0.2 and self.laser_charge == 0 and not self.laser_active:
            self.laser_charge = 60  # 60フレーム(1秒)の充電

class Boss7(Boss):
    """ボス7: 時間停止タイプ - 一時的にプレイヤーの動きを制限する効果を持つ"""
    def __init__(self, x, y):
        super().__init__(x, y, 7)
        self.name = "Chrono Disruptor"
        self.time_stop_cooldown = 0
        self.time_stop_active = False
        
    def draw_boss_shape(self):
        # 時計のような形状
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        radius = min(self.width, self.height) * 0.4
        
        # 時計の外枠
        pyxel.circ(center_x, center_y, radius, self.color_main)
        pyxel.circb(center_x, center_y, radius, self.color_sub)
        
        # 文字盤
        inner_radius = radius * 0.85
        pyxel.circ(center_x, center_y, inner_radius, self.color_sub)
        
        # 時針と分針
        angle1 = self.move_time / 120 * math.pi * 2
        angle2 = self.move_time / 30 * math.pi * 2
        
        hand1_length = inner_radius * 0.6
        hand2_length = inner_radius * 0.8
        
        pyxel.line(center_x, center_y,
                  center_x + math.cos(angle1) * hand1_length,
                  center_y + math.sin(angle1) * hand1_length,
                  RED)
                  
        pyxel.line(center_x, center_y,
                  center_x + math.cos(angle2) * hand2_length,
                  center_y + math.sin(angle2) * hand2_length,
                  BLACK)
        
        # 中心点
        pyxel.circ(center_x, center_y, 3, RED)
        
        # 時間停止中のエフェクト
        if self.time_stop_active:
            for i in range(8):
                angle = i * math.pi / 4
                pyxel.line(center_x, center_y,
                          center_x + math.cos(angle) * radius * 1.2,
                          center_y + math.sin(angle) * radius * 1.2,
                          WHITE)
                          
    def update(self, player_bullets, enemy_bullets, player):
        result = super().update(player_bullets, enemy_bullets, player)
        
        # 時間停止のクールダウン
        if self.time_stop_cooldown > 0:
            self.time_stop_cooldown -= 1
            
        # 時間停止の効果適用（プレイヤーの速度を遅くする）
        if self.time_stop_active:
            player.speed = player.base_speed * 0.3  # 30%の速度に
        
        return result
        
    def attack(self, enemy_bullets, player):
        # 通常攻撃
        super().attack(enemy_bullets, player)
        
        # 時間停止の発動
        if random.random() < 0.05 and self.time_stop_cooldown == 0:
            self.time_stop_cooldown = 300  # 5秒のクールダウン
            self.time_stop_active = True
            
            # 3秒間の時間停止
            pyxel.schedule(lambda: setattr(self, 'time_stop_active', False), 180)

class Boss8(Boss):
    """ボス8: 重力タイプ - 弾や障害物を引き寄せたり反発させる力を持つ"""
    def __init__(self, x, y):
        super().__init__(x, y, 8)
        self.name = "Gravity Well"
        self.gravity_field_active = False
        self.gravity_timer = 0
        self.gravity_type = 0  # 0: 引力, 1: 斥力
        
    def draw_boss_shape(self):
        # 球体のような形状
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        radius = min(self.width, self.height) * 0.4
        
        # 外側の球体
        pyxel.circ(center_x, center_y, radius, self.color_main)
        
        # 内側のコア
        inner_radius = radius * 0.6
        pyxel.circ(center_x, center_y, inner_radius, self.color_sub)
        
        # 重力場の表現
        if self.gravity_field_active:
            for i in range(5):
                field_radius = radius * (1 + i * 0.3)
                color = RED if self.gravity_type == 0 else CYAN  # 引力は赤、斥力は青
                pyxel.circb(center_x, center_y, field_radius, color)
                
    def update(self, player_bullets, enemy_bullets, player):
        result = super().update(player_bullets, enemy_bullets, player)
        
        # 重力場の処理
        if self.gravity_field_active:
            center_x = self.x + self.width/2
            center_y = self.y + self.height/2
            
            # 重力タイマー更新
            self.gravity_timer += 1
            if self.gravity_timer >= 180:  # 3秒間効果継続
                self.gravity_field_active = False
                self.gravity_timer = 0
                
            # 重力効果の適用
            gravity_range = min(self.width, self.height) * 2
            
            # プレイヤーへの重力効果
            player_dx = player.x + player.width/2 - center_x
            player_dy = player.y + player.height/2 - center_y
            player_dist = math.sqrt(player_dx*player_dx + player_dy*player_dy)
            
            if player_dist < gravity_range and player_dist > 0:
                force = (gravity_range - player_dist) / gravity_range * 0.5
                if self.gravity_type == 0:  # 引力
                    player.x -= player_dx / player_dist * force
                    player.y -= player_dy / player_dist * force
                else:  # 斥力
                    player.x += player_dx / player_dist * force
                    player.y += player_dy / player_dist * force
                    
            # 弾への重力効果（敵の弾）
            for bullet in enemy_bullets:
                bullet_dx = bullet.x - center_x
                bullet_dy = bullet.y - center_y
                bullet_dist = math.sqrt(bullet_dx*bullet_dx + bullet_dy*bullet_dy)
                
                if bullet_dist < gravity_range and bullet_dist > 0:
                    force = (gravity_range - bullet_dist) / gravity_range * 0.02
                    if self.gravity_type == 0:  # 引力
                        bullet.speed_x -= bullet_dx / bullet_dist * force
                        bullet.speed_y -= bullet_dy / bullet_dist * force
                    else:  # 斥力
                        bullet.speed_x += bullet_dx / bullet_dist * force
                        bullet.speed_y += bullet_dy / bullet_dist * force
        
        return result
        
    def attack(self, enemy_bullets, player):
        # 通常攻撃
        if not self.gravity_field_active:
            super().attack(enemy_bullets, player)
        
        # 重力場の発動
        if random.random() < 0.03 and not self.gravity_field_active:
            self.gravity_field_active = True
            self.gravity_timer = 0
            self.gravity_type = random.randint(0, 1)  # ランダムに引力か斥力を選択

class Boss9(Boss):
    """ボス9: ミラージュタイプ - 分身して攻撃するボス"""
    def __init__(self, x, y):
        super().__init__(x, y, 9)
        self.name = "Phantom Echo"
        self.clones = []
        self.clone_timer = 0
        
    def draw_boss_shape(self):
        # 半透明のような形状
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # 基本形状（細長い）
        height_ratio = 1.5
        width_ratio = 0.7
        
        adjusted_height = self.height * height_ratio
        adjusted_width = self.width * width_ratio
        
        # 中心位置から調整
        adj_x = center_x - adjusted_width/2
        adj_y = center_y - adjusted_height/2
        
        # 本体
        pyxel.rect(adj_x, adj_y, adjusted_width, adjusted_height, self.color_main)
        
        # 頭部
        head_width = adjusted_width * 0.8
        head_height = adjusted_height * 0.2
        head_x = center_x - head_width/2
        head_y = adj_y
        
        pyxel.rect(head_x, head_y, head_width, head_height, self.color_sub)
        
        # 目
        eye_y = head_y + head_height * 0.5
        eye_width = head_width * 0.15
        eye_spacing = head_width * 0.3
        
        pyxel.rect(center_x - eye_spacing - eye_width/2, eye_y - eye_width/2,
                  eye_width, eye_width, RED)
        pyxel.rect(center_x + eye_spacing - eye_width/2, eye_y - eye_width/2,
                  eye_width, eye_width, RED)
        
        # クローンの描画
        for clone in self.clones:
            clone_x = clone['x']
            clone_y = clone['y']
            clone_center_x = clone_x + self.width/2
            clone_center_y = clone_y + self.height/2
            
            # クローン本体（半透明表現）
            adj_clone_x = clone_center_x - adjusted_width/2
            adj_clone_y = clone_center_y - adjusted_height/2
            
            pyxel.rect(adj_clone_x, adj_clone_y, 
                     adjusted_width, adjusted_height, self.color_sub)
            
            # クローンの頭部
            clone_head_x = clone_center_x - head_width/2
            clone_head_y = adj_clone_y
            
            pyxel.rect(clone_head_x, clone_head_y, head_width, head_height, self.color_main)
            
            # クローンの目
            clone_eye_y = clone_head_y + head_height * 0.5
            
            pyxel.rect(clone_center_x - eye_spacing - eye_width/2, 
                      clone_eye_y - eye_width/2,
                      eye_width, eye_width, RED)
            pyxel.rect(clone_center_x + eye_spacing - eye_width/2, 
                      clone_eye_y - eye_width/2,
                      eye_width, eye_width, RED)
                
    def update(self, player_bullets, enemy_bullets, player):
        result = super().update(player_bullets, enemy_bullets, player)
        
        # クローンのタイマー更新
        self.clone_timer += 1
        if self.clone_timer >= 300:  # 5秒ごとにクローン更新
            self.clone_timer = 0
            
            # クローン作成
            self.clones = []
            
            # 2-3体のクローン作成
            clone_count = random.randint(2, 3)
            for _ in range(clone_count):
                # ランダムな位置
                clone_x = random.randint(0, SCREEN_WIDTH - self.width)
                clone_y = random.randint(10, int(SCREEN_HEIGHT/2 - self.height))
                
                self.clones.append({
                    'x': clone_x,
                    'y': clone_y,
                    'attack_timer': random.randint(60, 120)
                })
        
        # クローンの更新
        for clone in self.clones[:]:
            clone['attack_timer'] -= 1
            
            # 攻撃タイミング
            if clone['attack_timer'] <= 0:
                # クローンから攻撃
                center_x = clone['x'] + self.width/2
                center_y = clone['y'] + self.height/2
                
                # プレイヤー方向に弾発射
                dx = player.x + player.width/2 - center_x
                dy = player.y + player.height/2 - center_y
                
                if dx != 0 or dy != 0:
                    bullet = EnemyBullet(center_x, center_y)
                    length = math.sqrt(dx*dx + dy*dy)
                    bullet.speed_x = dx / length * 2
                    bullet.speed_y = dy / length * 2
                    enemy_bullets.append(bullet)
                
                # リセット
                clone['attack_timer'] = random.randint(120, 180)
        
        return result
        
    def attack(self, enemy_bullets, player):
        # 本体の攻撃（通常攻撃よりも弱め）
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # 放射状の弾
        angle_count = 4
        for i in range(angle_count):
            angle = (i * (360 / angle_count)) * (math.pi / 180)
            bullet = EnemyBullet(center_x, center_y)
            bullet.speed_x = math.cos(angle) * 1.5
            bullet.speed_y = math.sin(angle) * 1.5
            enemy_bullets.append(bullet)

class Boss10(Boss):
    """ボス10: 最終ボス - すべての能力を兼ね備えた最強のボス"""
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.name = "Ultimate Destroyer"
        self.phase = 0  # 0-2の3段階
        self.phase_health = self.max_health / 3
        
        # 各種攻撃モードの状態
        self.attack_mode = 0
        self.attack_mode_timer = 0
        
    def draw_boss_shape(self):
        # 複雑な形状の最終ボス
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # フェーズに応じた色
        phase_colors = [RED, ORANGE, YELLOW]
        current_color = phase_colors[min(self.phase, len(phase_colors)-1)]
        
        # 基本形状（大きな六角形）
        radius = min(self.width, self.height) * 0.4
        points = []
        
        for i in range(6):
            angle = i * math.pi / 3
            px = center_x + radius * math.cos(angle)
            py = center_y + radius * math.sin(angle)
            points.append((px, py))
        
        # 六角形を埋めるように描画
        for i in range(6):
            pyxel.tri(
                center_x, center_y,
                points[i][0], points[i][1],
                points[(i+1)%6][0], points[(i+1)%6][1],
                self.color_main
            )
            
        # 内側の要素
        inner_radius = radius * 0.7
        
        # フェーズに応じた内部形状
        if self.phase == 0:
            # フェーズ1: 円
            pyxel.circ(center_x, center_y, inner_radius, current_color)
        elif self.phase == 1:
            # フェーズ2: 星
            star_points = []
            for i in range(5):
                # 外側の点
                angle_outer = i * 2 * math.pi / 5
                px_outer = center_x + inner_radius * math.cos(angle_outer)
                py_outer = center_y + inner_radius * math.sin(angle_outer)
                star_points.append((px_outer, py_outer))
                
                # 内側の点
                angle_inner = angle_outer + math.pi / 5
                px_inner = center_x + inner_radius * 0.4 * math.cos(angle_inner)
                py_inner = center_y + inner_radius * 0.4 * math.sin(angle_inner)
                star_points.append((px_inner, py_inner))
            
            # 星形を描画
            for i in range(0, 10, 2):
                pyxel.tri(
                    center_x, center_y,
                    star_points[i][0], star_points[i][1],
                    star_points[(i+1)%10][0], star_points[(i+1)%10][1],
                    current_color
                )
                pyxel.tri(
                    center_x, center_y,
                    star_points[(i+1)%10][0], star_points[(i+1)%10][1],
                    star_points[(i+2)%10][0], star_points[(i+2)%10][1],
                    current_color
                )
        else:
            # フェーズ3: クロス
            cross_size = inner_radius * 0.8
            pyxel.rect(center_x - cross_size/4, center_y - cross_size,
                      cross_size/2, cross_size*2, current_color)
            pyxel.rect(center_x - cross_size, center_y - cross_size/4,
                      cross_size*2, cross_size/2, current_color)
        
        # 中央のコア
        core_radius = inner_radius * 0.3
        pyxel.circ(center_x, center_y, core_radius, self.color_sub)
        pyxel.circb(center_x, center_y, core_radius, WHITE)
        
        # フェーズ表示
        phase_text = f"PHASE {self.phase + 1}"
        text_x = center_x - len(phase_text) * 2
        text_y = self.y - 10
        pyxel.text(text_x, text_y, phase_text, WHITE)
        
    def update(self, player_bullets, enemy_bullets, player):
        result = super().update(player_bullets, enemy_bullets, player)
        
        # フェーズの更新
        current_phase = min(2, 2 - (self.health // self.phase_health))
        
        # フェーズが変わった時
        if current_phase != self.phase:
            self.phase = current_phase
            # フェーズ変更時のエフェクト
            print(f"Boss entering Phase {self.phase + 1}")
            
            # フェーズ変更時に短い無敵時間
            self.invulnerable = True
            pyxel.schedule(lambda: setattr(self, 'invulnerable', False), 60)
            
            # 攻撃モードをリセット
            self.attack_mode = 0
            self.attack_mode_timer = 0
        
        # 攻撃モードの更新
        self.attack_mode_timer += 1
        if self.attack_mode_timer >= 180:  # 3秒ごとに攻撃モード変更
            self.attack_mode_timer = 0
            self.attack_mode = (self.attack_mode + 1) % 3
        
        return result
        
    def attack(self, enemy_bullets, player):
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # フェーズとモードに応じた攻撃
        if self.phase == 0:
            # フェーズ1: 基本的な攻撃パターン
            if self.attack_mode == 0:
                # モード1: 放射状攻撃
                bullet_count = 8
                for i in range(bullet_count):
                    angle = (i * (360 / bullet_count)) * (math.pi / 180)
                    bullet = EnemyBullet(center_x, center_y)
                    bullet.speed_x = math.cos(angle) * 1.8
                    bullet.speed_y = math.sin(angle) * 1.8
                    enemy_bullets.append(bullet)
                    
            elif self.attack_mode == 1:
                # モード2: プレイヤー追尾
                bullet = EnemyBullet(center_x, center_y)
                dx = player.x + player.width/2 - center_x
                dy = player.y + player.height/2 - center_y
                
                if dx != 0 or dy != 0:
                    length = math.sqrt(dx*dx + dy*dy)
                    bullet.speed_x = dx / length * 2.5
                    bullet.speed_y = dy / length * 2.5
                    enemy_bullets.append(bullet)
                    
            else:
                # モード3: 3方向攻撃
                for direction in [-1, 0, 1]:
                    bullet = EnemyBullet(center_x, center_y)
                    bullet.speed_x = direction * 1.5
                    bullet.speed_y = 2
                    enemy_bullets.append(bullet)
                    
        elif self.phase == 1:
            # フェーズ2: より強力な攻撃
            if self.attack_mode == 0:
                # モード1: 二重螺旋
                bullet_count = 12
                for i in range(bullet_count):
                    angle1 = (i * (360 / bullet_count) + self.move_time) * (math.pi / 180)
                    angle2 = (i * (360 / bullet_count) + self.move_time + 180) * (math.pi / 180)
                    
                    bullet1 = EnemyBullet(center_x, center_y)
                    bullet1.speed_x = math.cos(angle1) * 2
                    bullet1.speed_y = math.sin(angle1) * 2
                    enemy_bullets.append(bullet1)
                    
                    bullet2 = EnemyBullet(center_x, center_y)
                    bullet2.speed_x = math.cos(angle2) * 2
                    bullet2.speed_y = math.sin(angle2) * 2
                    enemy_bullets.append(bullet2)
                    
            elif self.attack_mode == 1:
                # モード2: 複数追尾弾
                for _ in range(3):
                    offset_x = random.randint(-20, 20)
                    offset_y = random.randint(-20, 20)
                    
                    bullet = EnemyBullet(center_x + offset_x, center_y + offset_y)
                    dx = player.x + player.width/2 - (center_x + offset_x)
                    dy = player.y + player.height/2 - (center_y + offset_y)
                    
                    if dx != 0 or dy != 0:
                        length = math.sqrt(dx*dx + dy*dy)
                        bullet.speed_x = dx / length * 3
                        bullet.speed_y = dy / length * 3
                        enemy_bullets.append(bullet)
                        
            else:
                # モード3: 弾幕
                for angle in range(0, 360, 30):
                    rad = angle * (math.pi / 180)
                    for speed in [1.5, 2.5]:
                        bullet = EnemyBullet(center_x, center_y)
                        bullet.speed_x = math.cos(rad) * speed
                        bullet.speed_y = math.sin(rad) * speed
                        enemy_bullets.append(bullet)
                        
        else:
            # フェーズ3: 最終形態
            if self.attack_mode == 0:
                # モード1: 全方向高密度弾幕
                bullet_count = 16
                for i in range(bullet_count):
                    angle = (i * (360 / bullet_count)) * (math.pi / 180)
                    for speed in [1.5, 2.5, 3.5]:
                        bullet = EnemyBullet(center_x, center_y)
                        bullet.speed_x = math.cos(angle) * speed
                        bullet.speed_y = math.sin(angle) * speed
                        enemy_bullets.append(bullet)
                        
            elif self.attack_mode == 1:
                # モード2: 追尾多重弾
                for i in range(5):
                    bullet = EnemyBullet(center_x, center_y)
                    dx = player.x + player.width/2 - center_x
                    dy = player.y + player.height/2 - center_y
                    
                    if dx != 0 or dy != 0:
                        length = math.sqrt(dx*dx + dy*dy)
                        speed = 1.5 + i * 0.4
                        bullet.speed_x = dx / length * speed
                        bullet.speed_y = dy / length * speed
                        enemy_bullets.append(bullet)
                        
            else:
                # モード3: ランダム弾幕
                for _ in range(10):
                    angle = random.random() * math.pi * 2
                    speed = 1.5 + random.random() * 2
                    
                    bullet = EnemyBullet(center_x, center_y)
                    bullet.speed_x = math.cos(angle) * speed
                    bullet.speed_y = math.sin(angle) * speed
                    enemy_bullets.append(bullet)

# ボスファクトリ関数 - 番号に応じたボスをインスタンス化
def create_boss(boss_number, x, y):
    """ボス番号に対応したボスを生成する"""
    boss_classes = [
        Boss1, Boss2, Boss3, Boss4, Boss5,
        Boss6, Boss7, Boss8, Boss9, Boss10
    ]
    
    if 1 <= boss_number <= 10:
        return boss_classes[boss_number-1](x, y)
    else:
        return Boss1(x, y)  # デフォルト