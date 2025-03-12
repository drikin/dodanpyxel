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
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
                text-align: center;
                background-color: #f5f5f5;
            }
            h1 { 
                color: #333; 
                margin-bottom: 20px;
            }
            .container {
                background-color: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .download-btn { 
                display: inline-block; 
                margin: 15px; 
                padding: 15px 25px; 
                background-color: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 4px;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            .download-btn:hover { 
                background-color: #45a049; 
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .download-section {
                margin-top: 30px;
            }
            .platform-icon {
                display: block;
                font-size: 32px;
                margin-bottom: 10px;
            }
            .footer {
                margin-top: 40px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DodanPyxel シューティングゲーム</h1>
            <p>縦スクロールシューティングゲームをダウンロードして、プレイしてみましょう！</p>
            
            <div class="download-section">
                <a href="/download/windows" class="download-btn">
                    <span class="platform-icon">🪟</span>
                    Windows版
                </a>
                <a href="/download/mac" class="download-btn">
                    <span class="platform-icon">🍎</span>
                    Mac版
                </a>
                <a href="/download/source" class="download-btn">
                    <span class="platform-icon">📦</span>
                    ソースコード
                </a>
            </div>
            
            <div class="footer">
                <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
            </div>
        </div>
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
    return "Server is running on port 3000!"

if __name__ == '__main__':
    print("Starting Flask server on port 3000...")
    # ポートを3000に設定
    app.run(host='0.0.0.0', port=3000)