from flask import Flask, render_template, send_file, jsonify
import os
import subprocess
import sys
import signal
import atexit

app = Flask(__name__)

# グローバル変数でゲームプロセスを管理
game_process = None

def start_game_process():
    """ゲームプロセスを開始"""
    global game_process
    if game_process is None or game_process.poll() is not None:
        try:
            from custom_tag_web import create_html_with_custom_tags
            # まずHTMLを生成
            create_html_with_custom_tags()
            
            # プロセスがすでに終了している場合は新しいプロセスを開始
            game_process = None
            # カスタムタグサーバーを起動
            game_process = subprocess.Popen([
                sys.executable, 'custom_tag_server.py'
            ])
            return {"status": "started", "pid": game_process.pid}
        except Exception as e:
            error_message = str(e)
            return {"status": "error", "message": error_message}
    else:
        return {"status": "already_running", "pid": game_process.pid}

def stop_game_process():
    """ゲームプロセスを停止"""
    global game_process
    if game_process is not None:
        try:
            # プロセスを終了
            game_process.terminate()
            game_process.wait(timeout=5)  # 最大5秒待機
            game_process = None
            return {"status": "stopped"}
        except subprocess.TimeoutExpired:
            # 強制終了
            game_process.kill()
            game_process = None
            return {"status": "forcibly_stopped"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        return {"status": "not_running"}

@app.route('/')
def index():
    """メインページ"""
    # 自動的にゲームを開始する
    start_game_process()
    # iframeを使用してカスタムタグサーバーに接続
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Dodan Shooter - Pyxel</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: #000;
            }
            
            #game-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: none;
            }
        </style>
    </head>
    <body>
        <iframe id="game-container" src="http://0.0.0.0:8000/"></iframe>
    </body>
    </html>
    """
    return html

@app.route('/api/start')
def api_start():
    """ゲーム開始API"""
    result = start_game_process()
    return jsonify(result)

@app.route('/api/stop')
def api_stop():
    """ゲーム停止API"""
    result = stop_game_process()
    return jsonify(result)

@app.route('/health')
def health():
    """ヘルスチェック用エンドポイント"""
    return jsonify({"status": "ok"})

# アプリケーション終了時の処理
def cleanup_on_exit():
    global game_process
    if game_process is not None:
        game_process.terminate()
        try:
            game_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            game_process.kill()

# 終了時のクリーンアップを登録
atexit.register(cleanup_on_exit)

# SIGTERMシグナルハンドラ
def handle_sigterm(signum, frame):
    cleanup_on_exit()
    sys.exit(0)

# SIGTERMシグナルハンドラを登録
signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Minimal Flask Server starting on port {port}...")
    # 開始時にゲームプロセスを起動
    start_game_process()
    app.run(host='0.0.0.0', port=port)