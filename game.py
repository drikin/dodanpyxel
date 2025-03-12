import pyxel
import random
import math
from constants import *
from player import Player
from enemy import SmallEnemy, MediumEnemy, LargeEnemy
from background import Background
from assets.sounds import init_sounds
from powerup import PowerUp, create_random_powerup
from boss import create_boss

class Game:
    def __init__(self):
        try:
            # Try current API (newer Pyxel versions)
            pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="DodanPyxel", fps=60, display_scale=3, 
                      capture_scale=1, capture_sec=0, quit_key=pyxel.KEY_NONE)
        except:
            try:
                # Try older API
                pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="DodanPyxel", fps=60, scale=3)
            except:
                # Absolute minimal initialization
                pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
                
        # Enable mouse input for touch
        try:
            pyxel.mouse(True)  # Enable mouse/touch input
        except:
            pass  # Some versions don't have this
        
        # Initialize sounds
        try:
            init_sounds()
        except Exception as e:
            print(f"Error initializing sounds: {e}")
            # Continue without sounds if there's an error
        
        # Load resources
        self.load_resources()
        
        # Game state
        self.state = STATE_TITLE
        
        # Create background
        self.background = Background()
        
        # Touch controls for mobile
        self.touch_enabled = False
        self.touch_start_x = 0
        self.touch_start_y = 0
        self.touch_current_x = 0
        self.touch_current_y = 0
        self.touch_shoot = True  # 自動発射をデフォルトで有効
        
        # For virtual touch controls display
        self.show_touch_controls = True
        
        # Initialize other game components
        self.reset_game()
        
    def load_resources(self):
        # Create resources (sprites are defined in assets/sprites.py)
        pass
    
    def reset_game(self):
        # Initialize bullet lists first (so they exist before player creation)
        self.player_bullets = []
        self.enemy_bullets = []
        
        # Player (with direct reference to this game instance)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20, self)
        
        # Enemies
        self.enemies = []
        self.enemy_timer = 0
        
        # Explosions
        self.explosions = []
        
        # パワーアップアイテム
        self.powerups = []
        
        # Score
        self.score = 0
        
        # Game variables
        self.frame_count = 0
        
        # ボス戦関連の変数
        self.boss_distance = 0  # 進んだ距離
        self.boss_timer = BOSS_DISTANCE_INTERVAL  # 次のボスまでの距離
        self.current_boss_number = 0  # 現在のボス番号（0=ボスなし、1-10=ボス番号）
        self.boss = None  # 現在のボスオブジェクト
        self.boss_clear_count = 0  # 倒したボスの数
        self.all_boss_cleared = False  # すべてのボスを倒したフラグ
        
        # ボスサイクルの設定（ボスを倒した後に次のボスサイクルが始まるか）
        self.boss_cycle_enabled = BOSS_CYCLE_ENABLED
        self.max_boss_in_cycle = 10  # 1サイクルの最大ボス数
        
        # サイクル完了メッセージ表示用の変数
        self.show_cycle_message = False
        self.cycle_message_timer = 0
        self.cycle_message = ""
        
        # 自動発射は常に有効にする
        self.touch_shoot = True
    
    def update(self):
        # Handle touch input for mobile devices
        self.process_touch_input()
            
        # Update based on game state
        if self.state == STATE_TITLE:
            self.update_title_screen()
        elif self.state == STATE_PLAYING:
            self.update_game()
        elif self.state == STATE_GAME_OVER:
            self.update_game_over()
            
        # Increment frame counter
        self.frame_count += 1
        
    def process_touch_input(self):
        # Check for mouse press as a proxy for touch in Pyxel
        if pyxel.btnp(MOUSE_BUTTON_LEFT):
            self.touch_enabled = True
            self.touch_start_x = pyxel.mouse_x
            self.touch_start_y = pyxel.mouse_y
            self.touch_current_x = pyxel.mouse_x
            self.touch_current_y = pyxel.mouse_y
            
            # Auto-shoot is active by default, but allow additional control
            # with touch in the bottom right corner
            self.touch_shoot = True  # Always enable auto-shooting
            
            # Additional touch control in bottom right still available
            if (pyxel.mouse_x > SCREEN_WIDTH - 30 and 
                pyxel.mouse_y > SCREEN_HEIGHT - 30):
                self.touch_shoot = True
            
            # Handle state transitions via touch
            if self.state == STATE_TITLE:
                self.state = STATE_PLAYING
                pyxel.play(0, 2)  # Play start sound
            elif self.state == STATE_GAME_OVER:
                self.reset_game()
                self.state = STATE_PLAYING
                
        # Update current touch position if touching
        elif pyxel.btn(MOUSE_BUTTON_LEFT) and self.touch_enabled:
            self.touch_current_x = pyxel.mouse_x
            self.touch_current_y = pyxel.mouse_y
            
            # Check shoot button
            if (pyxel.mouse_x > SCREEN_WIDTH - 30 and 
                pyxel.mouse_y > SCREEN_HEIGHT - 30):
                self.touch_shoot = True
                
        # Reset touch when released, but keep auto-shoot enabled
        elif pyxel.btnr(MOUSE_BUTTON_LEFT):
            self.touch_enabled = False
            # 自動発射は常に有効にしておく
            self.touch_shoot = True
    
    def update_title_screen(self):
        # Start game when SPACE is pressed
        if pyxel.btnp(KEY_SPACE):
            self.state = STATE_PLAYING
            pyxel.play(0, 2)  # Play start sound
    
    def update_game(self):
        # 自動発射フラグを確認して更新
        self.touch_shoot = True
        
        # Update background
        self.background.update()
        
        # Update player
        self.player.update()
        
        # サイクル完了メッセージのタイマー更新
        if self.show_cycle_message:
            self.cycle_message_timer -= 1
            if self.cycle_message_timer <= 0:
                self.show_cycle_message = False
        
        # 距離カウンターの更新（1フレームごとに距離を加算）
        self.boss_distance += 1
        
        # ボスの状態更新（ボスの弾との衝突判定はcheck_collisionsで行う）
        if self.boss and self.boss.active:
            # 移動などの単純な動作のみ更新（弾との判定は行わない）
            if self.boss.entry_phase:
                self.boss.y += 0.5  # ゆっくり下に移動
                if self.boss.y >= 50:  # 画面上部に到達したら登場フェーズ終了
                    self.boss.entry_phase = False
            elif self.boss.exit_phase:
                self.boss.y -= 2  # 上に退場
                if self.boss.y + self.boss.height < 0:  # 画面外に出たら
                    self.boss.active = False  # 非アクティブに
                    
                    # ボスが倒されて退場完了した場合
                    self.score += 1000 * self.boss.boss_number  # ボーナススコア
                    self.boss_clear_count += 1
                    
                    # 大規模な爆発エフェクト (ボス撃破演出)
                    from explosion import Explosion
                    # 複数箇所に爆発エフェクト
                    for _ in range(10):
                        ex = self.boss.x + random.randint(0, self.boss.width)
                        ey = self.boss.y + random.randint(0, self.boss.height)
                        self.explosions.append(Explosion(ex, ey))
                    
                    # ボス撃破報酬として追加ライフ
                    self.player.lives += BOSS_EXTRA_LIFE
                    
                    # 効果音
                    try:
                        pyxel.play(2, 3)  # ボス撃破音
                        # 連続して効果音を鳴らして豪華に
                        pyxel.play(1, 1)  # 爆発音1
                        pyxel.play(0, 1)  # 爆発音2
                    except:
                        pass
                    
                    # 次のボスの準備または全ボスクリア処理
                    next_boss_cycle = self.boss_cycle_enabled and self.boss_clear_count >= self.max_boss_in_cycle
                    
                    if next_boss_cycle:
                        # ボスサイクル完了 - 新しいサイクルを開始
                        print(f"DEBUG: Boss cycle completed! Starting new cycle.")
                        cycle_bonus = BOSS_CLEAR_BONUS * 2  # サイクル完了ボーナスは通常の2倍
                        self.score += cycle_bonus  # ボーナス得点
                        self.boss = None
                        self.boss_timer = BOSS_DISTANCE_INTERVAL
                        self.current_boss_number = 0
                        self.boss_clear_count = 0  # ボスカウントリセット
                        
                        # 祝福のメッセージを表示（5秒間表示）
                        self.show_cycle_message = True
                        self.cycle_message_timer = 300  # 5秒（60FPS × 5）
                        self.cycle_message = f"BOSS CYCLE COMPLETED! BONUS: {cycle_bonus}"
                        
                    elif self.boss_clear_count >= self.max_boss_in_cycle and not self.boss_cycle_enabled:
                        # サイクル無効時の全ボスクリア
                        self.all_boss_cleared = True
                        self.score += BOSS_CLEAR_BONUS  # ボーナス得点
                        self.boss = None
                    else:
                        # ボス撃破後、次のボスまでのタイマーをリセット
                        self.boss = None
                        self.boss_timer = BOSS_DISTANCE_INTERVAL
                        self.current_boss_number = 0
                        
                        # 通常の敵が再度出現し始める
            else:
                # 通常の移動パターン更新
                self.boss.update_movement()
                
                # 攻撃パターン更新
                self.boss.attack_timer += 1
                if self.boss.attack_timer >= self.boss.attack_interval:
                    self.boss.attack_timer = 0
                    self.boss.attack(self.enemy_bullets, self.player)
        
        # ボスが出現していない場合は、ボスタイマーを減らす
        elif not self.all_boss_cleared:
            self.boss_timer -= 1
            
            # ボスの出現チェック
            if self.boss_timer <= 0:
                # 次のボス番号を設定し、ボスを生成
                self.current_boss_number += 1
                if self.current_boss_number <= 10:
                    # ボス出現時に敵を一掃（ボス戦の準備）
                    # 敵全滅の爆発エフェクトを追加
                    for enemy in self.enemies:
                        from explosion import Explosion
                        self.explosions.append(Explosion(enemy.x + enemy.width//2, enemy.y + enemy.height//2))
                    
                    # 敵リストをクリア
                    self.enemies = []
                    
                    # ボスの生成
                    self.boss = create_boss(
                        self.current_boss_number,
                        SCREEN_WIDTH // 2 - 25,  # 画面中央
                        -50  # 画面上部（徐々に下に移動）
                    )
                    
                    # ボスをアクティブにする（明示的に設定）
                    self.boss.active = True
                    
                    # ボス出現メッセージ
                    print(f"DEBUG: Boss {self.current_boss_number} appears!")
                    
                    # 効果音
                    try:
                        pyxel.play(0, 4)  # ボス登場音
                    except:
                        pass
        
        # Spawn enemies
        self.update_enemy_spawning()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Remove enemies that are off-screen
            if enemy.y > SCREEN_HEIGHT + 10:
                self.enemies.remove(enemy)
        
        # Update bullets
        self.update_bullets()
        
        # パワーアップアイテムの更新
        for powerup in self.powerups[:]:
            powerup.update()
            
            # 画面外に出たアイテムを削除
            if powerup.y > SCREEN_HEIGHT + 10:
                self.powerups.remove(powerup)
        
        # Check collisions
        self.check_collisions()
        
        # Update explosions
        self.update_explosions()
        
        # Check game over
        if self.player.lives <= 0:
            self.state = STATE_GAME_OVER
    
    def update_game_over(self):
        # Restart game when SPACE is pressed
        if pyxel.btnp(KEY_SPACE):
            self.reset_game()
            self.state = STATE_PLAYING
    
    def update_enemy_spawning(self):
        # ボスが存在する場合は敵の生成を停止（ボス戦中）
        if self.boss and self.boss.active:
            return
            
        # Spawn enemies based on timer
        self.enemy_timer += 1
        if self.enemy_timer >= ENEMY_SPAWN_INTERVAL:
            self.enemy_timer = 0
            
            # Determine enemy type (random for now)
            enemy_type = random.randint(0, 2)
            x = random.randint(10, SCREEN_WIDTH - 10)
            
            if enemy_type == 0:
                self.enemies.append(SmallEnemy(x, -10))
            elif enemy_type == 1:
                self.enemies.append(MediumEnemy(x, -15))
            else:
                self.enemies.append(LargeEnemy(x, -20))
    
    def update_bullets(self):
        # デバッグ: 弾のカウントを表示
        print(f"DEBUG: Player bullets count: {len(self.player_bullets)}")
        
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.y < -10:
                self.player_bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT + 10:
                self.enemy_bullets.remove(bullet)
    
    def check_collisions(self):
        # プレイヤー弾とボスの衝突判定（ボスの内部で処理）
        if self.boss and self.boss.active:
            self.boss.update(self.player_bullets, self.enemy_bullets, self.player)
            
            # プレイヤーとボスの衝突判定
            if not self.player.invulnerable:
                # ボスの全体サイズで判定
                if (self.player.x < self.boss.x + self.boss.width and
                    self.player.x + self.player.width > self.boss.x and
                    self.player.y < self.boss.y + self.boss.height and
                    self.player.y + self.player.height > self.boss.y):
                    
                    # プレイヤーにダメージ
                    self.player.hit()
                    
                    # 爆発エフェクト
                    from explosion import Explosion
                    self.explosions.append(Explosion(self.player.x + self.player.width//2, 
                                                    self.player.y + self.player.height//2))
                    
                    # 効果音
                    try:
                        pyxel.play(1, 1)  # 爆発音
                    except:
                        pass
        
        # Check player bullets vs enemies
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + 2 > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + 5 > enemy.y):
                    
                    # Hit enemy
                    enemy.hit()
                    
                    # Remove bullet
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    
                    # Check if enemy is destroyed
                    if enemy.health <= 0:
                        # Add explosion
                        from explosion import Explosion
                        self.explosions.append(Explosion(enemy.x + enemy.width//2, enemy.y + enemy.height//2))
                        
                        # Add score
                        if isinstance(enemy, SmallEnemy):
                            self.score += ENEMY_SMALL_SCORE
                        elif isinstance(enemy, MediumEnemy):
                            self.score += ENEMY_MEDIUM_SCORE
                        elif isinstance(enemy, LargeEnemy):
                            self.score += ENEMY_LARGE_SCORE
                        
                        # ランダムでパワーアップアイテムをドロップ
                        if random.random() < POWERUP_DROP_CHANCE:
                            # ランダムなパワーアップアイテムを生成
                            powerup = create_random_powerup(
                                enemy.x + enemy.width // 2, 
                                enemy.y + enemy.height // 2
                            )
                            self.powerups.append(powerup)
                            print(f"DEBUG: Powerup created of type {powerup.powerup_type}")
                        
                        # Remove enemy
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        
                        # Play explosion sound
                        pyxel.play(1, 1)  # explosion sound
                    
                    break
        
        # パワーアップアイテムとプレイヤーの衝突判定
        for powerup in self.powerups[:]:
            if (powerup.x < self.player.x + self.player.width and
                powerup.x + powerup.width > self.player.x and
                powerup.y < self.player.y + self.player.height and
                powerup.y + powerup.height > self.player.y):
                
                # パワーアップ効果を適用
                self.player.apply_powerup(powerup.powerup_type)
                
                # パワーアップアイテム削除
                self.powerups.remove(powerup)
                
                # パワーアップ取得音再生
                try:
                    pyxel.play(1, 2)  # アイテム取得音
                except:
                    pass
        
        # Check enemy bullets vs player
        if not self.player.invulnerable:
            for bullet in self.enemy_bullets[:]:
                if (bullet.x < self.player.x + self.player.width and
                    bullet.x + 2 > self.player.x and
                    bullet.y < self.player.y + self.player.height and
                    bullet.y + 5 > self.player.y):
                    
                    # Hit player
                    self.player.hit()
                    
                    # Remove bullet
                    self.enemy_bullets.remove(bullet)
                    
                    # Add explosion
                    from explosion import Explosion
                    self.explosions.append(Explosion(self.player.x + self.player.width//2, 
                                                     self.player.y + self.player.height//2))
                    
                    # Play explosion sound
                    pyxel.play(1, 1)  # explosion sound
                    break
        
        # Check player vs enemies
        if not self.player.invulnerable:
            for enemy in self.enemies[:]:
                if (self.player.x < enemy.x + enemy.width and
                    self.player.x + self.player.width > enemy.x and
                    self.player.y < enemy.y + enemy.height and
                    self.player.y + self.player.height > enemy.y):
                    
                    # Hit player
                    self.player.hit()
                    
                    # Add explosion
                    from explosion import Explosion
                    self.explosions.append(Explosion(enemy.x + enemy.width//2, enemy.y + enemy.height//2))
                    
                    # Remove enemy
                    self.enemies.remove(enemy)
                    
                    # Play explosion sound
                    pyxel.play(1, 1)  # explosion sound
                    break
    
    def update_explosions(self):
        # Update all explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
    
    def draw(self):
        # Clear screen
        pyxel.cls(0)
        
        # Draw based on game state
        if self.state == STATE_TITLE:
            self.draw_title_screen()
        elif self.state == STATE_PLAYING:
            self.draw_game()
        elif self.state == STATE_GAME_OVER:
            self.draw_game()
            self.draw_game_over()
    
    def draw_title_screen(self):
        # Draw background
        self.background.draw()
        
        # Draw title
        pyxel.text(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//3, "DODANPYXEL", pyxel.COLOR_YELLOW)
        
        # Blink "PRESS SPACE or TAP SCREEN" text
        if self.frame_count % 30 < 15:
            pyxel.text(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2, "PRESS SPACE or TAP SCREEN", pyxel.COLOR_WHITE)
        
        # Draw instructions
        pyxel.text(10, SCREEN_HEIGHT - 40, "ARROWS/WASD: MOVE", pyxel.COLOR_WHITE)
        pyxel.text(10, SCREEN_HEIGHT - 30, "AUTO-SHOOTING ENABLED!", ORANGE)
        
        # Mobile instructions
        pyxel.text(10, SCREEN_HEIGHT - 20, "TOUCH & DRAG: MOVE", pyxel.COLOR_YELLOW)
        pyxel.text(10, SCREEN_HEIGHT - 10, "AUTO-SHOOTING ACTIVE", pyxel.COLOR_YELLOW)
        
        # Draw auto-shoot button preview
        pyxel.circ(SCREEN_WIDTH - 15, SCREEN_HEIGHT - 15, 10, ORANGE)
        pyxel.text(SCREEN_WIDTH - 27, SCREEN_HEIGHT - 17, "AUTO", pyxel.COLOR_WHITE)
    
    def draw_game(self):
        # Draw background
        self.background.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()
            
        # ボスの描画（アクティブなボスがいる場合）
        if self.boss and self.boss.active:
            self.boss.draw()
        
        # Draw bullets
        print(f"DEBUG: Number of player bullets to draw: {len(self.player_bullets)}")
        for bullet in self.player_bullets:
            print(f"DEBUG: Drawing bullet at ({bullet.x}, {bullet.y})")
            bullet.draw()
        
        for bullet in self.enemy_bullets:
            bullet.draw()
            
        # パワーアップアイテムの描画
        for powerup in self.powerups:
            powerup.draw()
        
        # Draw explosions
        for explosion in self.explosions:
            explosion.draw()
        
        # Draw UI
        self.draw_ui()
        
        # サイクル完了メッセージを表示
        if self.show_cycle_message:
            # 半透明の背景
            for y in range(SCREEN_HEIGHT//3 - 20, SCREEN_HEIGHT//3 + 30, 2):
                for x in range(0, SCREEN_WIDTH, 2):
                    pyxel.pset(x, y, 0)
            
            # 点滅効果（5フレームごとに色を変える）
            text_color = YELLOW if (self.frame_count // 5) % 2 == 0 else RED
            
            # メッセージ表示 (中央揃え)
            message = self.cycle_message
            msg_width = len(message) * 4  # 4ピクセル/文字
            x = SCREEN_WIDTH//2 - msg_width//2
            y = SCREEN_HEIGHT//3
            pyxel.text(x, y, message, text_color)
    
    def draw_ui(self):
        # Draw score
        pyxel.text(5, 5, f"SCORE: {self.score}", pyxel.COLOR_WHITE)
        
        # Draw lives
        for i in range(self.player.lives):
            pyxel.rect(SCREEN_WIDTH - 10 - i * 8, 5, 6, 6, pyxel.COLOR_RED)
            
        # ボスステータスと距離の表示
        if self.state == STATE_PLAYING:
            # サイクル情報の表示
            if self.boss_cycle_enabled and self.boss_clear_count > 0:
                cycle_text = f"CYCLE: {self.boss_clear_count}/{self.max_boss_in_cycle}"
                pyxel.text(5, 25, cycle_text, ORANGE)
                
            # 現在のボス番号表示
            if self.boss:
                boss_name = getattr(self.boss, 'name', f"BOSS {self.current_boss_number}")
                pyxel.text(5, 15, f"BOSS: {self.current_boss_number}/10 - {boss_name}", RED)
            
            # ボスまでの距離インジケーター（ボスがいない場合のみ）
            elif not self.all_boss_cleared:
                # インジケーターの基本パラメータ
                bar_width = 50
                bar_height = 5
                x = SCREEN_WIDTH - bar_width - 5
                y = 20
                
                # 背景バー（黒枠）
                pyxel.rectb(x - 1, y - 1, bar_width + 2, bar_height + 2, BLACK)
                
                # 進行度を計算（0〜1の範囲）- ボスタイマーをベースに
                progress = 1.0 - (self.boss_timer / BOSS_DISTANCE_INTERVAL)
                progress = max(0.0, min(1.0, progress))  # 0〜1の範囲に制限
                
                # プログレスバーの色（赤→黄→緑でグラデーション）
                try:
                    if progress < 0.5:
                        # 赤→黄 (0.0〜0.5の範囲)
                        bar_color = RED
                    elif progress < 0.8:
                        # 黄 (0.5〜0.8の範囲)
                        bar_color = YELLOW
                    else:
                        # 緑 (0.8〜1.0の範囲)
                        bar_color = GREEN
                except Exception as e:
                    # エラーが発生した場合はデフォルト色に
                    print(f"DEBUG: Error setting bar color: {e}")
                    bar_color = WHITE
                    
                # 進行バー
                fill_width = int(bar_width * progress)
                pyxel.rect(x, y, fill_width, bar_height, bar_color)
                
                # 「BOSS」ラベル
                pyxel.text(x - 20, y, "BOSS:", WHITE)
                
                # 距離テキスト（％で表示）
                percent = int(progress * 100)
                pyxel.text(x + bar_width + 5, y, f"{percent}%", WHITE)
                
                # 次のボス番号表示
                next_boss = self.current_boss_number + 1
                if 1 <= next_boss <= 10:
                    pyxel.text(x - 20, y + 10, f"NEXT: BOSS {next_boss}", YELLOW)
            
        # Draw virtual touch controls if enabled
        if self.show_touch_controls:
            # Draw auto-shoot indicator in bottom right
            pyxel.circ(SCREEN_WIDTH - 15, SCREEN_HEIGHT - 15, 10, ORANGE)
            pyxel.text(SCREEN_WIDTH - 27, SCREEN_HEIGHT - 17, "AUTO", pyxel.COLOR_WHITE)
            
            # Draw touch movement indicator if active
            if self.touch_enabled and not (
                pyxel.mouse_x > SCREEN_WIDTH - 30 and pyxel.mouse_y > SCREEN_HEIGHT - 30
            ):
                # Draw touch start point
                pyxel.circ(self.touch_start_x, self.touch_start_y, 3, pyxel.COLOR_YELLOW)
                
                # Draw line from start to current position
                pyxel.line(
                    self.touch_start_x, 
                    self.touch_start_y, 
                    self.touch_current_x, 
                    self.touch_current_y, 
                    pyxel.COLOR_YELLOW
                )
    
    def draw_game_over(self):
        # Draw semi-transparent overlay
        for y in range(0, SCREEN_HEIGHT, 2):
            for x in range(0, SCREEN_WIDTH, 2):
                pyxel.pset(x, y, 0)
        
        # Draw "GAME OVER" text
        pyxel.text(SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2 - 10, "GAME OVER", pyxel.COLOR_RED)
        
        # Draw score
        pyxel.text(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//2 + 10, f"SCORE: {self.score}", pyxel.COLOR_YELLOW)
        
        # Blink "PRESS SPACE or TAP SCREEN" text
        if self.frame_count % 30 < 15:
            pyxel.text(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 30, "PRESS SPACE or TAP SCREEN", pyxel.COLOR_WHITE)
