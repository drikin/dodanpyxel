#!/usr/bin/env python3
# ハイスコアをリセットするスクリプト

from highscores import HighScores

def main():
    """ハイスコアをリセットする"""
    print("ハイスコアをリセットします...")
    high_scores = HighScores()
    high_scores.reset_scores()
    print("ハイスコアがリセットされました。")

if __name__ == "__main__":
    main()