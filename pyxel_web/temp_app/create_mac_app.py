import os
import shutil
import subprocess
import sys
import zipfile

def create_mac_app():
    print("Mac用のアプリケーションを作成中...")
    
    # PyInstallerコマンドを構築
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=DodanPyxel',
        '--windowed',
        '--clean',
        '--add-data=assets:assets',
        'main.py'
    ]
    
    # コマンドを実行
    subprocess.run(pyinstaller_cmd, check=True)
    
    # 生成されたappフォルダをpublicフォルダにコピー
    os.makedirs('public/downloads', exist_ok=True)
    
    # ZIPファイルを作成
    with zipfile.ZipFile('public/downloads/dodanpyxel-mac.zip', 'w') as zipf:
        # distディレクトリ内のappフォルダ全体を追加
        app_dir = 'dist/DodanPyxel.app'
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path.replace('dist/', ''))
        
        # READMEファイルを追加
        with open('mac_readme.txt', 'w') as readme:
            readme.write("""DodanPyxel - 縦スクロールシューティングゲーム (Mac版)

ゲームの起動方法:
1. ZIPファイルを解凍します
2. DodanPyxel.appをダブルクリックして起動します
※初回起動時にセキュリティ警告が表示される場合は、システム環境設定→セキュリティとプライバシーから許可してください

操作方法:
- 矢印キー: 移動
- Zキー: 発射 (常時自動発射も有効)
- Xキー: ボム発射
- ESCキー: 終了

© 2025 DodanPyxel
""")
        zipf.write('mac_readme.txt', 'README.txt')
    
    print("Mac用のアプリケーション作成完了！")
    print(f"ファイル: public/downloads/dodanpyxel-mac.zip")

if __name__ == "__main__":
    create_mac_app()