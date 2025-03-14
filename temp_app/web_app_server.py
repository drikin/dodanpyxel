import os
import sys
import time
import pyxel
from flask import Flask, render_template, send_from_directory, redirect, url_for

app = Flask(__name__, static_folder="web_version", template_folder="web_version")

# Web版の生成フラグ（初回アクセス時のみ生成）
web_version_built = False

def ensure_directory(directory):
    """指定されたディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def build_web_version():
    """ゲームのウェブ版をビルドする"""
    global web_version_built
    
    # すでに生成済みならスキップ
    if web_version_built:
        return True

    # 出力先ディレクトリの準備
    output_dir = "web_version"
    ensure_directory(output_dir)
    
    # Pyxelアプリケーションをウェブ形式に変換
    print("Building web version...")
    
    try:
        # App2htmlが利用可能ならそれを使う (Pyxel 2.0.0+)
        if hasattr(pyxel, 'app2html'):
            pyxel.app2html("main.py", html_file=f"{output_dir}/index.html", server=False)
            print("Successfully converted game to web version using pyxel.app2html")
            web_version_built = True
            return True
        else:
            print("Error: This version of Pyxel does not support app2html. Please use Pyxel 2.0.0 or higher.")
            return False
    except Exception as e:
        print(f"Error building web version: {e}")
        return False

# URLルート: トップページ
@app.route('/')
def index():
    """ゲームのWebブラウザ版へのリンクを表示"""
    # Web版の生成
    if not build_web_version():
        return "Failed to build web version. Please check the server logs.", 500
    
    # ゲームページへリダイレクト
    return redirect(url_for('game'))

# URLルート: ゲームページ
@app.route('/game')
def game():
    """ゲームのWebブラウザ版を提供"""
    # Web版の生成
    if not build_web_version():
        return "Failed to build web version. Please check the server logs.", 500
    
    # index.htmlを返す
    return send_from_directory('web_version', 'index.html')

# URLルート: ヘルスチェック
@app.route('/health')
def health():
    """サーバーの状態確認用エンドポイント"""
    return "OK", 200

if __name__ == "__main__":
    # Port3000は既に使用されているので4000を使用
    port = os.environ.get("PORT", 4000)
    
    print(f"Starting web app server on port {port}...")
    print(f"Web game will be available at: http://localhost:{port}/game")
    
    # Flaskサーバーを起動
    app.run(host="0.0.0.0", port=int(port))