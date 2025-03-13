import os
import subprocess
import shutil

def create_web_version():
    """Pyxelアプリをパッケージ化してHTML形式に変換"""
    print("Webバージョンの作成を開始します...")
    
    # 公開用ディレクトリを作成
    os.makedirs("public/web", exist_ok=True)
    
    # ソースファイルをコピー
    print("一時ディレクトリを作成中...")
    os.makedirs("temp_app", exist_ok=True)
    
    # 必要なファイルをコピー
    python_files = [
        "main.py", "game.py", "player.py", "enemy.py", "bullet.py", 
        "background.py", "explosion.py", "boss.py", "powerup.py", "constants.py"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy(file, f"temp_app/{file}")
    
    # assetsディレクトリがあればコピー
    if os.path.exists("assets"):
        shutil.copytree("assets", "temp_app/assets", dirs_exist_ok=True)
    
    try:
        # カレントディレクトリを一時的に変更して実行
        print("Pyxelアプリパッケージを作成中...")
        original_dir = os.getcwd()
        os.chdir("temp_app")
        subprocess.run(["pyxel", "package", ".", "main.py"], check=True)
        os.chdir(original_dir)
        
        # 作成されたpyxappファイルを見つける
        pyxapp_files = [f for f in os.listdir("temp_app") if f.endswith('.pyxapp')]
        if not pyxapp_files:
            print("エラー: .pyxappファイルが作成されませんでした")
            return False
        
        pyxapp_file = pyxapp_files[0]
        pyxapp_path = os.path.join("temp_app", pyxapp_file)
        print(f"作成されたパッケージ: {pyxapp_path}")
        
        # HTMLに変換
        print("パッケージをHTML形式に変換中...")
        # カレントディレクトリを一時的に変更して実行
        os.chdir("temp_app")
        subprocess.run(["pyxel", "app2html", pyxapp_file], check=True)
        os.chdir(original_dir)
        
        # 作成されたHTMLファイルを見つける
        html_dir = os.path.join("temp_app", pyxapp_file.replace('.pyxapp', '_html'))
        if not os.path.exists(html_dir):
            print(f"エラー: {html_dir}ディレクトリが作成されませんでした")
            return False
        
        # HTMLファイルを公開ディレクトリにコピー
        print("Webファイルを公開ディレクトリにコピー中...")
        for item in os.listdir(html_dir):
            src = os.path.join(html_dir, item)
            dst = os.path.join("public/web", item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        
        print("Webバージョンの作成が完了しました！")
        print(f"Webファイルは public/web ディレクトリに保存されました")
        
        # 後片付け
        shutil.rmtree("temp_app", ignore_errors=True)
        shutil.rmtree(html_dir, ignore_errors=True)
        if os.path.exists(pyxapp_file):
            os.remove(pyxapp_file)
        
        return True
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False
    finally:
        # 後片付け
        if os.path.exists("temp_app"):
            shutil.rmtree("temp_app", ignore_errors=True)

if __name__ == "__main__":
    create_web_version()