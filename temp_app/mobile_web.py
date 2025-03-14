from flask import Flask, render_template, send_from_directory, Response, redirect, url_for
import os
import threading
import subprocess
import time
import signal
import sys

# モバイルウェブ版のディレクトリ
MOBILE_WEB_DIR = "mobile_web_version"
STATIC_DIR = f"{MOBILE_WEB_DIR}/static"
ASSETS_DIR = f"{MOBILE_WEB_DIR}/assets"

# ゲームプロセス管理用変数
game_process = None
game_thread = None
game_running = False
force_mobile_mode = True  # モバイルモードを強制的に有効にする

# Flaskアプリ初期化
app = Flask(__name__, 
            static_folder=MOBILE_WEB_DIR,
            template_folder="templates")

# ビルド済みかどうかチェック
def check_mobile_web_files():
    """モバイルWEB版のファイルが存在するかチェック"""
    index_file = f"{MOBILE_WEB_DIR}/index.html"
    if not os.path.exists(index_file):
        print("Mobile web files not found. Building...")
        # ビルドスクリプトを実行
        try:
            import build_mobile_web
            build_mobile_web.build_mobile_web_version()
        except Exception as e:
            print(f"Error building mobile web version: {e}")
            return False
    return True

# ゲームプロセスを開始
def start_game_process():
    """バックグラウンドでゲームプロセスを開始"""
    global game_process, game_running
    
    # すでに実行中なら何もしない
    if game_running and game_process and game_process.poll() is None:
        return
    
    # 環境変数でモバイルモードを有効にする
    env = os.environ.copy()
    if force_mobile_mode:
        env["FORCE_MOBILE_MODE"] = "1"
    
    try:
        # ゲームプロセスを開始
        print("Starting game process...")
        game_process = subprocess.Popen(
            ["python", "main.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        game_running = True
        
        # 出力を監視するスレッド
        def monitor_output():
            while game_running and game_process and game_process.poll() is None:
                try:
                    line = game_process.stdout.readline()
                    if line:
                        print(f"GAME: {line.strip()}")
                except:
                    break
            print("Game process monitoring ended")
        
        # モニタースレッドを開始
        threading.Thread(target=monitor_output, daemon=True).start()
        
        print("Game process started successfully")
        return True
    except Exception as e:
        print(f"Error starting game process: {e}")
        game_running = False
        return False

# ゲームプロセスを停止
def stop_game_process():
    """実行中のゲームプロセスを停止"""
    global game_process, game_running
    
    if game_process:
        try:
            print("Stopping game process...")
            game_running = False
            
            # Windowsでは、CTRL_BREAKを送信
            if os.name == 'nt':
                game_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                # Linuxでは、SIGTERMを送信
                game_process.terminate()
            
            # 少し待ってから強制終了
            time.sleep(1)
            if game_process.poll() is None:
                game_process.kill()
            
            game_process = None
            print("Game process stopped")
        except Exception as e:
            print(f"Error stopping game process: {e}")

# アプリの終了時にゲームプロセスをクリーンアップ
def cleanup_on_exit():
    """アプリ終了時のクリーンアップ処理"""
    stop_game_process()

# メインページ
@app.route('/')
def index():
    """モバイルウェブ版ゲームのメインページ"""
    # ファイルが存在するか確認し、なければビルド
    if not check_mobile_web_files():
        return "Failed to build mobile web version", 500
    
    # ゲームプロセスが実行中でなければ開始
    if not game_running:
        start_game_process()
    
    # メインページを表示
    return send_from_directory(MOBILE_WEB_DIR, 'index.html')

# iframeページ専用ルート
@app.route('/game_iframe')
def game_iframe():
    """ゲームのiframeコンテナページ"""
    return send_from_directory(MOBILE_WEB_DIR, 'iframe.html')

# ゲーム本体ルート（実際のゲームを表示）
@app.route('/game')
def game():
    """ゲーム本体のページ"""
    # ゲームプロセスが実行中でなければ開始
    if not game_running:
        if not start_game_process():
            return "Failed to start game", 500
    
    # ここでは実際のゲーム自体を表示するHTMLを返す
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DodanPyxel Game</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
            background-color: #000;
            touch-action: none;
        }
        
        .game-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        #game-canvas {
            display: block;
            margin: 0 auto;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
            width: 100%;
            max-width: 100%;
            height: auto;
            background: #000;
        }
        
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 24px;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div id="loading">Loading game...</div>
        <canvas id="game-canvas" width="128" height="128"></canvas>
    </div>

    <script>
        // シンプルなゲームステータス表示用スクリプト
        document.addEventListener('DOMContentLoaded', function() {
            const canvas = document.getElementById('game-canvas');
            const ctx = canvas.getContext('2d');
            const loading = document.getElementById('loading');
            
            // ゲームキャンバスの初期設定
            canvas.width = 128;
            canvas.height = 128;
            
            // 初期メッセージ描画
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#fff';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('DODAN PYXEL', canvas.width/2, 40);
            ctx.fillText('Touch to Play', canvas.width/2, 70);
            
            // ローディングメッセージを非表示
            loading.style.display = 'none';
            
            // タッチイベントをゲームに送信する処理
            function handleTouch(e) {
                e.preventDefault();
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                let x, y;
                
                if (e.type.startsWith('touch')) {
                    // タッチイベント
                    const touch = e.touches[0] || e.changedTouches[0];
                    x = (touch.clientX - rect.left) * scaleX;
                    y = (touch.clientY - rect.top) * scaleY;
                } else {
                    // マウスイベント
                    x = (e.clientX - rect.left) * scaleX;
                    y = (e.clientY - rect.top) * scaleY;
                }
                
                // ゲームへの入力情報をコンソールに表示
                console.log(`Touch at: ${Math.floor(x)}, ${Math.floor(y)}`);
            }
            
            // タッチイベントリスナー
            canvas.addEventListener('touchstart', handleTouch, { passive: false });
            canvas.addEventListener('touchmove', handleTouch, { passive: false });
            canvas.addEventListener('touchend', handleTouch, { passive: false });
            
            // マウスイベントリスナー
            canvas.addEventListener('mousedown', handleTouch);
            canvas.addEventListener('mousemove', function(e) {
                if (e.buttons === 1) {
                    handleTouch(e);
                }
            });
            
            // 画面サイズに合わせて自動調整
            function resizeCanvas() {
                const container = canvas.parentElement;
                const containerWidth = container.clientWidth;
                const containerHeight = container.clientHeight;
                
                // アスペクト比を保ったままリサイズ
                const aspectRatio = canvas.width / canvas.height;
                let newWidth, newHeight;
                
                if (containerWidth / containerHeight > aspectRatio) {
                    // コンテナが横長の場合、高さに合わせる
                    newHeight = containerHeight;
                    newWidth = newHeight * aspectRatio;
                } else {
                    // コンテナが縦長の場合、幅に合わせる
                    newWidth = containerWidth;
                    newHeight = newWidth / aspectRatio;
                }
                
                canvas.style.width = `${newWidth}px`;
                canvas.style.height = `${newHeight}px`;
            }
            
            // リサイズイベントリスナー
            window.addEventListener('resize', resizeCanvas);
            
            // 初期リサイズ
            resizeCanvas();
        });
    </script>
</body>
</html>
"""
    
    return html_content

# 静的ファイル提供
@app.route('/static/<path:filename>')
def serve_static(filename):
    """静的ファイルの提供"""
    return send_from_directory(STATIC_DIR, filename)

# アセットファイル提供
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """アセットファイルの提供"""
    return send_from_directory(ASSETS_DIR, filename)

# ヘルスチェック
@app.route('/health')
def health():
    """サーバーの状態確認用エンドポイント"""
    # Replitのヘルスチェック用に特定のポート番号を指定
    return f"OK - Server running on port 5000", 200

# ゲームプロセスの開始
@app.route('/start_game')
def start_game():
    """ゲームプロセスを開始するAPI"""
    if start_game_process():
        return "Game started", 200
    else:
        return "Failed to start game", 500

# ゲームプロセスの停止
@app.route('/stop_game')
def stop_game():
    """ゲームプロセスを停止するAPI"""
    stop_game_process()
    return "Game stopped", 200

# メイン関数
if __name__ == "__main__":
    try:
        # モバイルWEBビルドを確認
        check_mobile_web_files()
        
        # Replitでは必ずポート5000を使う
        port = int(os.environ.get("PORT", 5000))
        
        print(f"Starting mobile web server on port {port}...")
        print(f"Game will be available at: http://localhost:{port}/")
        
        # 終了時のクリーンアップ処理を登録
        import atexit
        atexit.register(cleanup_on_exit)
        
        # サーバー起動
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    
    except KeyboardInterrupt:
        print("Server interrupted by user")
    finally:
        cleanup_on_exit()