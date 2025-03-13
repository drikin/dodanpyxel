import os
import shutil
import subprocess
import sys

def install_pyxel_web():
    """Pyxel Webをインストールし、Webビルドを作成する"""
    print("Pyxel Webのセットアップを開始します...")
    
    # Pyxel Webが既にインストールされているか確認
    try:
        subprocess.run(["pyxel", "watch", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Pyxel Webは既にインストールされています。")
    except:
        print("Pyxel Webをインストールしています...")
        try:
            # Pyxel Webのインストール
            subprocess.run([sys.executable, "-m", "pip", "install", "pyxel[web]"], check=True)
            print("Pyxel Webのインストールが完了しました。")
        except Exception as e:
            print(f"Pyxel Webのインストールに失敗しました: {e}")
            return False
    
    # Web用のビルドディレクトリを作成
    os.makedirs("public/web", exist_ok=True)
    
    # Pyxel Webコンバートを実行
    try:
        print("ゲームをWeb形式に変換しています...")
        subprocess.run(["pyxel", "package", ".", "-o", "public/web"], check=True)
        print("Web形式への変換が完了しました。")
    except Exception as e:
        print(f"Web形式への変換に失敗しました: {e}")
        return False
    
    print("Pyxel Webのセットアップが完了しました。")
    return True

if __name__ == "__main__":
    install_pyxel_web()