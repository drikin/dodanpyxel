import json
import os
import pyxel

class HighScores:
    """ハイスコアを管理するクラス"""
    
    def __init__(self, filename="high_scores.json", max_scores=10):
        self.filename = filename
        self.max_scores = max_scores
        self.scores = []
        self.load_scores()
        
    def reset_scores(self):
        """ハイスコアを全てリセット"""
        self.scores = []
        self.save_scores()
        print("DEBUG: High scores have been reset")
        
    def load_scores(self):
        """ハイスコアをファイルから読み込み"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    self.scores = json.load(file)
            else:
                self.scores = []
        except Exception as e:
            print(f"ハイスコア読み込みエラー: {e}")
            self.scores = []
    
    def save_scores(self):
        """ハイスコアをファイルに保存"""
        try:
            with open(self.filename, "w") as file:
                json.dump(self.scores, file)
        except Exception as e:
            print(f"ハイスコア保存エラー: {e}")
    
    def add_score(self, name, score):
        """新しいスコアを追加し、ランキングを更新"""
        self.scores.append({"name": name, "score": score})
        # スコアの高い順に並べ替え
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # 最大数を超えた場合は削除
        if len(self.scores) > self.max_scores:
            self.scores = self.scores[:self.max_scores]
        self.save_scores()
    
    def is_high_score(self, score):
        """新しいスコアがハイスコアかどうか判定"""
        if len(self.scores) < self.max_scores:
            return True
        return score > self.scores[-1]["score"] if self.scores else True
    
    def draw_high_scores(self, x, y, title_color=7, text_color=7, highlight_color=10):
        """ハイスコアリストを描画"""
        # タイトルは呼び出し側で表示するため、ここでは省略
        
        if not self.scores:
            # 背景付きで「まだスコアがありません」を表示
            pyxel.rect(x - 2, y - 2, 120, 12, 1)
            pyxel.text(x, y, "NO SCORES YET", text_color)
            return
        
        # 表の見出し行
        header_y = y
        pyxel.rect(x - 5, header_y - 2, 120, 10, 1)
        pyxel.text(x, header_y, "RANK NAME        SCORE", text_color)
        
        y += 12  # 見出しの下にスペースを追加
        
        # スコアリストの表示
        for i, score_data in enumerate(self.scores):
            # 行の背景色（交互に色を変える）
            row_bg_color = 1 if i % 2 == 0 else 0
            pyxel.rect(x - 5, y + i * 10 - 2, 120, 10, row_bg_color)
            
            # 特別な色分け
            if i == 0:  # 1位
                color = 10  # 緑
                prefix = "\x82"  # 王冠アイコン
            elif i == 1:  # 2位
                color = 9   # オレンジ
                prefix = "2."
            elif i == 2:  # 3位
                color = 8   # 赤
                prefix = "3."
            else:
                color = text_color
                prefix = f"{i+1}."
            
            name = score_data["name"]
            score = score_data["score"]
            
            # 見やすいように間隔を調整
            rank_x = x
            name_x = x + 18
            score_x = x + 85
            
            # ランク、名前、スコアを個別に表示
            pyxel.text(rank_x, y + i * 10, prefix, color)
            pyxel.text(name_x, y + i * 10, name, color)
            pyxel.text(score_x, y + i * 10, f"{score}", color)


class SoftwareKeyboard:
    """ソフトウェアキーボードクラス"""
    
    def __init__(self, x, y, max_length=8):
        self.x = x
        self.y = y
        self.max_length = max_length
        self.text = ""
        self.active = False
        self.keys = [
            list("ABCDEFG"),
            list("HIJKLMN"),
            list("OPQRSTU"),
            list("VWXYZ_.")
        ]
        self.cursor_row = 0
        self.cursor_col = 0
        self.complete = False
        self.confirm_button_focus = False  # 確定ボタンのフォーカスフラグを追加
        
    def update(self):
        """キーボード入力の更新"""
        if not self.active:
            return
            
        # マウス入力処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            
            # キーがクリックされたかチェック
            for row_idx, row in enumerate(self.keys):
                for col_idx, key in enumerate(row):
                    key_x = self.x + col_idx * 10
                    key_y = self.y + row_idx * 10
                    
                    if (key_x - 1 <= mouse_x <= key_x + 7 and 
                        key_y - 1 <= mouse_y <= key_y + 7):
                        # キーがクリックされた
                        self.cursor_row = row_idx
                        self.cursor_col = col_idx
                        
                        # クリックしたキーを入力
                        if len(self.text) < self.max_length:
                            # キー入力音を再生
                            pyxel.play(0, 11)  # 音声チャンネル0、効果音11を再生
                            
                            if key == '_':
                                self.text += ' '  # スペース
                            elif key == '.':
                                # バックスペース
                                if self.text:
                                    self.text = self.text[:-1]
                            else:
                                self.text += key
                                
            # 確定ボタン領域 (より広く、わかりやすく)
            confirm_button_x = self.x - 2
            confirm_button_y = self.y + len(self.keys) * 10 + 5
            confirm_button_width = 72  # ボタン全体の幅
            confirm_button_height = 16 # ボタンの高さ
            
            if (confirm_button_x <= mouse_x <= confirm_button_x + confirm_button_width and
                confirm_button_y <= mouse_y <= confirm_button_y + confirm_button_height):
                # 決定ボタンがクリックされた
                # 確定音を再生
                pyxel.play(0, 12)  # 音声チャンネル0、効果音12を再生
                self.complete = True
                return
            
        # 確定ボタンにフォーカスしているかどうかのフラグ
        confirm_button_focus = hasattr(self, 'confirm_button_focus') and self.confirm_button_focus
        
        # カーソル移動（キーボード）
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            if confirm_button_focus:
                # 確定ボタンからキーボードの一番下の行に移動
                confirm_button_focus = False
                self.confirm_button_focus = False
                self.cursor_row = len(self.keys) - 1
            else:
                # 通常の上移動
                self.cursor_row = (self.cursor_row - 1) % len(self.keys)
                
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            if self.cursor_row == len(self.keys) - 1:
                # キーボードの一番下の行から確定ボタンにフォーカス
                confirm_button_focus = True
                self.confirm_button_focus = True
            elif not confirm_button_focus:
                # 通常の下移動
                self.cursor_row = (self.cursor_row + 1) % len(self.keys)
                
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            if not confirm_button_focus:
                # キーボード内での左移動
                self.cursor_col = (self.cursor_col - 1) % len(self.keys[self.cursor_row])
                
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            if not confirm_button_focus:
                # キーボード内での右移動
                self.cursor_col = (self.cursor_col + 1) % len(self.keys[self.cursor_row])
        
        # 文字入力（キーボード）
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z)) and not confirm_button_focus:
            if len(self.text) < self.max_length:
                # キー入力音を再生
                pyxel.play(0, 11)  # 音声チャンネル0、効果音11を再生
                
                key = self.keys[self.cursor_row][self.cursor_col]
                if key == '_':
                    self.text += ' '  # スペース
                elif key == '.':
                    # バックスペース
                    if self.text:
                        self.text = self.text[:-1]
                else:
                    self.text += key
        
        # 確定ボタン押下またはキーボード確定キー
        if confirm_button_focus and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z)):
            # 確定ボタンにフォーカスがある状態でスペースまたはZキーが押された
            # 確定音を再生
            pyxel.play(0, 12)  # 音声チャンネル0、効果音12を再生
            self.complete = True
            print("DEBUG: Confirm button activated with keyboard")
            
        # 確定（キーボードのエンターキーまたはXキー）
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_X):
            # 確定音を再生
            pyxel.play(0, 12)  # 音声チャンネル0、効果音12を再生
            self.complete = True
            print("DEBUG: Confirm activated with Return or X key")
            
    def draw(self):
        """キーボードの描画"""
        if not self.active:
            return
            
        # キーボード背景（半透明黒）
        pyxel.rect(self.x - 5, self.y - 25, 80, 90, 0)
        
        # 入力中のテキスト表示
        pyxel.text(self.x, self.y - 20, "ENTER YOUR NAME:", 7)
        # 入力欄の背景
        pyxel.rect(self.x - 1, self.y - 11, self.max_length * 5 + 2, 9, 1)
        # 入力テキスト表示
        name_x = self.x + (self.max_length * 4) // 2 - len(self.text) * 2
        pyxel.text(name_x, self.y - 10, self.text + "_", 7)
        
        # キーボード表示
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                key_x = self.x + j * 10
                key_y = self.y + i * 10
                
                # キーの背景（タップしやすくするため）
                if i == self.cursor_row and j == self.cursor_col:
                    # 選択中のキーは強調表示
                    pyxel.rect(key_x - 1, key_y - 1, 8, 8, 5)
                    color = 0
                else:
                    # それ以外のキーも少し背景をつける
                    pyxel.rect(key_x - 1, key_y - 1, 8, 8, 1)
                    color = 7
                    
                # キーの文字表示
                pyxel.text(key_x, key_y, key, color)
        
        # 確定ボタン（目立つ大きなボタン）
        confirm_button_y = self.y + len(self.keys) * 10 + 5
        
        # 確定ボタンにフォーカスがあるか確認
        confirm_button_focus = hasattr(self, 'confirm_button_focus') and self.confirm_button_focus
        
        # ボタンの背景（点滅効果）- フォーカスがある場合は明るい色で強調
        if confirm_button_focus:
            # フォーカス時はより目立つ点滅効果
            button_color = 10 if (pyxel.frame_count // 4) % 2 == 0 else 11  # 明るい緑と黄色で点滅
            border_color = 7  # 白いボーダー
            text_color = 0  # 黒いテキスト
        else:
            # 通常の表示
            button_color = 8 if (pyxel.frame_count // 8) % 2 == 0 else 5
            border_color = 6  # 通常のボーダー
            text_color = 0  # 黒いテキスト
            
        # ボタンの描画
        pyxel.rect(self.x - 1, confirm_button_y - 1, 70, 14, button_color)
        pyxel.rectb(self.x - 2, confirm_button_y - 2, 72, 16, border_color)  # ボーダー
        
        # 「確定」テキスト
        pyxel.text(self.x + 25, confirm_button_y + 3, "確定", text_color)
        
        # フォーカス時に追加の視覚的なヒント
        if confirm_button_focus:
            # 矢印マーカーでボタンが選択されていることを示す
            pyxel.text(self.x - 7, confirm_button_y + 3, ">", 7)  # 左側の矢印
            pyxel.text(self.x + 65, confirm_button_y + 3, "<", 7)  # 右側の矢印
        
        # 操作説明（小さめに）
        instruction_y = self.y + len(self.keys) * 10 + 22
        pyxel.text(self.x, instruction_y, "TAP KEY/Z:INPUT TAP/X:OK", 13)
        
    def activate(self):
        """キーボードを有効化"""
        self.active = True
        self.text = ""
        self.complete = False
        self.confirm_button_focus = False  # フォーカスをリセット
        
    def deactivate(self):
        """キーボードを無効化"""
        self.active = False
        
    def get_text(self):
        """入力されたテキストを取得"""
        return self.text