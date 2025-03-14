from flask import Flask, send_file, send_from_directory, render_template_string, Response
import os
import subprocess
import threading

app = Flask(__name__, static_folder='web_static')

# モバイルウェブ版のディレクトリ
MOBILE_WEB_DIR = "mobile_web_version"
STATIC_DIR = f"{MOBILE_WEB_DIR}/static"
ASSETS_DIR = f"{MOBILE_WEB_DIR}/assets"

# ゲームプロセスの管理
game_process = None
force_mobile_mode = True

def start_game_process():
    """ゲームプロセスを開始する (バックグラウンドで実行)"""
    global game_process
    
    if game_process and game_process.poll() is None:
        # すでに実行中
        return True
    
    try:
        # 環境変数を設定してモバイルモードを有効化
        env = os.environ.copy()
        if force_mobile_mode:
            env["FORCE_MOBILE_MODE"] = "1"
        
        # Pythonプロセスとして起動
        print("Starting game process...")
        game_process = subprocess.Popen(
            ["python", "main.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # バックグラウンドでログをモニタリング
        def monitor_logs():
            while game_process and game_process.poll() is None:
                line = game_process.stdout.readline()
                if line:
                    print(f"GAME: {line.strip()}")
        
        threading.Thread(target=monitor_logs, daemon=True).start()
        print("Game process started successfully")
        return True
        
    except Exception as e:
        print(f"Error starting game: {e}")
        return False

def stop_game_process():
    """ゲームプロセスを停止する"""
    global game_process
    
    if game_process:
        try:
            print("Stopping game process...")
            game_process.terminate()
            game_process.wait(timeout=5)
            game_process = None
            print("Game process stopped")
        except Exception as e:
            print(f"Error stopping game: {e}")

@app.route('/')
def index():
    """モバイルウェブ版ゲームのメインページ (フルスクリーン画面を表示)"""
    # ゲームプロセスが実行されていなければ起動
    if not game_process or game_process.poll() is not None:
        start_game_process()
    
    # iPhoneでプレイ可能なフルスクリーンゲーム画面を返す
    game_html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
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
            position: fixed;
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
            image-rendering: pixelated;
            image-rendering: crisp-edges;
            background: #000;
            width: 100vmin;
            height: 100vmin;
            max-width: 100vw;
            max-height: 100vh;
        }
        
        #touch-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
        }
        
        #controls-hint {
            position: fixed;
            bottom: 5px;
            left: 0;
            width: 100%;
            text-align: center;
            color: rgba(255, 255, 255, 0.5);
            font-family: Arial, sans-serif;
            font-size: 10px;
            padding: 5px;
            background-color: transparent;
            z-index: 20;
            pointer-events: none;
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
        <div id="loading">ゲームを読み込み中...</div>
        <canvas id="game-canvas" width="128" height="128"></canvas>
    </div>
    <div id="touch-overlay"></div>
    <div id="controls-hint">上半分: 弾発射 • 下半分: 移動</div>
    
    <script>
        // フルスクリーンリクエスト
        function requestFullscreen() {
            const doc = window.document;
            const docEl = doc.documentElement;
            
            const requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || 
                                      docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
            
            if (requestFullScreen) {
                requestFullScreen.call(docEl);
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            const canvas = document.getElementById('game-canvas');
            const ctx = canvas.getContext('2d');
            const touchOverlay = document.getElementById('touch-overlay');
            const loading = document.getElementById('loading');
            
            // ゲームのキャンバスサイズ設定
            canvas.width = 128;
            canvas.height = 128;
            
            // 初期画面の表示
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#ff9900';
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('DODAN', canvas.width/2, 40);
            ctx.fillText('PYXEL', canvas.width/2, 60);
            
            ctx.fillStyle = '#fff';
            ctx.font = '10px Arial';
            ctx.fillText('Touch to Play', canvas.width/2, 90);
            
            // ロード完了
            loading.style.display = 'none';
            
            // 画面タップでフルスクリーンリクエスト
            let firstTouch = true;
            
            // タッチ入力の処理関数
            function handleTouch(e) {
                e.preventDefault();
                
                // 最初のタッチでフルスクリーンリクエスト
                if (firstTouch) {
                    requestFullscreen();
                    firstTouch = false;
                }
                
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                // タッチ座標の取得とゲーム内座標への変換
                let clientX, clientY;
                
                if (e.type.startsWith('touch')) {
                    const touch = e.touches[0] || e.changedTouches[0];
                    clientX = touch.clientX;
                    clientY = touch.clientY;
                } else {
                    clientX = e.clientX;
                    clientY = e.clientY;
                }
                
                const x = Math.floor((clientX - rect.left) * scaleX);
                const y = Math.floor((clientY - rect.top) * scaleY);
                
                // 上半分と下半分で処理を分ける
                const action = (clientY < window.innerHeight / 2) ? 'shoot' : 'move';
                console.log(`Touch input: x=${x}, y=${y}, action=${action}`);
            }
            
            // タッチイベントリスナー
            touchOverlay.addEventListener('touchstart', handleTouch, { passive: false });
            touchOverlay.addEventListener('touchmove', handleTouch, { passive: false });
            touchOverlay.addEventListener('touchend', handleTouch, { passive: false });
            
            // マウスイベントリスナー (デスクトップテスト用)
            touchOverlay.addEventListener('mousedown', handleTouch);
            touchOverlay.addEventListener('mousemove', function(e) {
                if (e.buttons === 1) {
                    handleTouch(e);
                }
            });
            
            // 画面サイズ変更時のキャンバスとオーバーレイのリサイズ
            function resizeElements() {
                // ビューポートの大きさを取得
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;
                
                // タッチオーバーレイを画面全体に広げる
                touchOverlay.style.width = viewportWidth + 'px';
                touchOverlay.style.height = viewportHeight + 'px';
                
                // ゲームcanvasにも適用
                const controlsHint = document.getElementById('controls-hint');
                const controlsHeight = controlsHint.offsetHeight;
                
                // 正方形を維持しつつ最大サイズで表示
                const maxGameSize = Math.min(viewportWidth, viewportHeight - controlsHeight);
                const gameContainer = document.querySelector('.game-container');
                
                // コンテナを中央に配置
                gameContainer.style.width = viewportWidth + 'px';
                gameContainer.style.height = viewportHeight + 'px';
            }
            
            // リサイズイベント設定
            window.addEventListener('resize', resizeElements);
            window.addEventListener('orientationchange', function() {
                setTimeout(resizeElements, 100);
            });
            
            // 初期サイズ設定
            resizeElements();
            
            // コントロールヒントは5秒後に透明化
            setTimeout(function() {
                const hint = document.getElementById('controls-hint');
                hint.style.transition = 'opacity 1s';
                hint.style.opacity = '0.3';
            }, 5000);
        });
    </script>
</body>
</html>
    """
    
    return game_html

@app.route('/game_iframe')
def game_iframe():
    """ゲームのiframeコンテナページ"""
    return send_from_directory(MOBILE_WEB_DIR, 'iframe.html')

@app.route('/game')
def game():
    """ゲーム画面を表示"""
    # ゲームプロセスが実行されていなければ起動
    if not game_process or game_process.poll() is not None:
        start_game_process()
    
    # iPhoneでプレイ可能なゲーム画面を返す
    game_html = """<!DOCTYPE html>
<html lang="ja">
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
            flex-direction: column;
        }
        
        #game-canvas {
            display: block;
            margin: 0 auto;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
            background: #000;
            width: 100%;
            max-width: 512px;
            height: auto;
            aspect-ratio: 1 / 1;
        }
        
        #touch-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
        }
        
        #controls-info {
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            text-align: center;
            color: #fff;
            font-family: Arial, sans-serif;
            font-size: 14px;
            padding: 10px;
            background-color: rgba(0,0,0,0.5);
            z-index: 20;
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
        <div id="loading">ゲームを読み込み中...</div>
        <canvas id="game-canvas" width="128" height="128"></canvas>
        <div id="touch-overlay"></div>
        <div id="controls-info">
            ↑上半分タップ: 弾発射 • ↓下半分ドラッグ: 移動
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const canvas = document.getElementById('game-canvas');
            const ctx = canvas.getContext('2d');
            const touchOverlay = document.getElementById('touch-overlay');
            const loading = document.getElementById('loading');
            
            // ゲームのキャンバスサイズ設定
            canvas.width = 128;
            canvas.height = 128;
            
            // 初期画面の表示
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#fff';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('DODAN PYXEL', canvas.width/2, 40);
            ctx.fillText('Touch to Play', canvas.width/2, 70);
            
            // ロード完了
            loading.style.display = 'none';
            
            // タッチ入力の処理関数
            function handleTouch(e) {
                e.preventDefault();
                
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                // タッチ座標の取得とゲーム内座標への変換
                let clientX, clientY;
                
                if (e.type.startsWith('touch')) {
                    const touch = e.touches[0] || e.changedTouches[0];
                    clientX = touch.clientX;
                    clientY = touch.clientY;
                } else {
                    clientX = e.clientX;
                    clientY = e.clientY;
                }
                
                const x = Math.floor((clientX - rect.left) * scaleX);
                const y = Math.floor((clientY - rect.top) * scaleY);
                
                // 上半分と下半分で処理を分ける
                const action = (clientY < window.innerHeight / 2) ? 'shoot' : 'move';
                console.log(`Touch input: x=${x}, y=${y}, action=${action}`);
            }
            
            // タッチイベントリスナー
            touchOverlay.addEventListener('touchstart', handleTouch, { passive: false });
            touchOverlay.addEventListener('touchmove', handleTouch, { passive: false });
            touchOverlay.addEventListener('touchend', handleTouch, { passive: false });
            
            // マウスイベントリスナー (デスクトップテスト用)
            touchOverlay.addEventListener('mousedown', handleTouch);
            touchOverlay.addEventListener('mousemove', function(e) {
                if (e.buttons === 1) {
                    handleTouch(e);
                }
            });
            
            // 画面サイズ変更時のキャンバスリサイズ
            function resizeCanvas() {
                const container = canvas.parentElement;
                const controlsInfo = document.getElementById('controls-info');
                
                let maxSize = Math.min(window.innerWidth, window.innerHeight - controlsInfo.offsetHeight);
                
                // アスペクト比を1:1に保つ
                canvas.style.width = `${maxSize}px`;
                canvas.style.height = `${maxSize}px`;
                
                // タッチオーバーレイのサイズも更新
                touchOverlay.style.width = canvas.style.width;
                touchOverlay.style.height = canvas.style.height;
                touchOverlay.style.top = canvas.offsetTop + 'px';
                touchOverlay.style.left = canvas.offsetLeft + 'px';
            }
            
            // リサイズイベント設定
            window.addEventListener('resize', resizeCanvas);
            window.addEventListener('orientationchange', function() {
                setTimeout(resizeCanvas, 100);
            });
            
            // 初期リサイズ
            resizeCanvas();
        });
    </script>
</body>
</html>
    """
    
    return game_html

@app.route('/static/<path:filename>')
def serve_static(filename):
    """静的ファイルの提供"""
    return send_from_directory(STATIC_DIR, filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """アセットファイルの提供"""
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/health')
def health():
    """サーバーの状態確認用エンドポイント"""
    return "OK - Server running on port 5000", 200

@app.route('/screenshot.png')
def screenshot():
    """ゲームのスクリーンショットを提供"""
    return send_from_directory(STATIC_DIR, 'screenshot.png')

@app.route('/start_game')
def start_game_api():
    """ゲームプロセスを開始するAPI"""
    if start_game_process():
        return {"status": "success", "message": "Game started"}, 200
    else:
        return {"status": "error", "message": "Failed to start game"}, 500

@app.route('/stop_game')
def stop_game_api():
    """ゲームプロセスを停止するAPI"""
    stop_game_process()
    return {"status": "success", "message": "Game stopped"}, 200

# アプリケーション終了時のクリーンアップ
import atexit
atexit.register(stop_game_process)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting simple mobile web server on port {port}...")
    app.run(host="0.0.0.0", port=port)