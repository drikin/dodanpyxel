#!/usr/bin/env python3
"""
最新のコードを使ってWebビルドを生成するスクリプト
GitHub経由でアクセスする際、キャッシュが効かないようにタイムスタンプを含める
"""

import os
import shutil
import datetime
import subprocess
import random

def ensure_directory(directory):
    """指定されたディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_directory(directory):
    """指定されたディレクトリを空にする"""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error: {e}")

def generate_cache_buster():
    """キャッシュを無効にするための一意の文字列を生成"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = random.randint(1000, 9999)
    return f"{timestamp}_{random_part}"

def build_fresh_web_version():
    """常に最新のコードを反映したWeb版を構築する"""
    # 現在の時刻をキャッシュバスティングに使用
    cache_buster = generate_cache_buster()
    
    # web_buildディレクトリをクリーンアップ
    web_dir = "web_build"
    ensure_directory(web_dir)
    clean_directory(web_dir)
    
    # 最新のソースコードをtemp_appにコピー
    print("最新のソースコードをtemp_appにコピー中...")
    temp_dir = "temp_app"
    ensure_directory(temp_dir)
    
    # Python ファイルをコピー
    for filename in os.listdir("."):
        if filename.endswith(".py") and not filename.startswith("."):
            shutil.copy2(filename, os.path.join(temp_dir, filename))
    
    # assets ディレクトリをコピー
    if os.path.exists("assets"):
        assets_dir = os.path.join(temp_dir, "assets")
        ensure_directory(assets_dir)
        for filename in os.listdir("assets"):
            if filename.endswith(".py"):
                shutil.copy2(os.path.join("assets", filename), 
                            os.path.join(assets_dir, filename))
    
    # high_scores.json をコピー
    if os.path.exists("high_scores.json"):
        shutil.copy2("high_scores.json", os.path.join(temp_dir, "high_scores.json"))
    
    # Pyxelアプリをパッケージ化
    print("Pyxelアプリをパッケージ化中...")
    os.chdir(temp_dir)
    subprocess.run(["python", "-m", "pyxel", "package", ".", "main.py"])
    os.chdir("..")
    
    # pyxappファイルを指定のディレクトリにコピー
    pyxapp_src = os.path.join(temp_dir, f"{os.path.basename(temp_dir)}.pyxapp")
    pyxapp_dest = f"{web_dir}/game_{cache_buster}.pyxapp"
    
    if os.path.exists(pyxapp_src):
        shutil.copy2(pyxapp_src, pyxapp_dest)
        print(f"pyxappファイルを {pyxapp_dest} にコピーしました")
    else:
        print(f"エラー: {pyxapp_src} が見つかりません")
        return False
    
    # HTMLに変換
    html_dest = f"{web_dir}/game_{cache_buster}.html"
    subprocess.run(["python", "-m", "pyxel", "app2html", pyxapp_dest])
    
    # 生成されたHTMLファイルを探す
    # ディレクトリを確認
    for f in os.listdir("."):
        if f.endswith(".html") and f.startswith(os.path.basename(pyxapp_dest)):
            print(f"生成されたHTMLファイル: {f}")
            generated_html = f
            break
    else:
        # ルートディレクトリで確認
        original_file = os.path.basename(pyxapp_dest)
        for f in os.listdir(".."):
            if f.endswith(".html") and original_file in f:
                generated_html = os.path.join("..", f)
                print(f"生成されたHTMLファイル: {generated_html}")
                break
        else:
            # もうひとつの可能性を確認
            generated_html = f"{pyxapp_dest}.html"
    if os.path.exists(generated_html):
        shutil.move(generated_html, html_dest)
        print(f"HTMLファイルを {html_dest} に生成しました")
    else:
        print(f"エラー: {generated_html} が見つかりません")
        return False
    
    # インデックスファイルを作成 - ゲームへのリンクを含む
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LAST DESCENT: THE FINAL HOPE</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #111;
            color: #eee;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        h1 {{
            color: #ffcc00;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            margin-bottom: 30px;
        }}
        .game-container {{
            margin: 20px 0;
            padding: 20px;
            background-color: #222;
            border-radius: 10px;
            max-width: 800px;
            width: 100%;
        }}
        .button {{
            display: inline-block;
            background-color: #ff3366;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 10px;
            transition: background-color 0.3s;
        }}
        .button:hover {{
            background-color: #cc0044;
        }}
        .timestamp {{
            font-size: 12px;
            color: #666;
            margin-top: 40px;
        }}
        .instructions {{
            margin: 20px 0;
            padding: 15px;
            background-color: #333;
            border-radius: 5px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <h1>LAST DESCENT: THE FINAL HOPE</h1>
    
    <div class="game-container">
        <h2>Play Now</h2>
        <p>A vertical scrolling shooter game with challenging bosses and power-ups!</p>
        <a href="game_{cache_buster}.html" class="button">Launch Game</a>
        
        <div class="instructions">
            <h3>Controls:</h3>
            <ul>
                <li>Arrow Keys / WASD: Move ship</li>
                <li>Z Key: Shoot</li>
                <li>Space: Start game / Skip intro</li>
            </ul>
        </div>
    </div>
    
    <p class="timestamp">Build: {cache_buster}</p>
</body>
</html>
"""
    
    with open(f"{web_dir}/index.html", "w") as f:
        f.write(index_html)
        
    print(f"インデックスページを生成しました: {web_dir}/index.html")
    print(f"キャッシュバスティング文字列: {cache_buster}")
    
    return True

if __name__ == "__main__":
    print("新鮮なWebビルドを生成中...")
    if build_fresh_web_version():
        print("ビルド成功！")
    else:
        print("ビルド失敗...")