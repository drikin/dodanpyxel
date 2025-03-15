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
            h2 {
                color: #555;
                margin-top: 30px;
                font-size: 22px;
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
            .info-box {
                background-color: #f8f9fa;
                border-left: 4px solid #4CAF50;
                padding: 15px;
                margin: 25px 0;
                text-align: left;
                border-radius: 4px;
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
                <a href="/download/source" class="download-btn">
                    <span class="platform-icon">📦</span>
                    ソースコード
                </a>
            </div>
            
            <div class="info-box">
                <h2>バイナリのビルド方法</h2>
                <p>ソースコードパッケージには、PyInstallerを使ってWindowsやMac用の実行可能ファイルを作成する方法が含まれています。</p>
                <p>詳細は同梱の <strong>build_guide.txt</strong> ファイルを参照してください。</p>
                <p>基本的な手順:</p>
                <ol>
                    <li>Python 3.8以上をインストール</li>
                    <li>必要なライブラリをインストール：<code>pip install pyxel pyinstaller</code></li>
                    <li>PyInstallerコマンドを実行してバイナリを生成</li>
                </ol>
            </div>
            
            <div class="info-box">
                <h2>ゲーム操作方法</h2>
                <p>
                    矢印キー: 移動<br>
                    Zキー: 発射 (常時自動発射も有効)<br>
                    Xキー: ボム発射<br>
                    ESCキー: 終了
                </p>
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