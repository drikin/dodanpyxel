import os
import sys
import subprocess
import shutil
import time
import glob

# Web出力ディレクトリ
WEB_DIR = "pyxel_web"
TEMP_DIR = "temp_app"
GAME_MODULE = "main.py"
APP_FILE = "game.pyxapp"

def ensure_directory(directory):
    """指定されたディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clean_directory(directory):
    """指定されたディレクトリを空にする"""
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.makedirs(directory)

def build_pyxapp():
    """PyxelゲームをPyxelアプリファイル(.pyxapp)にパッケージ化"""
    print("Pyxelゲームをパッケージ化しています...")
    
    # 必要なディレクトリを準備
    ensure_directory(TEMP_DIR)
    ensure_directory(os.path.join(TEMP_DIR, "assets"))
    
    # 主要ファイルをTEMP_DIRにコピー
    python_files = glob.glob("*.py")
    for py_file in python_files:
        shutil.copy(py_file, TEMP_DIR)
    
    # assetsディレクトリ内のファイルをコピー
    if os.path.exists("assets"):
        for asset_file in os.listdir("assets"):
            if asset_file.endswith(".py"):
                src = os.path.join("assets", asset_file)
                dst = os.path.join(TEMP_DIR, "assets", asset_file)
                shutil.copy(src, dst)
    
    # Pyxelのpackageコマンドでパッケージ化
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pyxel", "package", TEMP_DIR, GAME_MODULE],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("パッケージ化出力:", result.stdout)
        
        # 生成された.pyxappファイルを確認
        pyxapp_files = glob.glob("*.pyxapp")
        if pyxapp_files:
            print(f"パッケージ化成功: {pyxapp_files[0]}")
            return pyxapp_files[0]
        else:
            print("エラー: パッケージファイルが生成されませんでした")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"パッケージ化エラー: {e}")
        print(f"エラー出力: {e.stderr}")
        return None

def convert_to_html(pyxapp_file):
    """PyxelアプリファイルをHTMLに変換"""
    print(f"Pyxelアプリ {pyxapp_file} をHTMLに変換しています...")
    
    # 出力ディレクトリを準備
    clean_directory(WEB_DIR)
    
    try:
        # Pyxelのapp2html機能を使ってWebビルド
        result = subprocess.run(
            [sys.executable, "-m", "pyxel", "app2html", pyxapp_file, "-o", WEB_DIR],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("HTML変換出力:", result.stdout)
        
        # 生成されたHTMLファイルを確認
        html_files = glob.glob(os.path.join(WEB_DIR, "*.html"))
        if html_files:
            print(f"HTML変換成功: {len(html_files)}ファイル生成")
            for html in html_files:
                print(f" - {os.path.basename(html)}")
            return True
        else:
            print("エラー: HTMLファイルが生成されませんでした")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"HTML変換エラー: {e}")
        print(f"エラー出力: {e.stderr}")
        return False

def main():
    """メイン実行関数"""
    # まずPyxelアプリにパッケージ化
    pyxapp_file = build_pyxapp()
    if not pyxapp_file:
        print("パッケージ化に失敗しました")
        sys.exit(1)
    
    # 次にHTMLに変換
    if convert_to_html(pyxapp_file):
        print("ウェブビルドが完了しました")
        print(f"ファイルは {WEB_DIR} ディレクトリに保存されています")
    else:
        print("HTML変換に失敗しました")
        sys.exit(1)
        
if __name__ == "__main__":
    main()