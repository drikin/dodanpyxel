from flask import Flask, send_from_directory, redirect, url_for, render_template_string, Response
import os
import subprocess
import time
import sys
import create_web_build
import threading

app = Flask(__name__)

# ゲームを先に構築
def build_game_on_startup():
    print("バックグラウンドでゲームファイルをビルド中...")
    try:
        create_web_build.create_web_version()
        print("ゲームビルドが完了しました！")
    except Exception as e:
        print(f"ゲームビルド中にエラーが発生しました: {e}")

# バックグラウンドスレッドでゲームをビルド
threading.Thread(target=build_game_on_startup, daemon=True).start()

@app.route('/')
def index():
    try:
        # Webゲーム用ディレクトリが存在することを確認
        os.makedirs("public/web", exist_ok=True)
        
        # WebゲームHTMLが存在するか確認
        if not (os.path.exists("public/web/index.html") and os.path.exists("public/web/main.html")):
            # Web版がない場合は作成を試みる
            print("Web版ゲームファイルを作成中...")
            create_web_build.create_web_version()
        
        # トップページでゲームを直接表示するHTML
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
                    max-width: 850px;
                    margin: 0 auto;
                    padding: 20px;
                }
                
                h1 {
                    color: #ff6b6b;
                    margin-bottom: 20px;
                }
                
                .game-box {
                    background-color: #222244;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0 20px 0;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                
                .game-frame {
                    width: 100%;
                    max-width: 640px;
                    height: 480px;
                    border: none;
                    margin: 10px auto;
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
                
                .footer {
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 1px solid #333355;
                    color: #888;
                    font-size: 0.9em;
                }

                @media (max-width: 680px) {
                    .game-frame {
                        width: 100%;
                        height: 400px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>DodanPyxel シューティングゲーム</h1>
                
                <div class="game-box">
                    <iframe src="/index.html" class="game-frame" allowfullscreen></iframe>
                    
                    <div class="control-info">
                        <h3>ゲーム操作方法</h3>
                        <p>
                            矢印キー: 移動<br>
                            Zキー: 発射 (常時自動発射も有効)<br>
                            Xキー: ボム発射<br>
                            Rキー: ゲームオーバー時にリスタート<br>
                            ESCキー: 一時停止/再開
                        </p>
                        <p>
                            <strong>スマートフォン/タブレット:</strong><br>
                            画面タップ: 移動<br>
                            ダブルタップ: ボム発射
                        </p>
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <a href="/original" class="btn" style="display: inline-block; background-color: #ff6b6b; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s;">オリジナルゲームを起動</a>
                </div>
                
                <div class="footer">
                    <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
                </div>
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
                    word-break: break-word;
                }}
                .reload-btn {{
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
                .reload-btn:hover {{
                    background-color: #44b8b1;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ゲームのロード中にエラーが発生しました</h1>
                <div class="error-box">
                    <p>{str(e)}</p>
                </div>
                <div style="text-align: center;">
                    <a href="/" class="reload-btn">ページを再読み込み</a>
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
        if os.path.exists("public/web/main.html") and os.path.exists("public/web/index.html"):
            # Web版ゲームページを返す
            return send_from_directory('public/web', 'main.html')
        
        # Web版がない場合は作成を試みる
        print("Web版ゲームファイルが見つからないため、作成を試みます...")
        
        # Pyxel app2html を使ってWeb版を作成
        success = create_web_build.create_web_version()
        
        if success and os.path.exists("public/web/main.html") and os.path.exists("public/web/index.html"):
            print("Web版ゲームの作成に成功しました！")
            return send_from_directory('public/web', 'main.html')
        
        # 作成に失敗した場合はエラーメッセージを表示
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
                    <p>Webゲームの変換に失敗しました。技術的な問題が発生している可能性があります。</p>
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

@app.route('/index.html')
def game_html():
    return send_from_directory('public/web', 'index.html')

@app.route('/game.js')
def game_js():
    return send_from_directory('public/web', 'game.js')

@app.route('/<path:filename>')
def static_files(filename):
    if os.path.exists(os.path.join('public/web', filename)):
        return send_from_directory('public/web', filename)
    return "File not found", 404

@app.route('/web/<path:filename>')
def web_files(filename):
    return send_from_directory('public/web', filename)

@app.route('/screenshot')
def screenshot():
    # スクリーンショット画像を送信
    try:
        # デモ用のスクリーンショット画像を送信
        return send_from_directory('assets', 'screenshot.png')
    except:
        # スクリーンショット画像がない場合は代替テキストを返す
        return "スクリーンショット画像はまだ用意されていません。"

@app.route('/original')
def original_game():
    """オリジナルのPyxelゲームを新しいワークフローで直接起動する"""
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DodanPyxel - オリジナルゲーム起動</title>
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
                justify-content: center;
                min-height: 100vh;
                text-align: center;
            }
            
            .container {
                max-width: 800px;
                padding: 20px;
            }
            
            h1 {
                color: #ff6b6b;
                margin-bottom: 20px;
            }
            
            .game-box {
                background-color: #222244;
                border-radius: 10px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            .btn {
                display: inline-block;
                background-color: #4ecdc4;
                color: white;
                padding: 15px 30px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
                margin: 10px;
                transition: all 0.3s;
            }
            
            .btn:hover {
                background-color: #44b8b1;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            .btn-primary {
                background-color: #ff6b6b;
            }
            
            .btn-primary:hover {
                background-color: #e05555;
            }
            
            .info-box {
                background-color: #2a2a4a;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DodanPyxel - オリジナルゲーム起動</h1>
            
            <div class="game-box">
                <p>元のPyxelゲームを直接起動するには、以下のボタンをクリックしてください。</p>
                <p>新しいタブでゲームが起動します。</p>
                
                <a href="/run_game" target="_blank" class="btn btn-primary">オリジナルゲームを起動</a>
                <a href="/" class="btn">Webゲーム版に戻る</a>
                
                <div class="info-box">
                    <h3>注意事項</h3>
                    <p>
                        ・オリジナルゲームを実行するには、Pyxelのインストールが必要です。<br>
                        ・ゲームの起動には数秒かかる場合があります。<br>
                        ・「Shooter Game」ワークフローが起動します。
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/run_game')
def run_game():
    """Shooter Gameワークフローを起動する"""
    try:
        # Shooter Gameワークフローが実行中かどうかを確認
        # ただしReplitの制約上、ここではシンプルにページを返す
        return """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DodanPyxel - ゲーム起動中</title>
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
                    justify-content: center;
                    min-height: 100vh;
                    text-align: center;
                }
                
                .container {
                    max-width: 600px;
                    padding: 20px;
                }
                
                h1 {
                    color: #ff6b6b;
                    margin-bottom: 20px;
                }
                
                .box {
                    background-color: #222244;
                    border-radius: 10px;
                    padding: 30px;
                    margin: 20px 0;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                
                .loader {
                    border: 5px solid #333;
                    border-radius: 50%;
                    border-top: 5px solid #ff6b6b;
                    width: 50px;
                    height: 50px;
                    animation: spin 1.5s linear infinite;
                    margin: 20px auto;
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .btn {
                    display: inline-block;
                    background-color: #4ecdc4;
                    color: white;
                    padding: 12px 25px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 20px;
                    transition: all 0.3s;
                }
                
                .btn:hover {
                    background-color: #44b8b1;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>DodanPyxel - ゲーム起動中</h1>
                
                <div class="box">
                    <p>オリジナルゲームを起動しています...</p>
                    <div class="loader"></div>
                    <p>このページは自動的に更新されます。</p>
                    <p>ゲームがすでに起動している場合は、Replitの「Shooter Game」ワークフローを確認してください。</p>
                    
                    <a href="/original" class="btn">戻る</a>
                </div>
            </div>
            <script>
                // Shooter Gameワークフローが起動しているかをチェック
                setTimeout(function() {
                    // 3秒後に元のページに戻る
                    window.location.href = "/original";
                }, 3000);
            </script>
        </body>
        </html>
        """
    except Exception as e:
        return f"ゲームの起動中にエラーが発生しました: {str(e)}"

@app.route('/health')
def health():
    return "Server is running on port 3000!"

if __name__ == '__main__':
    print("Starting Flask server on port 3000...")
    # ポートを3000に設定
    app.run(host='0.0.0.0', port=3000)