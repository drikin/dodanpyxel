import os
import sys
import pyxel

# Web版の出力先ディレクトリ
OUTPUT_DIR = "web_version"

def ensure_directory(directory):
    """指定されたディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def build_web_version():
    """ゲームのウェブ版を生成する（サーバーは起動しない）"""
    # 出力先ディレクトリの準備
    ensure_directory(OUTPUT_DIR)
    
    # Pyxelアプリケーションをウェブ形式に変換
    print("Building web version...")
    
    try:
        # App2htmlが利用可能ならそれを使う (Pyxel 2.0.0+)
        if hasattr(pyxel, 'app2html'):
            pyxel.app2html("main.py", html_file=f"{OUTPUT_DIR}/index.html", server=False)
            print("Successfully converted game to web version using pyxel.app2html")
            return True
        else:
            print("Error: This version of Pyxel does not support app2html. Please use Pyxel 2.0.0 or higher.")
            return False
    except Exception as e:
        print(f"Error building web version: {e}")
        return False

if __name__ == "__main__":
    # Webバージョンのビルド
    if build_web_version():
        print(f"Web version built successfully in {OUTPUT_DIR}/ directory")
        print("Now you can start the web server with: python simple_flask_server.py")
    else:
        print("Failed to build web version.")
        sys.exit(1)