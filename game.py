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
from highscores import HighScores, SoftwareKeyboard

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
                
        # マウス入力を無効化（キーボードのみ）
        try:
            pyxel.mouse(False)  # マウス入力を無効化
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
        
        # Intro text related
        self.show_intro = False
        self.intro_timer = 0
        self.intro_texts = [
            "In a distant future where humanity has perished,",
            "you are the last survivor, encountering a civilization",
            "from the far reaches of the universe.",
            "",
            "Armed with their technology, you must find the key",
            "to humanity's revival while facing unknown enemies.",
            "",
            "Your choices will determine the future.",
            "Is there hope at the end of this battle?",
            "",
            "The final fight begins now...",
            "",
            "LAST DESCENT: THE FINAL HOPE"
        ]
        
        # キーボード操作専用モードに設定
        
        # Initialize high scores
        self.high_scores = HighScores()
        self.keyboard = SoftwareKeyboard(SCREEN_WIDTH // 2 - 35, SCREEN_HEIGHT // 2 + 20)
        self.new_high_score = False
        
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
        
        # BGM関連の変数
        self.current_bgm = 0  # 0=通常BGM、1=ボス戦BGM
        self.bgm_playing = False
        
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
        
        # メッセージ表示用の変数
        self.show_cycle_message = False
        self.cycle_message_timer = 0
        self.cycle_message = ""
        
        # ボスクリアメッセージ表示用の変数
        self.show_boss_clear_message = False
        self.boss_clear_message_timer = 0
        self.boss_clear_message = ""
        self.boss_clear_bonus = 0
        
        # 遅延エフェクト用の配列
        self.delayed_effects = []
        
        # ボス警告システム用の変数
        self.boss_warning_triggered = False
        self.boss_warning_flash = False
        self.boss_warning_count = 0
        self.warning_sound_played = False
        
        # 自動発射機能を設定（キーボード専用）
        self.auto_shoot = True
    
    def update(self):
        # Update based on game state
        if self.state == STATE_TITLE:
            self.update_title_screen()
        elif self.state == STATE_PLAYING:
            self.update_game()
        elif self.state == STATE_GAME_OVER:
            self.update_game_over()
            
        # Increment frame counter
        self.frame_count += 1
        
    # タッチ入力関連のメソッドを削除（キーボード操作のみに対応）
    
    def update_title_screen(self):
        # Intro display timer management
        self.intro_timer += 1
        
        # Show intro after 5 seconds on title screen
        if self.intro_timer > 300 and not self.show_intro:
            self.show_intro = True
        
        # SPACE key to skip intro or start game
        if pyxel.btnp(KEY_SPACE):
            if self.show_intro:
                # If showing intro, skip and return to title screen
                self.show_intro = False
                self.intro_timer = 0
                try:
                    pyxel.play(0, 3)  # Sound effect
                except:
                    pass
            else:
                # On normal title screen, start the game
                self.state = STATE_PLAYING
                try:
                    pyxel.play(0, 2)  # Play start sound
                except:
                    pass
                
                # Reset BGM flag when transitioning from title screen
                self.bgm_playing = False
    
    def update_game(self):
        # 自動発射フラグを更新（キーボード用）
        self.auto_shoot = True
        
        # BGMの再生と管理（毎フレーム確認）
        # ボス戦とノーマル戦で異なるBGM
        if self.boss and self.boss.active and not self.boss.exit_phase:
            # ボス戦BGM（インデックス1）に切り替え
            if self.current_bgm != 1:
                self.current_bgm = 1
                self.bgm_playing = False
                print("DEBUG: Switching to BOSS BGM")
        else:
            # 通常BGM（インデックス0）に切り替え
            if self.current_bgm != 0:
                self.current_bgm = 0
                self.bgm_playing = False
                print("DEBUG: Switching to NORMAL BGM")
        
        # BGMの再生（停止していたら再開）
        if not self.bgm_playing:
            try:
                pyxel.playm(self.current_bgm, loop=True)
                print(f"DEBUG: Started playing BGM {self.current_bgm}")
                self.bgm_playing = True
            except Exception as e:
                print(f"ERROR playing BGM {self.current_bgm}: {e}")
                # エラー発生時は次のフレームで再試行
                self.bgm_playing = False
        
        # Update background
        self.background.update()
        
        # Update player
        self.player.update()
        
        # サイクル完了メッセージのタイマー更新
        if self.show_cycle_message:
            self.cycle_message_timer -= 1
            if self.cycle_message_timer <= 0:
                self.show_cycle_message = False
                
        # ボスクリアメッセージのタイマー更新
        if self.show_boss_clear_message:
            self.boss_clear_message_timer -= 1
            if self.boss_clear_message_timer <= 0:
                self.show_boss_clear_message = False
        
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
                # 退場フェーズに入ったらBGM切り替えのフラグを設定（通常BGMに戻す準備）
                if not self.boss.exit_bgm_changed and self.boss.exit_phase:
                    print("DEBUG: Boss defeat detected - preparing to switch back to normal BGM")
                    self.boss.exit_bgm_changed = True
                    self.current_bgm = 0  # 通常BGMに切り替え準備
                    self.bgm_playing = False  # BGM再生をリセット
                
                self.boss.y -= 2  # 上に退場
                if self.boss.y + self.boss.height < 0:  # 画面外に出たら
                    self.boss.active = False  # 非アクティブに
                    
                    # ボスが倒されて退場完了した場合
                    self.score += 1000 * self.boss.boss_number  # ボーナススコア
                    self.boss_clear_count += 1
                    
                    # 大規模な爆発エフェクト (ボス撃破演出)
                    from explosion import Explosion
                    
                    # 複数の大きな爆発を時間差で発生（連鎖爆発の演出）
                    def create_delayed_explosion(x, y, scale=1.0, delay=0):
                        # 指定フレーム後に爆発を生成する関数
                        if delay <= 0:
                            explosion = Explosion(x, y)
                            explosion.scale = scale  # スケールの設定
                            self.explosions.append(explosion)
                        else:
                            # 遅延タイマーを設定
                            self.delayed_effects.append({
                                'type': 'explosion',
                                'timer': delay,
                                'x': x,
                                'y': y,
                                'scale': scale
                            })
                    
                    # 中央で大爆発
                    center_x = self.boss.x + self.boss.width//2
                    center_y = self.boss.y + self.boss.height//2
                    create_delayed_explosion(center_x, center_y, 2.0, 0)  # 即時の大爆発
                    
                    # 周囲に小〜中爆発をランダムな時間差で配置
                    for i in range(15):
                        offset_x = random.randint(-20, 20)
                        offset_y = random.randint(-20, 20)
                        delay = random.randint(5, 25)  # 数フレーム遅延
                        scale = random.uniform(0.7, 1.5)
                        ex = center_x + offset_x
                        ey = center_y + offset_y
                        create_delayed_explosion(ex, ey, scale, delay)
                    
                    # ボスの輪郭に沿った爆発 (より広範囲に)
                    for i in range(10):
                        ex = self.boss.x + random.randint(-10, self.boss.width + 10)
                        ey = self.boss.y + random.randint(-10, self.boss.height + 10)
                        delay = random.randint(10, 30)
                        scale = random.uniform(0.8, 1.2)
                        create_delayed_explosion(ex, ey, scale, delay)
                    
                    # 「BOSS CLEARED!」メッセージを表示
                    self.show_boss_clear_message = True
                    self.boss_clear_message_timer = 120  # 2秒間表示
                    self.boss_clear_message = f"BOSS {self.current_boss_number} CLEARED!"
                    self.boss_clear_bonus = 1000 * self.boss.boss_number  # ボーナス点数
                    
                    # ボス撃破報酬として追加ライフ
                    self.player.lives += BOSS_EXTRA_LIFE
                    
                    # 効果音 (複数のチャンネルを使って重ねて鳴らす)
                    try:
                        pyxel.play(2, 3)  # ボス撃破音
                        pyxel.play(1, 1)  # 爆発音1
                        pyxel.play(0, 1)  # 爆発音2
                        # 0.5秒後にもう一度爆発音
                        self.delayed_effects.append({
                            'type': 'sound',
                            'timer': 30,
                            'channel': 0,
                            'sound': 1
                        })
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
            
            # ボス出現警告の処理（ボスタイマーが一定値以下になったら警告を表示）
            if self.boss_timer <= 180 and self.boss_timer > 0:  # 約3秒前から警告開始
                # 警告フラグがまだ設定されていなければ設定
                if not self.boss_warning_triggered:
                    self.boss_warning_triggered = True
                    self.boss_warning_count = 0
                    print("DEBUG: Boss warning activated!")
                
                # 警告音を定期的に再生（30フレームごと）
                if self.boss_warning_count % 30 == 0 and not self.warning_sound_played:
                    try:
                        pyxel.play(0, 20)  # 警告音を再生
                        self.warning_sound_played = True
                    except Exception as e:
                        print(f"ERROR playing warning sound: {e}")
                
                # 1秒ごとに点滅の切り替え（視覚的な警告効果）
                if self.boss_warning_count % 60 == 0:
                    self.boss_warning_flash = not self.boss_warning_flash
                    self.warning_sound_played = False  # 次の警告音のために再設定
                
                # 警告カウンターを増やす
                self.boss_warning_count += 1
            
            # 警告状態のリセット（ボスタイマーがゼロになったらリセット）
            if self.boss_timer <= 0:
                self.boss_warning_triggered = False
                self.boss_warning_flash = False
                self.boss_warning_count = 0
                
                # ボスの出現チェック
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
                        pyxel.play(0, 21)  # 新しいボス登場音
                    except Exception as e:
                        print(f"ERROR playing boss appearance sound: {e}")
        
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
        # ハイスコア判定と入力処理
        if not self.new_high_score:
            # スコアがハイスコアなら名前入力モードに
            if self.high_scores.is_high_score(self.score):
                self.new_high_score = True
                self.keyboard.activate()
                # デバッグ表示
                print("DEBUG: High score detected, activating keyboard")
        else:
            # ゲーム全体でのタッチイベントを先にチェックし、
            # キーボード表示中はキーボード外のタッチを無視する
            if pyxel.btnp(MOUSE_BUTTON_LEFT):
                # タッチ座標を取得
                mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
                
                # キーボードの表示領域を計算
                keyboard_area_x = self.keyboard.x - 8
                keyboard_area_y = self.keyboard.y - 28
                keyboard_area_width = 85  # キーボード幅 + 余白
                keyboard_area_height = 120  # キーボード高さ + 確定ボタン + 余白
                
                # キーボード領域外のタッチはこの時点で無視（ゲーム再開防止）
                keyboard_area = (
                    keyboard_area_x <= mouse_x <= keyboard_area_x + keyboard_area_width and
                    keyboard_area_y <= mouse_y <= keyboard_area_y + keyboard_area_height
                )
                
                # キーボード領域外のタッチは処理しない（デバッグ出力）
                if not keyboard_area:
                    print("DEBUG: Touch outside keyboard area ignored")
                    return
            
            # キーボード操作を更新
            self.keyboard.update()
            
            # 名前入力が完了したらハイスコアに登録
            if self.keyboard.complete:
                player_name = self.keyboard.get_text()
                if not player_name:  # 空の場合はデフォルト名
                    player_name = "PLAYER"
                
                # デバッグ表示
                print(f"DEBUG: Name input complete: '{player_name}'")
                
                # ハイスコアに追加して保存
                self.high_scores.add_score(player_name, self.score)
                
                # キーボードを無効化し、ハイスコア登録完了
                self.keyboard.deactivate()
                self.new_high_score = False
                
                # 効果音再生
                try:
                    pyxel.play(0, 3)  # ハイスコア登録音
                except:
                    pass
                    
                # ハイスコア確定後にタイトル画面に戻る
                self.reset_game()
                self.state = STATE_TITLE
                print("DEBUG: High score submitted, returning to title screen")
                return  # 処理終了
        
        # 名前入力中は以下の処理をスキップ
        if self.keyboard.active:
            return
            
        # Restart game when SPACE is pressed
        if pyxel.btnp(KEY_SPACE):
            self.reset_game()
            self.state = STATE_TITLE  # タイトル画面に戻る
    
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
                
        # 遅延エフェクトの更新
        for effect in self.delayed_effects[:]:
            effect['timer'] -= 1
            if effect['timer'] <= 0:
                if effect['type'] == 'explosion':
                    # 爆発エフェクトの作成
                    from explosion import Explosion
                    explosion = Explosion(effect['x'], effect['y'])
                    explosion.scale = effect['scale']
                    self.explosions.append(explosion)
                    
                elif effect['type'] == 'sound':
                    # 効果音の再生
                    try:
                        pyxel.play(effect['channel'], effect['sound'])
                    except:
                        pass
                    
                # 処理済みのエフェクトをリストから削除
                self.delayed_effects.remove(effect)
    
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
        
        # スターウォーズ風のイントロテキストを表示
        if self.show_intro:
            self.draw_intro_text()
            return  # イントロ表示中は他の要素を描画しない
        
        # Draw title
        pyxel.text(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//6, "LAST DESCENT", pyxel.COLOR_YELLOW)
        pyxel.text(SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT//6 + 10, "THE FINAL HOPE", pyxel.COLOR_YELLOW)
        
        # Blink "PRESS SPACE" text
        if self.frame_count % 30 < 15:
            pyxel.text(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//2 + 30, "PRESS SPACE TO START", pyxel.COLOR_WHITE)
        
        # Draw high scores in the middle of the title screen
        self.draw_title_high_scores()
        
        # ビルド番号を右上（タイトルの下）に表示
        version_text = VERSION_DISPLAY
        pyxel.text(SCREEN_WIDTH - len(version_text) * 4 - 5, SCREEN_HEIGHT//6 + 25, version_text, pyxel.COLOR_GRAY)
        
        # Draw keyboard instructions（左下）
        pyxel.text(10, SCREEN_HEIGHT - 30, "ARROWS/WASD: MOVE", pyxel.COLOR_WHITE)
        pyxel.text(10, SCREEN_HEIGHT - 20, "Z: SHOOT", pyxel.COLOR_WHITE)
        
        # 自動発射の通知（左下）
        pyxel.text(10, SCREEN_HEIGHT - 10, "AUTO-SHOOTING ENABLED", ORANGE)
        
    def draw_intro_text(self):
        """Star Wars style intro text animation"""
        # Scroll speed and display time adjustment
        scroll_speed = 0.5
        display_time = 500  # Display time (frames)
        
        # Return to title screen when intro animation is complete
        if self.intro_timer > len(self.intro_texts) * 60 + display_time:
            self.show_intro = False
            self.intro_timer = 0
            return
            
        # Starry background
        pyxel.cls(0)  # Black background
        
        # Draw random stars
        for i in range(100):
            x = (i * 13) % SCREEN_WIDTH
            y = (i * 17) % SCREEN_HEIGHT
            col = 7 if i % 5 == 0 else 6  # Some white, others light blue
            pyxel.pset(x, y, col)
        
        # Calculate text Y position (scrolling effect)
        base_y = SCREEN_HEIGHT + 50 - self.intro_timer * scroll_speed
        
        # Draw each line of text
        for i, text in enumerate(self.intro_texts):
            y = base_y + i * 15  # Line spacing
            
            # Only draw text visible on screen
            if 0 <= y < SCREEN_HEIGHT:
                # Center text
                x = SCREEN_WIDTH//2 - len(text) * 2
                # Color with perspective (darker as it gets farther)
                color = max(5, min(7, 7 - int((SCREEN_HEIGHT - y) / 30)))
                pyxel.text(x, y, text, color)
                
        # Skip with SPACE key (blinking text)
        if self.frame_count % 30 < 15:
            pyxel.text(SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT - 10, "PRESS SPACE TO SKIP", 8)
        
    def draw_title_high_scores(self):
        """タイトル画面にハイスコア表示"""
        # タイトル
        title_text = "- HIGH SCORES -"
        title_width = len(title_text) * 4  # 文字幅の計算
        title_x = SCREEN_WIDTH // 2 - title_width // 2  # 中央揃え
        title_y = SCREEN_HEIGHT // 3
        
        # 半透明の背景パネル（ハイスコア表示用）
        panel_padding = 8
        panel_x = SCREEN_WIDTH // 2 - 70  # 幅を固定してセンターに配置
        panel_y = title_y - panel_padding
        panel_width = 140  # パネル幅を固定
        panel_height = 68  # タイトル + 上位5位分 + 余白
        
        # 背景パネルを描画（半透明効果）
        for y in range(panel_y, panel_y + panel_height, 2):
            for x in range(panel_x, panel_x + panel_width, 2):
                pyxel.pset(x, y, 0)  # 黒色のドット
        
        # パネルの枠線
        pyxel.rectb(panel_x, panel_y, panel_width, panel_height, 5)  # 紫色の枠線
        
        # タイトルを描画
        pyxel.text(title_x, title_y, title_text, pyxel.COLOR_YELLOW)
        
        # 上位5スコアのみを表示（タイトル画面用に簡略化）
        scores = self.high_scores.scores[:5]  # 上位5件を取得
        
        # スコアがない場合
        if not scores:
            no_score_text = "NO SCORES YET"
            no_score_x = SCREEN_WIDTH // 2 - len(no_score_text) * 2
            pyxel.text(no_score_x, title_y + 15, no_score_text, pyxel.COLOR_WHITE)
            return
        
        # スコア表示の開始位置
        start_x = panel_x + 10  # 左余白
        score_y = title_y + 10  # タイトルの下
        
        # スコア情報のカラム幅を設定
        rank_width = 15   # ランク表示用
        name_width = 70   # 名前表示用
        score_width = 45  # スコア表示用
        
        # 上位5スコアを表示
        for i, score_data in enumerate(scores):
            # 色分け (1位: 金, 2位: 銀, 3位: 銅, その他: 白)
            if i == 0:  # 1位
                color = 10  # 緑/金
                prefix = "1."
            elif i == 1:  # 2位
                color = 7   # 白/銀
                prefix = "2."
            elif i == 2:  # 3位
                color = 9   # オレンジ/銅
                prefix = "3."
            else:
                color = pyxel.COLOR_WHITE
                prefix = f"{i+1}."
            
            name = score_data["name"]
            score = score_data["score"]
            
            # 位置を計算
            rank_x = start_x
            name_x = start_x + rank_width
            
            # スコアは右寄せ
            score_text = f"{score}"
            score_x_pos = panel_x + panel_width - 15 - len(score_text) * 4
            
            # 各行を表示
            pyxel.text(rank_x, score_y + i * 10, prefix, color)
            pyxel.text(name_x, score_y + i * 10, name, color)
            pyxel.text(score_x_pos, score_y + i * 10, score_text, color)
    
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
            
        # ボス出現警告の表示（警告フラグが立っている場合のみ）
        if self.boss_warning_triggered and self.boss_warning_flash:
            # 画面全体に薄い赤色のオーバーレイを表示（警告効果）
            for y in range(0, SCREEN_HEIGHT, 4):
                for x in range(0, SCREEN_WIDTH, 4):
                    pyxel.pset(x, y, RED)
            
            # "WARNING"メッセージを表示（中央上部、点滅）
            warning_text = "! WARNING !"
            text_width = len(warning_text) * 4  # 4ピクセル/文字
            text_x = SCREEN_WIDTH//2 - text_width//2
            text_y = SCREEN_HEIGHT//4
            
            # 点滅するテキスト色
            text_color = WHITE if (self.frame_count // 3) % 2 == 0 else YELLOW
            pyxel.text(text_x, text_y, warning_text, text_color)
            
            # ボス接近メッセージ
            boss_text = "BOSS APPROACHING"
            boss_width = len(boss_text) * 4
            boss_x = SCREEN_WIDTH//2 - boss_width//2
            boss_y = text_y + 10
            pyxel.text(boss_x, boss_y, boss_text, RED)
        
        # Draw bullets
        for bullet in self.player_bullets:
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
            
        # ボスクリアメッセージを表示（ボス撃破時）
        if self.show_boss_clear_message:
            # 半透明の背景（画面中央に横帯）
            for y in range(SCREEN_HEIGHT//2 - 15, SCREEN_HEIGHT//2 + 25, 2):
                for x in range(0, SCREEN_WIDTH, 1):  # 横帯を濃くする
                    pyxel.pset(x, y, 0)
            
            # 点滅効果
            text_color = WHITE if (self.frame_count // 3) % 2 == 0 else YELLOW
            bonus_color = GREEN if (self.frame_count // 4) % 2 == 0 else YELLOW
            
            # メッセージ表示 (中央揃え)
            message = self.boss_clear_message
            msg_width = len(message) * 4
            x = SCREEN_WIDTH//2 - msg_width//2
            y = SCREEN_HEIGHT//2 - 5
            
            # ボスクリアメッセージ
            pyxel.text(x, y, message, text_color)
            
            # ボーナススコアメッセージ
            bonus_msg = f"BONUS: {self.boss_clear_bonus}"
            bonus_width = len(bonus_msg) * 4
            pyxel.text(SCREEN_WIDTH//2 - bonus_width//2, y + 10, bonus_msg, bonus_color)
            
            # 追加ライフメッセージ
            if BOSS_EXTRA_LIFE > 0:
                life_msg = f"+{BOSS_EXTRA_LIFE} LIFE!"
                life_width = len(life_msg) * 4
                pyxel.text(SCREEN_WIDTH//2 - life_width//2, y + 20, life_msg, RED)
    
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
            
        # タッチコントロール表示を削除（キーボード操作のみ対応）
    
    def draw_game_over(self):
        # 暗めの半透明オーバーレイ（市松模様）
        for y in range(0, SCREEN_HEIGHT, 2):
            for x in range(0, SCREEN_WIDTH, 2):
                pyxel.pset(x, y, 0)
        
        # "GAME OVER" テキストの背景とボーダー
        game_over_y = 30
        # 背景（黒い長方形）
        pyxel.rect(SCREEN_WIDTH//2 - 35, game_over_y - 5, 70, 15, 0)
        # 赤いボーダー
        pyxel.rectb(SCREEN_WIDTH//2 - 36, game_over_y - 6, 72, 17, 8)
        pyxel.rectb(SCREEN_WIDTH//2 - 35, game_over_y - 5, 70, 15, 8)
        
        # "GAME OVER" テキスト（点滅効果）
        text_color = 8 if (self.frame_count // 8) % 2 == 0 else 7
        pyxel.text(SCREEN_WIDTH//2 - 20, game_over_y, "GAME OVER", text_color)
        
        # スコア表示の背景
        score_y = 50
        pyxel.rect(SCREEN_WIDTH//2 - 35, score_y - 2, 70, 10, 1)
        
        # スコア表示（大きめのフォントで）
        score_text = f"SCORE: {self.score}"
        pyxel.text(SCREEN_WIDTH//2 - len(score_text)*2, score_y, score_text, pyxel.COLOR_YELLOW)
        
        # ソフトウェアキーボードが有効な場合は表示
        if self.keyboard.active:
            # キーボード入力中のメッセージ
            message = "NEW HIGH SCORE!"
            msg_width = len(message) * 4
            msg_x = SCREEN_WIDTH//2 - msg_width//2
            
            # 点滅効果付きメッセージ
            if (self.frame_count // 10) % 2 == 0:
                pyxel.text(msg_x, 65, message, 10)  # 緑色
            else:
                pyxel.text(msg_x, 65, message, 9)   # オレンジ色
            
            # キーボード表示
            self.keyboard.draw()
            return
            
        # ハイスコア表示（名前入力完了後または入力不要の場合）
        if not self.new_high_score:
            # ハイスコアセクションの背景
            pyxel.rect(20, 68, SCREEN_WIDTH - 40, 86, 5)
            pyxel.rectb(19, 67, SCREEN_WIDTH - 38, 88, 7)
            
            # ハイスコアヘッダー
            pyxel.text(SCREEN_WIDTH//2 - 30, 70, "HIGH SCORES", 7)
            
            # ハイスコアリストを描画
            self.high_scores.draw_high_scores(30, 80, 7, 10, 9)
            
            # 自分のスコアがハイスコアにある場合はハイライト
            player_in_scores = False
            for score in self.high_scores.scores:
                if score["score"] == self.score:
                    player_in_scores = True
                    break
                    
            if player_in_scores:
                # ハイスコア達成メッセージ（アニメーション効果）
                message = "CONGRATULATIONS! NEW HIGH SCORE!"
                msg_x = (self.frame_count % (SCREEN_WIDTH + len(message)*4)) - len(message)*4
                # 点滅効果
                text_color = 10 if (self.frame_count // 5) % 2 == 0 else 9
                pyxel.text(msg_x, 160, message, text_color)
        
        # リスタートのためのガイダンス
        restart_y = SCREEN_HEIGHT - 25
        # ボタンの背景
        pyxel.rect(SCREEN_WIDTH//2 - 60, restart_y - 2, 120, 15, 5)
        pyxel.rectb(SCREEN_WIDTH//2 - 61, restart_y - 3, 122, 17, 7)
        
        # 点滅するテキスト
        if self.frame_count % 30 < 20:
            pyxel.text(SCREEN_WIDTH//2 - 40, restart_y + 3, "PRESS SPACE TO RESTART", 0)
