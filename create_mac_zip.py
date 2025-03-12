import os
import zipfile
import io

# macOS用ZIPファイルを作成
def create_mac_zip():
    zip_path = 'web_static/downloads/dodanpyxel-mac.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # READMEファイルの内容
        readme_content = """
        # DodanPyxel - macOS版
        
        ## インストール方法
        1. ダウンロードしたZIPファイルを解凍します。
        2. ターミナルで dodanpyxel.sh を実行します。
           $ chmod +x dodanpyxel.sh
           $ ./dodanpyxel.sh
        
        ## 注意事項
        初回起動時は「開発元を確認できないアプリ」と表示される場合があります。
        Control+クリックで「開く」を選択してください。
        
        ## コントロール
        - 矢印キー: 移動
        - 自動発射モード有効
        - ESC: ゲーム終了
        
        お楽しみください！
        """
        
        # ZIPファイルにREADMEを追加
        zf.writestr('README.txt', readme_content)
        
        # シェルスクリプトを作成
        shell_content = """#!/bin/bash
echo "DodanPyxel をインストールしています..."
python3 -m pip install pyxel
echo "インストール完了！"
python3 main.py
"""
        zf.writestr('dodanpyxel.sh', shell_content)
        
        # 現在のソースコードも含める
        for file_name in ['main.py', 'game.py', 'player.py', 'enemy.py', 'bullet.py', 'constants.py',
                         'background.py', 'explosion.py', 'boss.py', 'powerup.py']:
            try:
                if os.path.exists(file_name):
                    with open(file_name, 'r') as f:
                        zf.writestr(file_name, f.read())
            except Exception as e:
                print(f"Error adding {file_name} to zip: {e}")
        
        # アセットディレクトリ
        if os.path.exists('assets'):
            for file_name in ['assets/sounds.py', 'assets/sprites.py']:
                try:
                    if os.path.exists(file_name):
                        with open(file_name, 'r') as f:
                            zf.writestr(file_name, f.read())
                except Exception as e:
                    print(f"Error adding {file_name} to zip: {e}")
    
    print(f"macOS ZIP file created at {zip_path}")

if __name__ == "__main__":
    # アップロードディレクトリが存在することを確認
    os.makedirs('web_static/downloads', exist_ok=True)
    
    create_mac_zip()