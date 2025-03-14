from flask import Flask, render_template_string, send_from_directory, jsonify
import os
import subprocess
import threading
import time

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
        env=dict(os.environ, FORCE_MOBILE_MODE="1")
    )
    
    return game_process

def stop_game_process():
    """ゲームプロセスを停止"""
    global game_process
    if game_process is not None:
        print(f"Stopping game process (PID: {game_process.pid})...")
        try:
            game_process.terminate()
            game_process.wait(timeout=3)
        except Exception as e:
            print(f"Error stopping game: {e}")
        game_process = None

# HTMLコンテンツ
HTML_CONTENT = """
<!DOCTYPE html>
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
            fetch('/api/start')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('statusText').textContent = data.message;
                })
                .catch(error => {
                    document.getElementById('statusText').textContent = 'エラー: ' + error.message;
                });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """メインページ"""
    return HTML_CONTENT

@app.route('/api/start')
def api_start():
    """ゲーム開始API"""
    start_game_process()
    return jsonify({"message": "ゲームを開始しました！画面に注目してください。", "status": "success"})

@app.route('/api/stop')
def api_stop():
    """ゲーム停止API"""
    stop_game_process()
    return jsonify({"message": "ゲームを停止しました", "status": "success"})

@app.route('/health')
def health():
    """ヘルスチェック用エンドポイント"""
    return jsonify({"status": "ok", "message": "サーバーは正常に動作しています"})

if __name__ == '__main__':
    print("Starting simple Flask server on port 5000...")
    # atexit.register(stop_game_process)  # アプリケーション終了時のクリーンアップ
    app.run(host='0.0.0.0', port=5000, debug=False)