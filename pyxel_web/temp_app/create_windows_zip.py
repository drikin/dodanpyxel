import os
import zipfile
import io

# Windows用ZIPファイルを作成
def create_windows_zip():
    zip_path = 'web_static/downloads/dodanpyxel-windows.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # READMEファイルの内容
        readme_content = """
        # DodanPyxel - Windows版
        
        ## インストール方法
        1. ダウンロードしたZIPファイルを解凍します。
        2. 'dodanpyxel.bat' をダブルクリックして実行します。
        
        ## 注意事項
        初回起動時はWindows SmartScreenが表示される場合があります。
        「詳細情報」から「実行」を選択してください。
        
        ## コントロール
        - 矢印キー: 移動
        - 自動発射モード有効
        - ESC: ゲーム終了
        
        お楽しみください！
        """
        
        # ZIPファイルにREADMEを追加
        zf.writestr('README.txt', readme_content)
        
        # バッチファイルを作成
        batch_content = """@echo off
echo DodanPyxel をインストールしています...
python -m pip install pyxel
echo インストール完了！
python main.py
pause
"""
        zf.writestr('dodanpyxel.bat', batch_content)
        
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
    
    print(f"Windows ZIP file created at {zip_path}")

if __name__ == "__main__":
    # アップロードディレクトリが存在することを確認
    os.makedirs('web_static/downloads', exist_ok=True)
    
    create_windows_zip()