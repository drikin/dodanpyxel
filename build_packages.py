import os
import sys
import subprocess
from create_windows_exe import create_windows_executable
from create_mac_app import create_mac_app
from create_source_zip import create_source_zip

def ensure_public_directory():
    """公開用ディレクトリが存在することを確認"""
    os.makedirs('public/downloads', exist_ok=True)

def build_all_packages():
    """すべてのプラットフォーム用パッケージをビルド"""
    print("===== DodanPyxel ゲームパッケージ生成開始 =====")
    
    ensure_public_directory()
    
    # Windowsバイナリの作成
    print("\n----- Windows用実行可能ファイルを生成 -----")
    create_windows_executable()
    
    # Macアプリの作成
    print("\n----- Mac用アプリケーションを生成 -----")
    create_mac_app()
    
    # ソースコードパッケージの作成
    print("\n----- ソースコードパッケージを生成 -----")
    create_source_zip()
    
    print("\n===== すべてのパッケージ生成完了 =====")
    print(f"パッケージの保存場所: {os.path.abspath('public/downloads')}")
    print("以下のファイルが生成されました:")
    print("- dodanpyxel-windows.zip (Windows用実行ファイル)")
    print("- dodanpyxel-mac.zip (Mac用アプリケーション)")
    print("- dodanpyxel-source.zip (ソースコード)")

if __name__ == "__main__":
    build_all_packages()