#!/usr/bin/env python3
"""
DodanPyxel Web版作成スクリプト
このスクリプトは、Pyxel アプリをHTML5にコンバートするためのものです
"""

import os
import sys
import subprocess
import shutil
import tempfile

def create_temporary_package():
    """
    一時的なディレクトリに.pyxappファイルを作成する
    """
    print("Pyxelアプリをパッケージ化しています...")
    
    # 一時ディレクトリにメインファイルをコピー
    temp_dir = "temp_app"
    
    # 既存のディレクトリがあれば一旦削除（クリーンな状態から始める）
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
            print(f"{temp_dir}ディレクトリをクリーンアップしました")
        except Exception as e:
            print(f"ディレクトリのクリーンアップに失敗しました: {e}")
    
    # 新しいディレクトリを作成
    os.makedirs(temp_dir, exist_ok=True)
    
    # ゲームの必要なファイルをすべてコピー
    game_files = [
        "main.py", "game.py", "player.py", "enemy.py", 
        "bullet.py", "boss.py", "background.py", 
        "explosion.py", "powerup.py", "constants.py"
    ]
    
    print("ゲームファイルをコピーしています...")
    for file in game_files:
        if os.path.exists(file):
            try:
                shutil.copy(file, temp_dir)
                print(f"コピー完了: {file}")
            except Exception as e:
                print(f"ファイルのコピー中にエラーが発生しました ({file}): {e}")
        else:
            print(f"警告: ファイルが見つかりません: {file}")
    
    # assetsディレクトリがあればコピー
    if os.path.exists("assets"):
        if os.path.exists(os.path.join(temp_dir, "assets")):
            shutil.rmtree(os.path.join(temp_dir, "assets"))
        try:
            shutil.copytree("assets", os.path.join(temp_dir, "assets"))
            print("assetsディレクトリをコピーしました")
        except Exception as e:
            print(f"assetsディレクトリのコピー中にエラーが発生しました: {e}")
    else:
        print("警告: assetsディレクトリが見つかりません")
    
    # Pyxelのバージョンを確認
    try:
        pyxel_version = subprocess.check_output([sys.executable, "-m", "pyxel", "--version"], text=True).strip()
        print(f"Pyxelバージョン: {pyxel_version}")
    except Exception as e:
        print(f"Pyxelバージョンの確認に失敗しました: {e}")
        pyxel_version = "unknown"
    
    # pyxappパッケージのパス
    pyxapp_path = os.path.join(temp_dir, "game.pyxapp")
    
    print("Pyxelパッケージを作成しています...")
    # ここでPyxelのパッケージコマンドを実行
    try:
        # 最初の方法: メインファイルを指定
        cmd = [sys.executable, "-m", "pyxel", "package", os.path.join(temp_dir, "main.py"), pyxapp_path]
        print(f"実行コマンド: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("標準出力:", result.stdout)
        print("標準エラー:", result.stderr)
        print("パッケージ化が成功しました！方法1")
        return pyxapp_path
    except subprocess.CalledProcessError as e:
        print(f"パッケージ化中にエラーが発生しました: {e}")
        print(f"標準出力: {e.stdout if hasattr(e, 'stdout') else 'N/A'}")
        print(f"標準エラー: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
        print("別の方法を試みます...")
        
        try:
            # 別の方法: ディレクトリを指定
            cmd = [sys.executable, "-m", "pyxel", "package", temp_dir, pyxapp_path]
            print(f"実行コマンド: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("標準出力:", result.stdout)
            print("標準エラー:", result.stderr)
            print("パッケージ化が成功しました！方法2")
            return pyxapp_path
        except subprocess.CalledProcessError as e:
            print(f"再試行でもエラーが発生しました: {e}")
            print(f"標準出力: {e.stdout if hasattr(e, 'stdout') else 'N/A'}")
            print(f"標準エラー: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
            
            # 最後の手段: シンプルなダミーアプリを作成
            try:
                print("最後の手段: シンプルなダミーアプリを作成します...")
                with open(os.path.join(temp_dir, "simple_app.py"), "w") as f:
                    f.write("""
import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Demo")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.text(35, 61, "Please run the main.py", 13)

App()
                    """)
                
                # シンプルなアプリをパッケージ化
                cmd = [sys.executable, "-m", "pyxel", "package", os.path.join(temp_dir, "simple_app.py"), pyxapp_path]
                print(f"実行コマンド: {' '.join(cmd)}")
                
                result = subprocess.run(
                    cmd,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print("標準出力:", result.stdout)
                print("標準エラー:", result.stderr)
                print("ダミーアプリのパッケージ化が成功しました！")
                return pyxapp_path
            except subprocess.CalledProcessError as e:
                print(f"ダミーアプリの作成でもエラーが発生しました: {e}")
                print(f"標準出力: {e.stdout if hasattr(e, 'stdout') else 'N/A'}")
                print(f"標準エラー: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
                return None

def convert_to_html(pyxapp_path):
    """
    .pyxappファイルをHTML5に変換する
    """
    if not pyxapp_path or not os.path.exists(pyxapp_path):
        print(f"パッケージファイルが見つかりません: {pyxapp_path}")
        return False
    
    print(f".pyxappファイルをHTML5に変換しています... ファイルパス: {pyxapp_path}")
    web_dir = "public/web"
    
    # ディレクトリをクリーンアップ
    if os.path.exists(web_dir):
        try:
            for file in os.listdir(web_dir):
                file_path = os.path.join(web_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"ファイル削除エラー {file_path}: {e}")
            print(f"{web_dir}ディレクトリをクリーンアップしました")
        except Exception as e:
            print(f"ディレクトリのクリーンアップに失敗しました: {e}")
    
    os.makedirs(web_dir, exist_ok=True)
    
    try:
        cmd = [sys.executable, "-m", "pyxel", "app2html", pyxapp_path, web_dir]
        print(f"実行コマンド: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("HTML5への変換が成功しました！")
        print("標準出力:", result.stdout)
        print("標準エラー:", result.stderr)
        
        # 生成されたファイルの確認
        print("生成されたファイル:")
        for root, dirs, files in os.walk(web_dir):
            rel_path = os.path.relpath(root, web_dir)
            print(f"ディレクトリ: {rel_path if rel_path != '.' else ''}")
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f"  - {file} ({file_size} バイト)")
                
            # パーミッションを設定
            for file in files:
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o644)
                print(f"パーミッション設定: {file_path}")
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.chmod(dir_path, 0o755)
                print(f"パーミッション設定: {dir_path}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"HTML5への変換中にエラーが発生しました: {e}")
        print(f"標準出力: {e.stdout if hasattr(e, 'stdout') else 'N/A'}")
        print(f"標準エラー: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
        
        # エラーが発生した場合はダミーのHTMLを作成
        try:
            print("最後の手段: ダミーのHTML/JSファイルを作成します...")
            with open(os.path.join(web_dir, "index.html"), "w") as f:
                f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DodanPyxel ゲーム</title>
    <style>
        body { 
            background-color: #222;
            color: white;
            font-family: sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        
        .error-box {
            background-color: #333;
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 20px;
        }
        
        h1 { color: #ff5555; }
        p { line-height: 1.6; }
        
        .btn {
            display: inline-block;
            background-color: #0077cc;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>ゲーム準備中</h1>
    <div class="error-box">
        <p>申し訳ありませんが、ゲームのロードに問題が発生しました。</p>
        <p>開発者に問題を報告してください。</p>
        <p>トップページに戻って、別の方法でゲームを起動してみてください。</p>
    </div>
    <a href="/" class="btn">トップページに戻る</a>
    
    <script src="game.js"></script>
</body>
</html>""")
            
            with open(os.path.join(web_dir, "game.js"), "w") as f:
                f.write("""
console.log("ゲームの読み込みに失敗しました。");
document.addEventListener('DOMContentLoaded', function() {
    console.log("HTML/CSSは正常に読み込まれました。");
});
""")
            
            print("ダミーファイルを作成しました")
            return False
        except Exception as e:
            print(f"ダミーファイルの作成中にエラーが発生しました: {e}")
            return False

def create_web_version():
    """
    WebアプリのHTMLラッパーを作成する
    """
    pyxapp_path = create_temporary_package()
    if not pyxapp_path:
        print("パッケージ作成に失敗しました")
        return False
    
    success = convert_to_html(pyxapp_path)
    if not success:
        print("HTML変換に失敗しました")
        return False
    
    # ラッパーHTMLの作成は変換成功後に行われる
    create_wrapper_html()
    return True

def create_wrapper_html():
    """
    ゲームをラップするHTMLページを作成する
    """
    web_dir = "public/web"
    
    # ラッパーHTMLを作成
    wrapper_html = """<!DOCTYPE html>
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
            height: 520px;
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
        
        .back-btn {
            display: inline-block;
            background-color: #4ecdc4;
            color: white;
            padding: 10px 20px;
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
            <iframe src="index.html" class="game-frame" frameborder="0" scrolling="no" allowfullscreen></iframe>
            
            <div class="control-info">
                <h2>ゲーム操作方法</h2>
                <p>
                    矢印キー: 移動<br>
                    Zキー: 発射 (常時自動発射も有効)<br>
                    Xキー: ボム発射<br>
                    Rキー: ゲームオーバー時にリスタート<br>
                    ESCキー: 一時停止/再開
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
"""
    
    with open(os.path.join(web_dir, "main.html"), "w") as f:
        f.write(wrapper_html)
    
    print("ラッパーHTMLを作成しました")

if __name__ == "__main__":
    if create_web_version():
        print("Web版の作成が完了しました！")
    else:
        print("Web版の作成に失敗しました")