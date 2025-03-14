from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="web_version")

# URLルート: トップページ
@app.route('/')
def index():
    """ゲームのWebブラウザ版を提供"""
    return send_from_directory('web_version', 'index.html')

# URLルート: 静的ファイル
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('web_version', path)

# URLルート: ヘルスチェック
@app.route('/health')
def health():
    """サーバーの状態確認用エンドポイント"""
    return "OK", 200

if __name__ == "__main__":
    # Replitで推奨されるポート5000を使用
    port = 5000
    
    print(f"Starting web server on port {port}...")
    print(f"Web game will be available at: http://localhost:{port}/")
    
    # Flaskサーバーを起動
    app.run(host="0.0.0.0", port=port)