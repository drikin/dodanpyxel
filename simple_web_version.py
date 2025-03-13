import os
import sys
import shutil
import subprocess

def create_web_playable_version():
    """簡易版のWeb用ゲームプレイ環境を作成する"""
    print("Web用プレイ環境の作成を開始します...")
    
    # 公開用ディレクトリを作成
    os.makedirs("public/web", exist_ok=True)
    os.makedirs("public/web/js", exist_ok=True)
    os.makedirs("public/web/css", exist_ok=True)
    
    # Webページの作成
    with open("public/web/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DodanPyxel シューティングゲーム</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <h1>DodanPyxel シューティングゲーム - Web版</h1>
        
        <div class="game-container">
            <p>ブラウザでゲームを直接プレイすることはできませんが、以下のダウンロードオプションを使用してゲームをお楽しみください。</p>
            
            <div class="instruction-box">
                <h2>ゲーム操作方法</h2>
                <p>
                    矢印キー: 移動<br>
                    Zキー: 発射 (常時自動発射も有効)<br>
                    Xキー: ボム発射<br>
                    ESCキー: 終了
                </p>
            </div>
        </div>
        
        <div class="download-section">
            <h2>ダウンロードオプション</h2>
            <a href="/download/linux" class="download-btn">
                <span class="platform-icon">🐧</span>
                Linux版
            </a>
            <a href="/download/source" class="download-btn">
                <span class="platform-icon">📦</span>
                ソースコード
            </a>
        </div>
        
        <div class="screenshot-section">
            <h2>ゲームスクリーンショット</h2>
            <div class="screenshots">
                <img src="/screenshot" alt="ゲームスクリーンショット" class="game-screenshot">
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
        </div>
    </div>
</body>
</html>
""")
    
    # CSSファイルの作成
    with open("public/web/css/style.css", "w") as f:
        f.write("""body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #1a1a2e;
    color: #e6e6e6;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    text-align: center;
    color: #ff6b6b;
    margin-bottom: 30px;
}

h2 {
    color: #4ecdc4;
    border-bottom: 1px solid #4ecdc4;
    padding-bottom: 5px;
}

.game-container {
    background-color: #222244;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.instruction-box {
    background-color: #2a2a4a;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
}

.download-section {
    margin: 30px 0;
    text-align: center;
}

.download-btn {
    display: inline-block;
    background-color: #ff6b6b;
    color: white;
    padding: 12px 25px;
    margin: 10px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    transition: background-color 0.3s;
}

.download-btn:hover {
    background-color: #ff8e8e;
}

.platform-icon {
    font-size: 1.5em;
    margin-right: 8px;
}

.screenshot-section {
    margin: 30px 0;
}

.screenshots {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
}

.game-screenshot {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.footer {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #333355;
    color: #888;
    font-size: 0.9em;
}
""")
    
    print("Web用プレイ環境の作成が完了しました！")
    print("ファイルは public/web ディレクトリに保存されました")
    return True

if __name__ == "__main__":
    create_web_playable_version()