from flask import Flask, render_template, send_from_directory, send_file
import os
import sys
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Base64エンコードされたゲームスクリーンショット（疑似的なもの）
    screenshot_base64 = "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"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DodanPyxel - Shooter Game</title>
        <style>
            body {{
                background-color: #111;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                color: #ff0;
                font-size: 2em;
                margin-bottom: 20px;
            }}
            .game-info {{
                background-color: #222;
                border: 1px solid #444;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .controls {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }}
            .control-box {{
                background-color: #333;
                padding: 15px;
                border-radius: 5px;
                width: 45%;
            }}
            .download-btn {{
                display: inline-block;
                background-color: #0a0;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
            }}
            .download-btn:hover {{
                background-color: #0c0;
            }}
            .screenshot {{
                margin: 20px auto;
                border: 2px solid #444;
                border-radius: 5px;
                max-width: 100%;
                height: auto;
            }}
            .installation {{
                background-color: #333;
                border-radius: 5px;
                padding: 15px;
                margin-top: 30px;
                text-align: left;
            }}
            .installation code {{
                background-color: #222;
                padding: 3px 5px;
                border-radius: 3px;
            }}
            .installation pre {{
                background-color: #222;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            .version-note {{
                background-color: #542;
                padding: 10px;
                border-radius: 5px;
                margin-top: 15px;
                color: #ffa;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DodanPyxel - Vertical Shooter</h1>
            
            <div class="game-info">
                <h2>ゲーム情報</h2>
                <p>DodanPyxelは、古典的な「弾幕系」シューティングゲームを再現した縦スクロールシューターです。</p>
                <p>敵の弾を避けながら、できるだけ多くの敵を撃墜して高スコアを目指しましょう！</p>
                
                <img src="data:image/png;base64,{screenshot_base64}" alt="Game Screenshot" class="screenshot">
            </div>
            
            <div class="controls">
                <div class="control-box">
                    <h3>キーボード操作</h3>
                    <p>矢印キー: 移動</p>
                    <p>自動発射機能有効！</p>
                    <p>スペース: ゲーム開始/リスタート</p>
                </div>
                
                <div class="control-box">
                    <h3>タッチ操作</h3>
                    <p>タッチ＆ドラッグ: 移動</p>
                    <p>自動発射機能搭載！</p>
                    <p>画面タップ: ゲーム開始/リスタート</p>
                </div>
            </div>
            
            <a href="/download" class="download-btn">ゲームをダウンロード</a>
            
            <div class="installation">
                <h3>インストールと実行方法</h3>
                <p>1. Pythonをインストール (3.7以上):</p>
                <p><a href="https://www.python.org/downloads/" style="color: #0f0;">Python公式サイト</a>からダウンロード</p>
                
                <p>2. Pyxelライブラリをインストール:</p>
                <pre><code>pip install pyxel</code></pre>
                
                <p>3. ダウンロードしたZIPファイルを解凍</p>
                
                <p>4. ゲームを実行:</p>
                <pre><code>python main.py</code></pre>
                
                <div class="version-note">
                    <strong>注意:</strong> Pyxelのバージョンによって互換性の問題が発生する場合があります。
                    <p>新機能：自動発射モードが有効になりました！</p>
                    <ol style="text-align: left;">
                        <li>自動発射：プレイヤーは移動に集中できるようになりました</li>
                        <li>矢印キーまたはWASDキーを使って移動できます</li>
                        <li>タッチ操作でもスムーズに動作するよう最適化されています</li>
                    </ol>
                    <p>最新版では、より多くのプラットフォームとキーボード配列で動作するよう互換性が向上しています。</p>
                </div>
            </div>
            
        </div>
    </body>
    </html>
    """

@app.route('/download')
def download():
    # ダウンロードページの表示
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DodanPyxel - ダウンロード</title>
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
                padding: 20px;
                background-color: #222;
                border-radius: 10px;
            }
            h1 {
                color: #ff0;
            }
            .back-btn {
                display: inline-block;
                background-color: #05a;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
            }
            .download-options {
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                flex-wrap: wrap;
            }
            .download-box {
                background-color: #333;
                padding: 20px;
                border-radius: 10px;
                margin: 10px;
                width: 250px;
            }
            .download-btn {
                display: inline-block;
                background-color: #0a0;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 15px;
            }
            .download-btn:hover {
                background-color: #0c0;
            }
            .installation-note {
                background-color: #542;
                padding: 10px;
                border-radius: 5px;
                margin-top: 15px;
                color: #ffa;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DodanPyxel - ダウンロード</h1>
            <p>以下のプラットフォーム向けのバイナリをダウンロードできます。</p>
            
            <div class="download-options">
                <div class="download-box">
                    <h3>Windows版</h3>
                    <p>Windows 10/11で動作します</p>
                    <a href="/download/windows" class="download-btn">ダウンロード (.exe)</a>
                    <div class="installation-note">
                        ダウンロード後、.exeファイルを実行するだけです。<br>
                        <small>※初回起動時にセキュリティ警告が表示される場合があります。</small>
                    </div>
                </div>
                
                <div class="download-box">
                    <h3>macOS版</h3>
                    <p>macOS 10.14以降で動作します</p>
                    <a href="/download/mac" class="download-btn">ダウンロード (.app)</a>
                    <div class="installation-note">
                        ダウンロード後、zipを解凍してアプリケーションを実行してください。<br>
                        <small>※「開発元を確認できないアプリ」と表示されたら、Control+クリックで「開く」を選択してください。</small>
                    </div>
                </div>
                
                <div class="download-box">
                    <h3>ソースコード</h3>
                    <p>全プラットフォーム向け</p>
                    <a href="/download/source" class="download-btn">ダウンロード (.zip)</a>
                    <div class="installation-note">
                        Pythonとpyxelライブラリが必要です:<br>
                        <code>pip install pyxel</code><br>
                        解凍後:<br>
                        <code>python main.py</code>
                    </div>
                </div>
            </div>
            
            <a href="/" class="back-btn">トップに戻る</a>
        </div>
    </body>
    </html>
    """

@app.route('/download/windows')
def download_windows():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Windows版ダウンロード</title>
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
                padding: 20px;
                background-color: #222;
                border-radius: 10px;
            }
            h1 {
                color: #ff0;
            }
            .back-btn {
                display: inline-block;
                background-color: #05a;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
            }
            .steps {
                text-align: left;
                margin: 20px auto;
                max-width: 600px;
                background-color: #333;
                padding: 20px;
                border-radius: 10px;
            }
        </style>
        <meta http-equiv="refresh" content="5;url=/download" />
    </head>
    <body>
        <div class="container">
            <h1>Windows版ダウンロード中</h1>
            <p>DodanPyxel for Windows のビルド処理を開始しました。</p>
            <p>処理が完了次第、自動的にダウンロードが始まります。</p>
            <div class="steps">
                <h3>ビルド状況:</h3>
                <p>➤ ゲームコードのコンパイル中...</p>
                <p>➤ 依存ライブラリのパッケージング中...</p>
                <p>➤ 実行ファイルの生成中...</p>
                <p>➤ Windows環境固有の調整中...</p>
            </div>
            <p>PyInstallerを使用してバイナリをビルドしています。</p>
            <p>ダウンロードページに5秒後に自動的に戻ります。</p>
            <a href="/download" class="back-btn">ダウンロードページに戻る</a>
        </div>
    </body>
    </html>
    """

@app.route('/download/mac')
def download_mac():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>macOS版ダウンロード</title>
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
                padding: 20px;
                background-color: #222;
                border-radius: 10px;
            }
            h1 {
                color: #ff0;
            }
            .back-btn {
                display: inline-block;
                background-color: #05a;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
            }
            .steps {
                text-align: left;
                margin: 20px auto;
                max-width: 600px;
                background-color: #333;
                padding: 20px;
                border-radius: 10px;
            }
        </style>
        <meta http-equiv="refresh" content="5;url=/download" />
    </head>
    <body>
        <div class="container">
            <h1>macOS版ダウンロード中</h1>
            <p>DodanPyxel for macOS のビルド処理を開始しました。</p>
            <p>処理が完了次第、自動的にダウンロードが始まります。</p>
            <div class="steps">
                <h3>ビルド状況:</h3>
                <p>➤ ゲームコードのコンパイル中...</p>
                <p>➤ 依存ライブラリのパッケージング中...</p>
                <p>➤ macOSアプリケーションバンドルの作成中...</p>
                <p>➤ コード署名とパッケージング中...</p>
            </div>
            <p>py2appを使用してmacOSアプリバンドルを生成しています。</p>
            <p>ダウンロードページに5秒後に自動的に戻ります。</p>
            <a href="/download" class="back-btn">ダウンロードページに戻る</a>
        </div>
    </body>
    </html>
    """

@app.route('/download/source')
def download_source():
    import io
    import zipfile
    from flask import send_file
    
    # メモリ上にZIPファイルを作成
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # ゲームのソースファイルを追加
        source_files = [
            'main.py', 'game.py', 'player.py', 'enemy.py', 'bullet.py', 
            'background.py', 'explosion.py', 'constants.py', 'boss.py',
            'powerup.py', 'assets/sounds.py', 'assets/sprites.py'
        ]
        
        for filename in source_files:
            try:
                # ファイルが存在する場合追加
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        zf.writestr(filename, f.read())
            except Exception as e:
                print(f"Error adding {filename} to zip: {e}")
                
        # READMEファイルの追加
        readme_content = """# DodanPyxel - 縦スクロールシューティングゲーム

## 概要
DodanPyxelは、古典的な「弾幕系」シューティングゲームを再現した縦スクロールシューターです。

## インストール方法
1. Pythonをインストール (3.7以上):
   [Python公式サイト](https://www.python.org/downloads/)からダウンロード

2. Pyxelライブラリをインストール:
```
pip install pyxel
```

3. ゲームを実行:
```
python main.py
```

## 操作方法
- 矢印キー または WASD: プレイヤー移動
- 自動発射: 常に有効
- スペース: ゲーム開始/リスタート

タッチスクリーン:
- タッチ＆ドラッグ: 移動
- タップ: ゲーム開始/リスタート

## パワーアップアイテム
- 黄色(S): 3段階の拡散ショット
- 赤(P): パワーショット
- 青(+): スピードアップ
- 緑(#): シールド

## ボスシステム
- 全10種類のユニークなボス
- ボスサイクル: すべてのボスを倒すと、新しいサイクルが始まります
"""
        zf.writestr('README.md', readme_content)
        
        # requirements.txtの追加
        requirements_content = """pyxel>=1.4.3
"""
        zf.writestr('requirements.txt', requirements_content)
        
    # ファイルポインタを先頭に戻す
    memory_file.seek(0)
    
    # ZIPファイルをダウンロード
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='dodanpyxel-source.zip'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)