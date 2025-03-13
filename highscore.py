import os
import json
import pyxel

class HighScore:
    def __init__(self, max_entries=10):
        self.scores = []
        self.max_entries = max_entries
        self.file_path = "highscores.json"
        self.input_name = ""
        self.is_input_active = False
        self.current_score = 0
        self.load_scores()
        
    def load_scores(self):
        """スコアファイルを読み込む"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.scores = json.load(f)
                # スコアの降順にソート
                self.scores.sort(key=lambda x: x["score"], reverse=True)
                # 最大数に制限
                self.scores = self.scores[:self.max_entries]
            except Exception as e:
                print(f"スコア読み込みエラー: {e}")
                self.scores = []
        else:
            self.scores = []
    
    def save_scores(self):
        """スコアをファイルに保存する"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, ensure_ascii=False)
        except Exception as e:
            print(f"スコア保存エラー: {e}")
    
    def add_score(self, score, name):
        """新しいスコアを追加"""
        self.scores.append({"name": name, "score": score})
        # スコアの降順にソート
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # 最大数に制限
        self.scores = self.scores[:self.max_entries]
        # 保存
        self.save_scores()
    
    def is_high_score(self, score):
        """与えられたスコアがハイスコアかどうかを判定"""
        if len(self.scores) < self.max_entries:
            return True
        return score > min(entry["score"] for entry in self.scores)
    
    def start_name_input(self, score):
        """名前入力モードを開始"""
        self.is_input_active = True
        self.input_name = ""
        self.current_score = score
    
    def update_name_input(self):
        """名前入力の更新処理"""
        if not self.is_input_active:
            return False
            
        # 文字入力処理
        for i in range(48, 91):  # 0-9, A-Z
            if pyxel.btnp(i):
                char = chr(i)
                if len(self.input_name) < 8:  # 最大8文字まで
                    self.input_name += char
        
        # バックスペース
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.input_name) > 0:
            self.input_name = self.input_name[:-1]
        
        # エンターキーで確定
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            name = self.input_name if self.input_name else "PLAYER"
            self.add_score(self.current_score, name)
            self.is_input_active = False
            return True
            
        return False
    
    def draw_input_screen(self):
        """名前入力画面の描画"""
        if not self.is_input_active:
            return
            
        # 入力背景
        pyxel.rect(20, 70, 120, 60, 5)
        pyxel.rectb(20, 70, 120, 60, 7)
        
        # タイトルと説明
        pyxel.text(40, 80, "NEW HIGH SCORE!", 7)
        pyxel.text(40, 90, f"SCORE: {self.current_score}", 7)
        pyxel.text(40, 100, "ENTER YOUR NAME:", 7)
        
        # 入力フィールド
        pyxel.rectb(40, 110, 80, 10, 7)
        pyxel.text(45, 112, self.input_name + ("_" if pyxel.frame_count % 30 < 15 else ""), 7)
    
    def draw_high_scores(self, x, y):
        """ハイスコアの表示"""
        pyxel.text(x, y, "HIGH SCORES", 7)
        y += 10
        
        for i, entry in enumerate(self.scores):
            text = f"{i+1:2d}. {entry['name']:8s} {entry['score']:8d}"
            pyxel.text(x, y + i * 8, text, 7 if i > 2 else [10, 9, 8][i])