import os
import shutil
import subprocess
import sys
import zipfile

def create_windows_executable():
    print("Windows用の実行可能ファイルを作成中...")
    
    # アイコンファイルの存在を確認
    icon_path = 'generated-icon.png'
    
    # PyInstallerコマンドを構築
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=DodanPyxel',
        '--onefile',
        '--windowed',
        '--clean',
        '--add-data=assets:assets',
        'main.py'
    ]
    
    # コマンドを実行
    subprocess.run(pyinstaller_cmd, check=True)
    
    # 生成されたexeファイルをpublicフォルダにコピー
    os.makedirs('public/downloads', exist_ok=True)
    
    # ZIPファイルを作成
    with zipfile.ZipFile('public/downloads/dodanpyxel-windows.zip', 'w') as zipf:
        zipf.write('dist/DodanPyxel.exe', 'DodanPyxel.exe')
        # READMEファイルを追加
        with open('windows_readme.txt', 'w') as readme:
            readme.write("""DodanPyxel - 縦スクロールシューティングゲーム (Windows版)

ゲームの起動方法:
1. ZIPファイルを解凍します
2. DodanPyxel.exeをダブルクリックして起動します

操作方法:
- 矢印キー: 移動
- Zキー: 発射 (常時自動発射も有効)
- Xキー: ボム発射
- ESCキー: 終了

© 2025 DodanPyxel
""")
        zipf.write('windows_readme.txt', 'README.txt')
    
    print("Windows用の実行可能ファイル作成完了！")
    print(f"ファイル: public/downloads/dodanpyxel-windows.zip")

if __name__ == "__main__":
    create_windows_executable()