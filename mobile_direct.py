from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import time
import subprocess
import threading
import signal
import atexit

app = Flask(__name__)

# ゲーム実行プロセス
game_process = None
# 前回のリロード時刻
last_reload_time = 0

def start_game_process():
    """バックグラウンドでゲームプロセスを開始する"""
    global game_process
    if game_process is not None:
        # 既存のプロセスを停止
        stop_game_process()
    
    # 新しいプロセスを開始
    print("Starting Pyxel game process...")
    game_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=dict(os.environ, FORCE_MOBILE_MODE="1")
    )
    
    # 出力をモニターするスレッド
    def monitor_output():
        for line in iter(game_process.stdout.readline, b''):
            print(f"GAME: {line.decode('utf-8', errors='replace').rstrip()}")
    
    threading.Thread(target=monitor_output, daemon=True).start()
    print("Game process started with PID:", game_process.pid)
    
    return game_process

def stop_game_process():
    """実行中のゲームプロセスを停止する"""
    global game_process
    if game_process is not None:
        print(f"Stopping game process (PID: {game_process.pid})...")
        try:
            os.kill(game_process.pid, signal.SIGTERM)
            game_process.terminate()
            game_process.wait(timeout=5)
        except Exception as e:
            print(f"Error stopping game process: {e}")
            try:
                os.kill(game_process.pid, signal.SIGKILL)
            except:
                pass
        game_process = None
        print("Game process stopped")

# アプリケーション終了時のクリーンアップ
def cleanup_on_exit():
    stop_game_process()

atexit.register(cleanup_on_exit)

@app.route('/')
def index():
    """メインページ - Pyxelゲームの実行を指示するページ"""
    # テンプレートを直接返す
    return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dodan Shooter - iPhone Compatible</title>
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
            touch-action: none;
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
            touch-action: manipulation;
        }
        button:active {
            background: #45a049;
        }
        .status {
            margin-top: 20px;
            font-style: italic;
            font-size: 14px;
        }
        .instructions {
            margin-top: 30px;
            text-align: left;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 5px;
            max-width: 400px;
        }
        .instructions h2 {
            font-size: 18px;
            margin-top: 0;
        }
        .instructions ul {
            padding-left: 20px;
        }
        .instructions li {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dodan Shooter - iPhoneブラウザ対応版</h1>
        <p>このゲームはiPhoneのブラウザで動作するように最適化されています。<br>下のボタンをタップしてゲームを開始してください。</p>
        
        <button id="startButton">ゲームを開始</button>
        
        <div class="status" id="statusText">読み込み準備中...</div>
        
        <div class="instructions">
            <h2>操作方法</h2>
            <ul>
                <li>画面左下の仮想パッドで移動</li>
                <li>画面右下の赤いボタンで発射</li>
                <li>敵を倒してスコアを稼ごう！</li>
                <li>パワーアップアイテムを取って強化しよう！</li>
            </ul>
        </div>
    </div>

    <script>
        const startButton = document.getElementById('startButton');
        const statusText = document.getElementById('statusText');
        
        // ゲームの状態を確認
        async function checkGameStatus() {
            try {
                const response = await fetch('/status');
                const status = await response.text();
                
                if (status === 'running') {
                    statusText.textContent = 'ゲーム実行中...';
                    startButton.textContent = 'ゲームを再起動';
                } else {
                    statusText.textContent = '準備完了';
                    startButton.textContent = 'ゲームを開始';
                }
            } catch (error) {
                statusText.textContent = 'エラー: ' + error.message;
            }
        }
        
        // ゲームを開始する
        async function startGame() {
            statusText.textContent = 'ゲーム起動中...';
            startButton.disabled = true;
            
            try {
                const response = await fetch('/start_game');
                if (response.ok) {
                    statusText.textContent = 'ゲーム実行中...';
                    startButton.textContent = 'ゲームを再起動';
                } else {
                    statusText.textContent = 'エラー: ' + await response.text();
                }
            } catch (error) {
                statusText.textContent = 'エラー: ' + error.message;
            }
            
            startButton.disabled = false;
        }
        
        // ボタンのクリックイベント
        startButton.addEventListener('click', startGame);
        
        // 初期状態の確認
        checkGameStatus();
        
        // 定期的にステータスチェック
        setInterval(checkGameStatus, 5000);
    </script>
</body>
</html>"""

@app.route('/start_game')
def start_game():
    """ゲームを開始する"""
    global last_reload_time
    current_time = time.time()
    
    # 前回のリロードから3秒以上経っている場合のみ処理（連続リロード防止）
    if current_time - last_reload_time > 3:
        last_reload_time = current_time
        start_game_process()
        
    return "Game started", 200

@app.route('/stop_game')
def stop_game():
    """ゲームを停止する"""
    stop_game_process()
    return "Game stopped", 200

@app.route('/status')
def status():
    """ゲームの状態を返す"""
    if game_process is not None and game_process.poll() is None:
        return "running", 200
    else:
        return "stopped", 200

if __name__ == "__main__":
    # テンプレートディレクトリの確認
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # モバイル用テンプレートの作成
    mobile_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dodan Shooter - iPhone Compatible</title>
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
            touch-action: none;
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
            touch-action: manipulation;
        }
        button:active {
            background: #45a049;
        }
        .status {
            margin-top: 20px;
            font-style: italic;
            font-size: 14px;
        }
        .instructions {
            margin-top: 30px;
            text-align: left;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 5px;
            max-width: 400px;
        }
        .instructions h2 {
            font-size: 18px;
            margin-top: 0;
        }
        .instructions ul {
            padding-left: 20px;
        }
        .instructions li {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dodan Shooter - iPhoneブラウザ対応版</h1>
        <p>このゲームはiPhoneのブラウザで動作するように最適化されています。<br>下のボタンをタップしてゲームを開始してください。</p>
        
        <button id="startButton">ゲームを開始</button>
        
        <div class="status" id="statusText">読み込み準備中...</div>
        
        <div class="instructions">
            <h2>操作方法</h2>
            <ul>
                <li>画面左下の仮想パッドで移動</li>
                <li>画面右下の赤いボタンで発射</li>
                <li>敵を倒してスコアを稼ごう！</li>
                <li>パワーアップアイテムを取って強化しよう！</li>
            </ul>
        </div>
    </div>

    <script>
        const startButton = document.getElementById('startButton');
        const statusText = document.getElementById('statusText');
        
        // ゲームの状態を確認
        async function checkGameStatus() {
            try {
                const response = await fetch('/status');
                const status = await response.text();
                
                if (status === 'running') {
                    statusText.textContent = 'ゲーム実行中...';
                    startButton.textContent = 'ゲームを再起動';
                } else {
                    statusText.textContent = '準備完了';
                    startButton.textContent = 'ゲームを開始';
                }
            } catch (error) {
                statusText.textContent = 'エラー: ' + error.message;
            }
        }
        
        // ゲームを開始する
        async function startGame() {
            statusText.textContent = 'ゲーム起動中...';
            startButton.disabled = true;
            
            try {
                const response = await fetch('/start_game');
                if (response.ok) {
                    statusText.textContent = 'ゲーム実行中...';
                    startButton.textContent = 'ゲームを再起動';
                } else {
                    statusText.textContent = 'エラー: ' + await response.text();
                }
            } catch (error) {
                statusText.textContent = 'エラー: ' + error.message;
            }
            
            startButton.disabled = false;
        }
        
        // ボタンのクリックイベント
        startButton.addEventListener('click', startGame);
        
        // 初期状態の確認
        checkGameStatus();
        
        // 定期的にステータスチェック
        setInterval(checkGameStatus, 5000);
    </script>
</body>
</html>
"""
    
    with open(os.path.join(templates_dir, "mobile_index.html"), "w") as f:
        f.write(mobile_template)
    
    print("Mobile Direct Web Server starting on port 5000...")
    app.run(host='0.0.0.0', port=5000)