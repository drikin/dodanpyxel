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
        pyxel.text(x, y, "HIGH SCORES", title_color)
        y += 10
        
        if not self.scores:
            pyxel.text(x, y, "NO SCORES YET", text_color)
            return
        
        for i, score_data in enumerate(self.scores):
            color = highlight_color if i < 3 else text_color  # トップ3は特別な色
            name = score_data["name"]
            score = score_data["score"]
            pyxel.text(x, y + i * 8, f"{i+1:2d}. {name:<8} {score:>8}", color)


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
        
    def update(self):
        """キーボード入力の更新"""
        if not self.active:
            return
            
        # カーソル移動
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.cursor_row = (self.cursor_row - 1) % len(self.keys)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.cursor_row = (self.cursor_row + 1) % len(self.keys)
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.cursor_col = (self.cursor_col - 1) % len(self.keys[self.cursor_row])
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.cursor_col = (self.cursor_col + 1) % len(self.keys[self.cursor_row])
            
        # 文字入力
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
            if len(self.text) < self.max_length:
                key = self.keys[self.cursor_row][self.cursor_col]
                if key == '_':
                    self.text += ' '  # スペース
                elif key == '.':
                    # バックスペース
                    if self.text:
                        self.text = self.text[:-1]
                else:
                    self.text += key
            
        # 確定
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_X):
            self.complete = True
            
    def draw(self):
        """キーボードの描画"""
        if not self.active:
            return
            
        # 入力中のテキスト表示
        pyxel.text(self.x, self.y - 20, "ENTER YOUR NAME:", 7)
        name_x = self.x + (self.max_length * 4) // 2 - len(self.text) * 2
        pyxel.text(name_x, self.y - 10, self.text + "_", 7)
        
        # キーボード表示
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                key_x = self.x + j * 10
                key_y = self.y + i * 10
                
                # 選択中のキーは異なる色で表示
                if i == self.cursor_row and j == self.cursor_col:
                    pyxel.rect(key_x - 1, key_y - 1, 8, 8, 5)
                    color = 0
                else:
                    color = 7
                    
                pyxel.text(key_x, key_y, key, color)
                
        # 操作説明
        pyxel.text(self.x, self.y + len(self.keys) * 10 + 5, "Z:INPUT X:ENTER", 13)
        
    def activate(self):
        """キーボードを有効化"""
        self.active = True
        self.text = ""
        self.complete = False
        
    def deactivate(self):
        """キーボードを無効化"""
        self.active = False
        
    def get_text(self):
        """入力されたテキストを取得"""
        return self.text