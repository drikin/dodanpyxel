from flask import Flask, send_from_directory
import os

app = Flask(__name__)

PYXEL_WEB_DIR = "pyxel_web"  # Pyxelのウェブ出力ディレクトリ

@app.route('/')
def index():
    """メインページ"""
    return send_from_directory(PYXEL_WEB_DIR, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    """その他の静的ファイル"""
    return send_from_directory(PYXEL_WEB_DIR, path)

if __name__ == "__main__":
    print(f"Starting web server on port 5000...")
    print(f"Serving files from: {os.path.abspath(PYXEL_WEB_DIR)}")
    
    # ディレクトリの存在確認
    if not os.path.exists(PYXEL_WEB_DIR):
        print(f"警告: {PYXEL_WEB_DIR} ディレクトリが見つかりません。")
        print("先に build_pyxel_web_fixed.py を実行してください。")
    
    # HTMLファイルの存在確認
    if not os.path.exists(os.path.join(PYXEL_WEB_DIR, "index.html")):
        print(f"警告: {PYXEL_WEB_DIR}/index.html ファイルが見つかりません。")
    
    app.run(host='0.0.0.0', port=5000)