import os
import sys
import subprocess
import shutil
import time
import glob

# Web出力ディレクトリ
WEB_DIR = "pyxel_web"
GAME_MODULE = "main.py"

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

def build_web_version():
    """PyxelゲームをWebアプリにコンパイル"""
    print("Pyxelゲームをウェブアプリにコンパイルしています...")
    
    # 出力ディレクトリを準備
    clean_directory(WEB_DIR)
    
    try:
        # Pyxelのapp2html機能を使ってWebビルド
        result = subprocess.run(
            [sys.executable, "-m", "pyxel", "app2html", GAME_MODULE, "-o", WEB_DIR],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("ビルド出力:", result.stdout)
        
        # 生成されたHTMLファイルを確認
        html_files = glob.glob(os.path.join(WEB_DIR, "*.html"))
        if html_files:
            print(f"コンパイル成功: {len(html_files)}ファイル生成")
            for html in html_files:
                print(f" - {os.path.basename(html)}")
            return True
        else:
            print("エラー: HTMLファイルが生成されませんでした")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"コンパイルエラー: {e}")
        print(f"エラー出力: {e.stderr}")
        return False

def main():
    """メイン実行関数"""
    # まずウェブビルドを実行
    if build_web_version():
        print("ウェブビルドが完了しました")
        print(f"ファイルは {WEB_DIR} ディレクトリに保存されています")
    else:
        print("ウェブビルドに失敗しました")
        sys.exit(1)
        
if __name__ == "__main__":
    main()