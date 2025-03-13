from flask import Flask, send_from_directory, redirect, url_for, render_template_string
import os
import subprocess
import time
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
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
                text-align: center;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            
            h1 {
                color: #ff6b6b;
                margin-bottom: 30px;
            }
            
            h2 {
                color: #4ecdc4;
                margin-top: 30px;
            }
            
            .game-box {
                background-color: #222244;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            
            .game-frame {
                width: 100%;
                max-width: 640px;
                height: 480px;
                border: none;
                margin: 20px auto;
                display: block;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }
            
            .control-info {
                background-color: #2a2a4a;
                border-radius: 8px;
                padding: 15px;
                margin: 20px auto;
                max-width: 600px;
                text-align: left;
            }
            
            .play-btn {
                display: inline-block;
                background-color: #ff6b6b;
                color: white;
                padding: 15px 30px;
                margin: 20px 0;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
                font-size: 18px;
                transition: all 0.3s;
            }
            
            .play-btn:hover {
                background-color: #ff8e8e;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #333355;
                color: #888;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DodanPyxel シューティングゲーム</h1>
            
            <div class="game-box">
                <h2>ブラウザでプレイ！</h2>
                <p>Pyxel製の縦スクロールシューティングゲームをブラウザで直接プレイ！</p>
                
                <a href="/play" class="play-btn">今すぐプレイ!</a>
                
                <div class="control-info">
                    <h3>ゲーム操作方法</h3>
                    <p>
                        矢印キー: 移動<br>
                        Zキー: 発射 (常時自動発射も有効)<br>
                        Xキー: ボム発射<br>
                        ESCキー: 終了
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/download/<platform>')
def download(platform):
    if platform == 'windows':
        return send_from_directory('public/downloads', 'dodanpyxel-windows.zip', as_attachment=True)
    elif platform == 'mac':
        return send_from_directory('public/downloads', 'dodanpyxel-mac.zip', as_attachment=True)
    elif platform == 'linux':
        return send_from_directory('public/downloads', 'dodanpyxel-linux.zip', as_attachment=True)
    elif platform == 'source':
        return send_from_directory('public/downloads', 'dodanpyxel-source.zip', as_attachment=True)
    else:
        return "Invalid platform"

@app.route('/play')
def play():
    try:
        # Webゲーム用ディレクトリが存在することを確認
        os.makedirs("public/web", exist_ok=True)
        
        # すでにWebゲームファイルが存在するか確認
        if os.path.exists("public/web/main.html") and os.path.exists("public/web/game.js"):
            # Web版ゲームページを返す
            return send_from_directory('public/web', 'main.html')
        
        # Web版がない場合はエラーメッセージを表示
        return """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DodanPyxel - ゲーム準備中</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #1a1a2e;
                    color: #e6e6e6;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    text-align: center;
                    margin: 0;
                    padding: 20px;
                }
                
                .container {
                    background-color: #222244;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                    max-width: 600px;
                    width: 100%;
                }
                
                h1 {
                    color: #ff6b6b;
                    margin-bottom: 20px;
                }
                
                p {
                    font-size: 18px;
                    line-height: 1.6;
                }
                
                .error-box {
                    background-color: #3a2a3a;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 20px 0;
                    text-align: left;
                    color: #ffaaaa;
                }
                
                .continue-btn {
                    display: inline-block;
                    background-color: #4ecdc4;
                    color: white;
                    padding: 15px 30px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 30px;
                    transition: all 0.3s;
                }
                
                .continue-btn:hover {
                    background-color: #44b8b1;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>DodanPyxel - シューティングゲーム</h1>
                <p>申し訳ありませんが、Web版ゲームの準備中にエラーが発生しました。</p>
                
                <div class="error-box">
                    <p>Webゲームファイルが見つかりません。</p>
                </div>
                
                <p>Web版の問題を解決しています。しばらくしてから再度お試しください。</p>
                
                <a href="/" class="continue-btn">トップページに戻る</a>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>エラー</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 20px;
                    background-color: #1a1a2e;
                    color: #e6e6e6;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 800px;
                    width: 100%;
                    background-color: #222244;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                }}
                h1 {{ 
                    color: #ff6b6b; 
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .error-box {{ 
                    background-color: #2a2a4a; 
                    border-left: 3px solid #ff6b6b; 
                    padding: 20px; 
                    border-radius: 5px; 
                    margin: 20px 0;
                }}
                .back-btn {{
                    display: inline-block;
                    background-color: #4ecdc4;
                    color: white;
                    padding: 12px 25px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 20px;
                    transition: all 0.3s;
                    text-align: center;
                }}
                .back-btn:hover {{
                    background-color: #44b8b1;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Web版の準備中にエラーが発生しました</h1>
                <div class="error-box">
                    <p>{str(e)}</p>
                </div>
                <div style="text-align: center;">
                    <a href="/" class="back-btn">トップページに戻る</a>
                </div>
            </div>
        </body>
        </html>
        """

@app.route('/screenshot')
def screenshot():
    # スクリーンショット画像を送信
    try:
        # デモ用のスクリーンショット画像を送信
        return send_from_directory('assets', 'screenshot.png')
    except:
        # スクリーンショット画像がない場合は代替テキストを返す
        return "スクリーンショット画像はまだ用意されていません。"

@app.route('/health')
def health():
    return "Server is running on port 3000!"

if __name__ == '__main__':
    print("Starting Flask server on port 3000...")
    # ポートを3000に設定
    app.run(host='0.0.0.0', port=3000)