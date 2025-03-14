from flask import Flask, send_from_directory, send_file, redirect, request, make_response
import os
import custom_tag_web
import platform
import socket
import json

app = Flask(__name__)

# カスタムタグHTMLを生成
custom_tag_web.create_html_with_custom_tags()

@app.route('/')
def index():
    """メインページ"""
    # iPhoneの場合はiPhone特化版にリダイレクト
    user_agent = request.headers.get('User-Agent', '').lower()
    if 'iphone' in user_agent or 'ipad' in user_agent:
        return redirect('/iphone')
    return send_file('custom_web/index.html')

@app.route('/ping')
def ping():
    """簡単な動作確認用エンドポイント"""
    return "Pong! Server is running."

@app.route('/test')
def test():
    """シンプルなHTML表示テスト"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background-color: #333; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
            h1 { color: #ffcc00; }
            p { margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>Pyxel Custom Tag Test</h1>
        <p>このページが表示されればサーバーは正常に動作しています。</p>
        <p><a href="/" style="color: #6cf;">メインページに戻る</a></p>
    </body>
    </html>
    """

@app.route('/device-info')
def device_info():
    """デバイス情報を表示 (開発用)"""
    device_data = {
        "user_agent": request.headers.get('User-Agent', 'Unknown'),
        "is_iphone": 'iphone' in request.headers.get('User-Agent', '').lower(),
        "is_ipad": 'ipad' in request.headers.get('User-Agent', '').lower(),
        "is_mobile": any(x in request.headers.get('User-Agent', '').lower() for x in ['mobile', 'android', 'iphone', 'ipad']),
        "python_version": platform.python_version(),
        "system": platform.system(),
        "headers": dict(request.headers),
        "host_ip": socket.gethostbyname(socket.gethostname())
    }
    
    # 見やすいHTML形式で返す
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>デバイス情報</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background-color: #222; color: #eee; font-family: monospace; padding: 20px; }}
            h1 {{ color: #ffcc00; }}
            .data {{ background-color: #333; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            pre {{ margin: 0; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <h1>デバイス情報</h1>
        <div class="data">
            <pre>{json.dumps(device_data, indent=2, ensure_ascii=False)}</pre>
        </div>
        <p><a href="/" style="color: #6cf;">メインページに戻る</a></p>
    </body>
    </html>
    """
    return html

@app.route('/main.py')
def serve_main_py():
    """main.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('main.py')

@app.route('/game.py')
def serve_game_py():
    """game.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('game.py')

@app.route('/player.py')
def serve_player_py():
    """player.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('player.py')

@app.route('/enemy.py')
def serve_enemy_py():
    """enemy.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('enemy.py')

@app.route('/bullet.py')
def serve_bullet_py():
    """bullet.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('bullet.py')

@app.route('/powerup.py')
def serve_powerup_py():
    """powerup.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('powerup.py')

@app.route('/explosion.py')
def serve_explosion_py():
    """explosion.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('explosion.py')

@app.route('/background.py')
def serve_background_py():
    """background.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('background.py')

@app.route('/highscores.py')
def serve_highscores_py():
    """highscores.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('highscores.py')

@app.route('/boss.py')
def serve_boss_py():
    """boss.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('boss.py')

@app.route('/assets/sprites.py')
def serve_sprites_py():
    """sprites.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('assets/sprites.py')

@app.route('/assets/sounds.py')
def serve_sounds_py():
    """sounds.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('assets/sounds.py')

@app.route('/constants.py')
def serve_constants_py():
    """constants.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('constants.py')

@app.route('/high_scores.json')
def serve_highscores_json():
    """high_scores.jsonファイルを提供 - Pyxelカスタムタグが必要"""
    return send_file('high_scores.json')

@app.route('/game')
def play_game():
    """Pyxelゲームのウェブ版（app2html生成版）を提供"""
    return send_file('workspace.html')

@app.route('/play')
def play_redirect():
    """ゲームページへのリダイレクト"""
    return redirect('/game')

@app.route('/iphone')
def iphone_version():
    """iPhone最適化版ゲームページ"""
    return send_file('static_iphone/index.html')

@app.route('/static_iphone/<path:filename>')
def serve_iphone_static(filename):
    """iPhone用静的ファイルの提供"""
    return send_from_directory('static_iphone', filename)

@app.route('/<path:path>')
def serve_file(path):
    """その他の静的ファイル"""
    if os.path.exists(path):
        return send_file(path)
    return f"File {path} not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Custom Tag Web Server starting on port {port}...")
    # Replitの環境で正しく動作するために必要な設定
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)