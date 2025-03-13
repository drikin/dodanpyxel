import os
import sys
import subprocess
import shutil

def setup_web_game():
    """PyxelのWebバージョンを設定し、ブラウザで直接プレイできるようにする"""
    
    print("Web用ゲーム環境の構築を開始します...")
    
    # 公開用ディレクトリを作成
    os.makedirs("public/web", exist_ok=True)
    
    # PyxelアプリをWebエクスポート用の一時ディレクトリに作成
    os.makedirs("temp_app", exist_ok=True)
    
    try:
        # すべての必要なコードファイルを一時ディレクトリにコピー
        print("ゲームファイルを準備しています...")
        game_files = [
            "main.py", "game.py", "player.py", "enemy.py", 
            "bullet.py", "boss.py", "background.py", 
            "explosion.py", "powerup.py", "constants.py"
        ]
        
        # アセットディレクトリも存在するならコピー
        if os.path.exists("assets"):
            if not os.path.exists("temp_app/assets"):
                shutil.copytree("assets", "temp_app/assets")
        
        for file in game_files:
            if os.path.exists(file):
                shutil.copy(file, "temp_app/")
        
        # pyxapp形式でエクスポートを試みる
        print("Pyxelアプリをパッケージ化しています...")
        try:
            # まず直接メインPythonファイルを指定
            subprocess.run([sys.executable, "-m", "pyxel", "package", "temp_app/main.py", "temp_app/temp_app.pyxapp"], check=True)
        except:
            # 失敗した場合はディレクトリを指定する方法を試す
            try:
                subprocess.run([sys.executable, "-m", "pyxel", "package", "temp_app", "temp_app/temp_app.pyxapp"], check=True)
            except:
                print("pyxapp形式でのパッケージ化に失敗しました。代替方法を使用します。")
                # Web版変換に失敗しても続行する
                return False
        
        # Pyxel Web版に変換
        print("PyxelアプリをWeb形式に変換しています...")
        try:
            subprocess.run([sys.executable, "-m", "pyxel", "app2html", "temp_app/temp_app.pyxapp", "public/web"], check=True)
        except:
            print("Web形式への変換に失敗しました。")
            return False
        
        # HTMLファイルのリダイレクト設定
        with open("public/web/index.html", "r") as f:
            html_content = f.read()
        
        # メインページの作成
        create_main_page()
        
        print("Web版ゲームの構築が完了しました！")
        print("ブラウザでダイレクトにアクセスして、ゲームをプレイしてください。")
        return True
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラーが発生した場合は代替ページを作成
        create_fallback_page()
        return False

def create_main_page():
    """メインのWeb用ゲームページを作成"""
    with open("public/web/main.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DodanPyxel シューティングゲーム</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a2e;
            color: #e6e6e6;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            width: 100%;
            padding: 20px;
            box-sizing: border-box;
        }
        
        h1 {
            text-align: center;
            color: #ff6b6b;
            margin-bottom: 30px;
        }
        
        .game-container {
            background-color: #222244;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .game-frame {
            width: 100%;
            max-width: 640px;
            height: 480px;
            border: none;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        .control-info {
            background-color: #2a2a4a;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            width: 100%;
            max-width: 640px;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #333355;
            color: #888;
            font-size: 0.9em;
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DodanPyxel シューティングゲーム</h1>
        
        <div class="game-container">
            <iframe src="index.html" class="game-frame" allowfullscreen></iframe>
            
            <div class="control-info">
                <h2>ゲーム操作方法</h2>
                <p>
                    矢印キー: 移動<br>
                    Zキー: 発射 (常時自動発射も有効)<br>
                    Xキー: ボム発射<br>
                    ESCキー: 終了
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
        </div>
    </div>
</body>
</html>
""")

def create_fallback_page():
    """Web版ゲームの構築に失敗した場合の代替ページを作成"""
    os.makedirs("public/web", exist_ok=True)
    
    with open("public/web/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DodanPyxel シューティングゲーム</title>
    <style>
        body {
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
        
        .game-container {
            background-color: #222244;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .error-message {
            background-color: #3a3a5a;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            text-align: left;
            color: #ffaaaa;
        }
        
        .instruction-box {
            background-color: #2a2a4a;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .screenshot {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
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
        
        .back-btn {
            display: inline-block;
            background-color: #4ecdc4;
            color: white;
            padding: 12px 25px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 20px;
            transition: all 0.3s;
        }
        
        .back-btn:hover {
            background-color: #44b8b1;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DodanPyxel シューティングゲーム</h1>
        
        <div class="game-container">
            <h2>Web版の準備中</h2>
            
            <div class="error-message">
                <p>申し訳ありませんが、Web版ゲームの構築中にエラーが発生しました。現在、開発チームが解決に取り組んでいます。</p>
                <p>ゲームのスクリーンショットをご覧ください：</p>
            </div>
            
            <img src="/screenshot" alt="ゲームスクリーンショット" class="screenshot">
            
            <div class="instruction-box">
                <h2>ゲーム操作方法</h2>
                <p>
                    矢印キー: 移動<br>
                    Zキー: 発射 (常時自動発射も有効)<br>
                    Xキー: ボム発射<br>
                    ESCキー: 終了
                </p>
            </div>
            
            <a href="/" class="back-btn">トップページに戻る</a>
        </div>
        
        <div class="footer">
            <p>© 2025 DodanPyxel - Pyxelで作られた縦スクロールシューティングゲーム</p>
        </div>
    </div>
</body>
</html>
""")

if __name__ == "__main__":
    setup_web_game()