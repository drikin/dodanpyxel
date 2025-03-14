from flask import Flask, send_from_directory, redirect
import os
import build_pyxel_web_fixed
import threading
import time

app = Flask(__name__, static_folder='pyxel_web')
WEB_DIR = "pyxel_web"

# 初期化時にウェブビルドを実行
build_thread = None

def run_build():
    """バックグラウンドでビルドを実行"""
    try:
        build_pyxel_web_fixed.main()
        print("Webビルドが完了しました")
    except Exception as e:
        print(f"Webビルドエラー: {e}")

@app.route('/')
def index():
    """メインページ - index.htmlにリダイレクト"""
    # index.htmlが存在するか確認し、存在しなければリビルド
    if not os.path.exists(os.path.join(WEB_DIR, "index.html")):
        # メインファイル名が違う可能性があるため、拡張子で検索
        if not os.path.exists(WEB_DIR):
            os.makedirs(WEB_DIR)
            
        html_files = [f for f in os.listdir(WEB_DIR) if f.endswith('.html')] if os.path.exists(WEB_DIR) else []
        if html_files:
            # 最初のhtmlファイルを使用
            return redirect(html_files[0])
        else:
            # HTMLファイルがなければエラーページを表示
            return """
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>ビルドエラー</title>
                <style>
                    body { 
                        background: #000; 
                        color: #fff; 
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px 20px;
                    }
                    h1 { color: #ff9900; }
                    .error { color: #ff0000; margin: 20px 0; }
                    button {
                        background: #ff9900;
                        border: none;
                        padding: 10px 20px;
                        color: #000;
                        font-weight: bold;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <h1>ウェブビルドエラー</h1>
                <p class="error">PyxelゲームのWebビルドに失敗しました</p>
                <p>リビルドを試みています...</p>
                <script>
                    // 5秒後にリロード
                    setTimeout(() => {
                        location.reload();
                    }, 5000);
                </script>
            </body>
            </html>
            """
    
    # indexファイルへリダイレクト
    return redirect('index.html')

@app.route('/<path:path>')
def serve_file(path):
    """静的ファイルを提供"""
    return send_from_directory(WEB_DIR, path)

@app.route('/health')
def health():
    """ヘルスチェックエンドポイント"""
    return "OK - Pyxel Web Server Running", 200

@app.route('/rebuild')
def rebuild():
    """ウェブビルドを再実行"""
    global build_thread
    if build_thread and build_thread.is_alive():
        return "既にビルド中です", 202
    
    build_thread = threading.Thread(target=run_build)
    build_thread.daemon = True
    build_thread.start()
    
    return """
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>リビルド中</title>
        <style>
            body { 
                background: #000; 
                color: #fff; 
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px 20px;
            }
            h1 { color: #ff9900; }
            .loading {
                display: inline-block;
                width: 50px;
                height: 50px;
                border: 5px solid rgba(255,153,0,.3);
                border-radius: 50%;
                border-top-color: #ff9900;
                animation: spin 1s ease-in-out infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <h1>ウェブビルド実行中</h1>
        <div class="loading"></div>
        <p>しばらくお待ちください...</p>
        <script>
            // 10秒後にホームページにリダイレクト
            setTimeout(() => {
                window.location.href = "/";
            }, 10000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    # 初期ビルドを実行
    print("初期ウェブビルドを開始します...")
    build_thread = threading.Thread(target=run_build)
    build_thread.daemon = True
    build_thread.start()
    
    # ビルドが完了するまで少し待機
    time.sleep(2)
    
    # サーバー起動
    port = int(os.environ.get("PORT", 5000))
    print(f"Pyxel Web サーバーを起動します (ポート {port})...")
    app.run(host="0.0.0.0", port=port)