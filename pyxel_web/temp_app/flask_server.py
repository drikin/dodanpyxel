from flask import Flask, render_template, send_from_directory, redirect
import os
from create_windows_zip import create_windows_zip
from create_mac_zip import create_mac_zip
from create_source_zip import create_source_zip

app = Flask(__name__, 
            static_folder='web_static',
            template_folder='web_static')

# ゲームパッケージのビルド
def build_game_packages():
    # ダウンロードディレクトリを確認
    if not os.path.exists('web_static/downloads'):
        os.makedirs('web_static/downloads', exist_ok=True)
    
    # 各プラットフォーム用のZIPファイルを生成
    try:
        create_windows_zip()
        create_mac_zip()
        create_source_zip()
        print("All game packages built successfully")
    except Exception as e:
        print(f"Error building game packages: {e}")

# トップページ
@app.route('/')
def index():
    return app.send_static_file('index.html')

# ダウンロードページ
@app.route('/download')
def download():
    return app.send_static_file('download.html')

# Windowsパッケージダウンロード
@app.route('/download/windows')
def download_windows():
    return send_from_directory('web_static/downloads', 'dodanpyxel-windows.zip')

# macOSパッケージダウンロード
@app.route('/download/mac')
def download_mac():
    return send_from_directory('web_static/downloads', 'dodanpyxel-mac.zip')

# ソースコードパッケージダウンロード
@app.route('/download/source')
def download_source():
    return send_from_directory('web_static/downloads', 'dodanpyxel-source.zip')

# 静的ファイルハンドリング
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    # サーバー起動前にゲームパッケージをビルド
    build_game_packages()
    
    # Flask開発サーバー起動
    app.run(host='0.0.0.0', port=5000, debug=True)