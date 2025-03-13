#!/usr/bin/env python3
"""
DodanPyxel Web版作成スクリプト
このスクリプトは、Pyxel アプリをHTML5にコンバートするためのものです
"""

import os
import sys
import subprocess
import shutil
import tempfile

def create_temporary_package():
    """
    一時的なディレクトリに.pyxappファイルを作成する
    """
    print("Pyxelアプリをパッケージ化しています...")
    
    # 一時ディレクトリにメインファイルをコピー
    temp_dir = "temp_app"
    os.makedirs(temp_dir, exist_ok=True)
    
    # ゲームの必要なファイルをすべてコピー
    game_files = [
        "main.py", "game.py", "player.py", "enemy.py", 
        "bullet.py", "boss.py", "background.py", 
        "explosion.py", "powerup.py", "constants.py"
    ]
    
    for file in game_files:
        if os.path.exists(file):
            shutil.copy(file, temp_dir)
    
    # assetsディレクトリがあればコピー
    if os.path.exists("assets"):
        if os.path.exists(os.path.join(temp_dir, "assets")):
            shutil.rmtree(os.path.join(temp_dir, "assets"))
        shutil.copytree("assets", os.path.join(temp_dir, "assets"))
    
    # ここでPyxelのパッケージコマンドを実行
    try:
        subprocess.run(
            [sys.executable, "-m", "pyxel", "package", os.path.join(temp_dir, "main.py"), os.path.join(temp_dir, "game.pyxapp")],
            check=True
        )
        print("パッケージ化が成功しました！")
        return os.path.join(temp_dir, "game.pyxapp")
    except subprocess.CalledProcessError as e:
        print(f"パッケージ化中にエラーが発生しました: {e}")
        print("別の方法を試みます...")
        
        try:
            # 別の方法を試す - ディレクトリを指定
            subprocess.run(
                [sys.executable, "-m", "pyxel", "package", temp_dir, os.path.join(temp_dir, "game.pyxapp")],
                check=True
            )
            print("パッケージ化が成功しました！")
            return os.path.join(temp_dir, "game.pyxapp")
        except subprocess.CalledProcessError as e:
            print(f"再試行でもエラーが発生しました: {e}")
            return None

def convert_to_html(pyxapp_path):
    """
    .pyxappファイルをHTML5に変換する
    """
    if not pyxapp_path or not os.path.exists(pyxapp_path):
        print("パッケージファイルが見つかりません")
        return False
    
    print(".pyxappファイルをHTML5に変換しています...")
    web_dir = "public/web"
    os.makedirs(web_dir, exist_ok=True)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pyxel", "app2html", pyxapp_path, web_dir],
            check=True
        )
        print("HTML5への変換が成功しました！")
        
        # 念のためパーミッションを設定
        for root, dirs, files in os.walk(web_dir):
            for file in files:
                os.chmod(os.path.join(root, file), 0o644)
            for dir in dirs:
                os.chmod(os.path.join(root, dir), 0o755)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"HTML5への変換中にエラーが発生しました: {e}")
        return False

def create_web_version():
    """
    WebアプリのHTMLラッパーを作成する
    """
    pyxapp_path = create_temporary_package()
    if not pyxapp_path:
        print("パッケージ作成に失敗しました")
        return False
    
    success = convert_to_html(pyxapp_path)
    if not success:
        print("HTML変換に失敗しました")
        return False
    
    # ラッパーHTMLの作成は変換成功後に行われる
    create_wrapper_html()
    return True

def create_wrapper_html():
    """
    ゲームをラップするHTMLページを作成する
    """
    web_dir = "public/web"
    
    # ラッパーHTMLを作成
    wrapper_html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DodanPyxel シューティングゲーム</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a2e;
            color: #e6e6e6;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            width: 100%;
            padding: 20px;
            box-sizing: border-box;
        }
        
        h1 {
            text-align: center;
            color: #ff6b6b;
            margin-bottom: 30px;
        }
        
        .game-container {
            background-color: #222244;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .game-frame {
            width: 100%;
            max-width: 640px;
            height: 520px;
            border: none;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        .control-info {
            background-color: #2a2a4a;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            width: 100%;
            max-width: 640px;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #333355;
            color: #888;
            font-size: 0.9em;
            width: 100%;
        }
        
        .back-btn {
            display: inline-block;
            background-color: #4ecdc4;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 20px;
            transition: all 0.3s;
        }
        
        .back-btn:hover {
            background-color: #44b8b1;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DodanPyxel シューティングゲーム</h1>
        
        <div class="game-container">
            <iframe src="index.html" class="game-frame" frameborder="0" scrolling="no" allowfullscreen></iframe>
            
            <div class="control-info">
                <h2>ゲーム操作方法</h2>
                <p>
                    矢印キー: 移動<br>
                    Zキー: 発射 (常時自動発射も有効)<br>
                    Xキー: ボム発射<br>
                    Rキー: ゲームオーバー時にリスタート<br>
                    ESCキー: 一時停止/再開
                </p>
            </div>
            
            <a href="/" class="back-btn">トップページに戻る</a>
        </div>
        
        <div class="footer">
            <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(os.path.join(web_dir, "main.html"), "w") as f:
        f.write(wrapper_html)
    
    print("ラッパーHTMLを作成しました")

if __name__ == "__main__":
    if create_web_version():
        print("Web版の作成が完了しました！")
    else:
        print("Web版の作成に失敗しました")