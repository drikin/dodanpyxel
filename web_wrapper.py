from flask import Flask, render_template, send_from_directory
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DodanPyxel - Shooter Game</title>
        <style>
            body {
                background-color: #111;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: #ff0;
                font-size: 2em;
                margin-bottom: 20px;
            }
            .game-info {
                background-color: #222;
                border: 1px solid #444;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .controls {
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }
            .control-box {
                background-color: #333;
                padding: 15px;
                border-radius: 5px;
                width: 45%;
            }
            .download-btn {
                display: inline-block;
                background-color: #0a0;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
            }
            .download-btn:hover {
                background-color: #0c0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DodanPyxel - Vertical Shooter</h1>
            
            <div class="game-info">
                <h2>ゲーム情報</h2>
                <p>DodanPyxelは、古典的な「弾幕系」シューティングゲームを再現した縦スクロールシューターです。</p>
                <p>敵の弾を避けながら、できるだけ多くの敵を撃墜して高スコアを目指しましょう！</p>
            </div>
            
            <div class="controls">
                <div class="control-box">
                    <h3>キーボード操作</h3>
                    <p>矢印キー: 移動</p>
                    <p>Zキー: 発射</p>
                    <p>スペース: ゲーム開始/リスタート</p>
                </div>
                
                <div class="control-box">
                    <h3>タッチ操作</h3>
                    <p>タッチ＆ドラッグ: 移動</p>
                    <p>右下の赤いボタン: 発射</p>
                    <p>画面タップ: ゲーム開始/リスタート</p>
                </div>
            </div>
            
            <a href="/download" class="download-btn">ゲームをダウンロード</a>
            
            <p style="margin-top: 40px;">
                注: このゲームを実行するには、Pythonとpyxelライブラリが必要です。<br>
                インストール方法: <code>pip install pyxel</code>
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/download')
def download():
    # ZIPファイルを作成
    import zipfile
    import tempfile
    
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, 'shooter_game.zip')
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # ゲームのソースファイルを追加
        source_files = [
            'main.py', 'game.py', 'player.py', 'enemy.py', 
            'bullet.py', 'explosion.py', 'background.py', 
            'constants.py'
        ]
        
        # アセットフォルダを追加
        if os.path.exists('assets'):
            for root, _, files in os.walk('assets'):
                for file in files:
                    if file.endswith('.py'):
                        source_files.append(os.path.join(root, file))
        
        for file in source_files:
            if os.path.exists(file):
                zipf.write(file)
        
        # READMEファイルを追加
        readme = """# DodanPyxel シューティングゲーム

縦スクロールシューティングゲーム (Pyxel製)

## 必要条件
- Python 3.7以上
- Pyxelライブラリ

## インストール方法
```
pip install pyxel
```

## 実行方法
```
python main.py
```

## 操作方法
- 矢印キー: 移動
- Zキー: 発射
- スペース: ゲーム開始/リスタート

## タッチ操作
- タッチ＆ドラッグ: 移動
- 右下の赤いボタン: 発射
- 画面タップ: ゲーム開始/リスタート
"""
        zipf.writestr('README.md', readme)
    
    # ファイルを送信
    return send_from_directory(temp_dir, 'shooter_game.zip', as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)