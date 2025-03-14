from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>シューティングゲームダウンロード</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; text-align: center; }
            h1 { color: #333; }
            .download-btn { 
                display: inline-block; 
                margin: 10px; 
                padding: 15px 25px; 
                background-color: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 4px;
                font-size: 18px;
            }
            .download-btn:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h1>シューティングゲームダウンロード</h1>
        <p>以下のプラットフォーム用のゲームをダウンロードできます：</p>
        <a href="/download/windows" class="download-btn">Windows版</a>
        <a href="/download/mac" class="download-btn">Mac版</a>
        <a href="/download/source" class="download-btn">ソースコード</a>
    </body>
    </html>
    """

@app.route('/download/<platform>')
def download(platform):
    if platform == 'windows':
        return send_from_directory('public/downloads', 'dodanpyxel-windows.zip', as_attachment=True)
    elif platform == 'mac':
        return send_from_directory('public/downloads', 'dodanpyxel-mac.zip', as_attachment=True)
    elif platform == 'source':
        return send_from_directory('public/downloads', 'dodanpyxel-source.zip', as_attachment=True)
    else:
        return "Invalid platform"

@app.route('/health')
def health():
    return "Server is running"

if __name__ == '__main__':
    # 設定されたポート、または3000をデフォルトとして使用
    port = int(os.environ.get('PORT', 3000))
    print(f"Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)