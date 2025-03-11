import pyxel
import random
from constants import *

class PowerUp:
    """パワーアップアイテムの基本クラス"""
    
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.speed = 1.0
        self.powerup_type = powerup_type
        self.animation_timer = 0
        
    def update(self):
        # 画面下に向かって移動
        self.y += self.speed
        
        # アニメーション用タイマー更新
        self.animation_timer += 1
        if self.animation_timer > 60:
            self.animation_timer = 0
    
    def draw(self):
        # アイテムのタイプに応じた色を選択
        if self.powerup_type == POWERUP_SPREAD:
            color = YELLOW  # スプレッド弾のアイテム
        elif self.powerup_type == POWERUP_POWER:
            color = RED     # パワーアップのアイテム
        elif self.powerup_type == POWERUP_SPEED:
            color = CYAN    # スピードアップのアイテム
        elif self.powerup_type == POWERUP_SHIELD:
            color = LIME    # シールドのアイテム
        else:
            color = WHITE   # デフォルト色
            
        # 点滅効果 (アニメーション用)
        if (self.animation_timer // 5) % 2 == 0:
            # ダイヤモンド形状のアイテムを描画
            pyxel.tri(
                self.x + self.width // 2, self.y,  # 上
                self.x, self.y + self.height // 2,  # 左
                self.x + self.width, self.y + self.height // 2,  # 右
                color
            )
            pyxel.tri(
                self.x + self.width // 2, self.y + self.height,  # 下
                self.x, self.y + self.height // 2,  # 左
                self.x + self.width, self.y + self.height // 2,  # 右
                color
            )
            
            # アイテムタイプの文字を表示
            if self.powerup_type == POWERUP_SPREAD:
                pyxel.text(self.x + 2, self.y + 3, "S", BLACK)
            elif self.powerup_type == POWERUP_POWER:
                pyxel.text(self.x + 2, self.y + 3, "P", BLACK)
            elif self.powerup_type == POWERUP_SPEED:
                pyxel.text(self.x + 2, self.y + 3, "+", BLACK)
            elif self.powerup_type == POWERUP_SHIELD:
                pyxel.text(self.x + 2, self.y + 3, "#", BLACK)

# パワーアップアイテムファクトリー関数
def create_random_powerup(x, y):
    """ランダムなパワーアップアイテムを生成"""
    # 黄色パワーアップ（POWERUP_YELLOW）の出現率を高くする
    if random.random() < 0.4:  # 40%の確率で黄色
        powerup_type = POWERUP_YELLOW
    else:
        # 残りは他のパワーアップからランダム選択
        powerup_type = random.choice([POWERUP_POWER, POWERUP_SPEED, POWERUP_SHIELD])
    
    print(f"DEBUG: Powerup created of type {powerup_type}")
    return PowerUp(x, y, powerup_type)