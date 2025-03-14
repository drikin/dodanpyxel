from flask import Flask, send_from_directory, redirect
import os
import subprocess
import threading
import signal
import atexit

app = Flask(__name__)

# ゲームプロセス
game_process = None

def start_game_process():
    """ゲームプロセスを開始"""
    global game_process
    if game_process is not None:
        # 既存プロセスの停止
        stop_game_process()
    
    # 新しいプロセスを開始
    print("Starting game process...")
    game_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=dict(os.environ, FORCE_MOBILE_MODE="1")
    )
    
    # 出力監視スレッド
    threading.Thread(target=lambda: [print(f"GAME: {line.decode('utf-8', errors='replace').strip()}") 
                                     for line in iter(game_process.stdout.readline, b'')], 
                     daemon=True).start()
    
    return game_process

def stop_game_process():
    """ゲームプロセスを停止"""
    global game_process
    if game_process is not None:
        print(f"Stopping game process (PID: {game_process.pid})...")
        try:
            os.kill(game_process.pid, signal.SIGTERM)
            game_process.terminate()
            game_process.wait(timeout=3)
        except Exception as e:
            print(f"Error stopping game: {e}")
            try:
                os.kill(game_process.pid, signal.SIGKILL)
            except:
                pass
        game_process = None

# アプリケーション終了時のクリーンアップ
atexit.register(stop_game_process)

# 静的ファイルディレクトリの作成
static_dir = "static_iphone"
os.makedirs(static_dir, exist_ok=True)

# HTMLファイルの作成
html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dodan Shooter - iPhoneブラウザ対応版</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 20px;
            box-sizing: border-box;
            text-align: center;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }
        p {
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.5;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        button:active {
            background: #45a049;
        }
        .status {
            margin-top: 20px;
            font-style: italic;
        }
        .instructions {
            margin-top: 30px;
            text-align: left;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dodan Shooter - iPhoneブラウザ対応版</h1>
        <p>このゲームはiPhoneのブラウザで動作するように最適化されています。<br>下のボタンをタップしてゲームを開始してください。</p>
        
        <button id="startButton">ゲームを開始</button>
        
        <div class="status" id="statusText">準備中...</div>
        
        <div class="instructions">
            <h2>操作方法</h2>
            <ul>
                <li>画面左下の仮想パッドで移動</li>
                <li>画面右下の赤いボタンで発射</li>
                <li>敵を倒してスコアを稼ごう！</li>
            </ul>
        </div>
    </div>

    <script>
        document.getElementById('startButton').addEventListener('click', function() {
            fetch('/start_game')
                .then(response => {
                    document.getElementById('statusText').textContent = 'ゲーム起動中...';
                    if (response.ok) {
                        document.getElementById('statusText').textContent = 'ゲーム実行中';
                    } else {
                        document.getElementById('statusText').textContent = 'エラーが発生しました';
                    }
                })
                .catch(error => {
                    document.getElementById('statusText').textContent = 'エラー: ' + error.message;
                });
        });
    </script>
</body>
</html>
"""

with open(os.path.join(static_dir, "index.html"), "w") as f:
    f.write(html_content)

@app.route('/')
def index():
    """メインページ"""
    # 直接HTMLコンテンツを返す
    return html_content

@app.route('/static/<path:path>')
def serve_static(path):
    """静的ファイルの提供"""
    # 明示的にCORS対応
    resp = send_from_directory(static_dir, path)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/start_game')
def start_game_api():
    """ゲームプロセスを開始するAPI"""
    start_game_process()
    return "Game started", 200

@app.route('/stop_game')
def stop_game_api():
    """ゲームプロセスを停止するAPI"""
    stop_game_process()
    return "Game stopped", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"iPhone Direct Web Server starting on port {port}...")
    app.run(host='0.0.0.0', port=port)