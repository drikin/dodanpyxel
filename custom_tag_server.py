from flask import Flask, send_from_directory, redirect, url_for, abort
import os
import custom_tag_web
import sys

app = Flask(__name__)

CUSTOM_WEB_DIR = "custom_web"  # カスタムタグを使用したウェブ出力ディレクトリ
GAME_DIR = "."  # ゲームのソースコードディレクトリ

@app.route('/')
def index():
    """メインページ"""
    # カスタムタグHTMLファイルの存在確認
    if not os.path.exists(os.path.join(CUSTOM_WEB_DIR, "index.html")):
        # HTMLファイルが存在しない場合は生成
        custom_tag_web.create_html_with_custom_tags()
    
    return send_from_directory(CUSTOM_WEB_DIR, 'index.html')

@app.route('/main.py')
def serve_main_py():
    """main.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'main.py')

@app.route('/game.py')
def serve_game_py():
    """game.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'game.py')

@app.route('/player.py')
def serve_player_py():
    """player.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'player.py')

@app.route('/enemy.py')
def serve_enemy_py():
    """enemy.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'enemy.py')

@app.route('/bullet.py')
def serve_bullet_py():
    """bullet.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'bullet.py')

@app.route('/powerup.py')
def serve_powerup_py():
    """powerup.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'powerup.py')

@app.route('/explosion.py')
def serve_explosion_py():
    """explosion.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'explosion.py')

@app.route('/background.py')
def serve_background_py():
    """background.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'background.py')

@app.route('/highscores.py')
def serve_highscores_py():
    """highscores.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'highscores.py')

@app.route('/boss.py')
def serve_boss_py():
    """boss.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'boss.py')

@app.route('/assets/sprites.py')
def serve_sprites_py():
    """sprites.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory('assets', 'sprites.py')

@app.route('/assets/sounds.py')
def serve_sounds_py():
    """sounds.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory('assets', 'sounds.py')

@app.route('/constants.py')
def serve_constants_py():
    """constants.pyファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'constants.py')

@app.route('/high_scores.json')
def serve_highscores_json():
    """high_scores.jsonファイルを提供 - Pyxelカスタムタグが必要"""
    return send_from_directory(GAME_DIR, 'high_scores.json')

@app.route('/<path:path>')
def serve_file(path):
    """その他の静的ファイル"""
    # まずカスタムWebディレクトリを確認
    if os.path.exists(os.path.join(CUSTOM_WEB_DIR, path)):
        return send_from_directory(CUSTOM_WEB_DIR, path)
    
    # 次にゲームのソースディレクトリを確認
    if os.path.exists(os.path.join(GAME_DIR, path)):
        return send_from_directory(GAME_DIR, path)
    
    # 見つからない場合は404
    abort(404)

if __name__ == "__main__":
    print(f"カスタムタグWebサーバーを起動しています（ポート5000）...")
    print(f"ファイル提供元: {os.path.abspath(CUSTOM_WEB_DIR)}")
    print(f"ゲームソース提供元: {os.path.abspath(GAME_DIR)}")
    
    # ディレクトリの存在確認
    if not os.path.exists(CUSTOM_WEB_DIR):
        os.makedirs(CUSTOM_WEB_DIR)
        print(f"{CUSTOM_WEB_DIR} ディレクトリを作成しました。")
    
    # HTMLファイルの存在確認と生成
    if not os.path.exists(os.path.join(CUSTOM_WEB_DIR, "index.html")):
        custom_tag_web.create_html_with_custom_tags()
    
    # 警告メッセージの非表示
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    
    app.run(host='0.0.0.0', port=5000)