import os
import zipfile
import io

# ソースコード一式のZIPファイルを作成
def create_source_zip():
    zip_path = 'web_static/downloads/dodanpyxel-source.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # ゲームのソースファイルを追加
        source_files = [
            'main.py', 'game.py', 'player.py', 'enemy.py', 'bullet.py', 
            'background.py', 'explosion.py', 'constants.py', 'boss.py',
            'powerup.py', 'assets/sounds.py', 'assets/sprites.py'
        ]
        
        for filename in source_files:
            try:
                # ファイルが存在する場合追加
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        zf.writestr(filename, f.read())
            except Exception as e:
                print(f"Error adding {filename} to zip: {e}")
                
        # READMEファイルの追加
        readme_content = """# DodanPyxel - 縦スクロールシューティングゲーム

## 概要
DodanPyxelは、古典的な「弾幕系」シューティングゲームを再現した縦スクロールシューターです。

## インストール方法
1. Pythonをインストール (3.7以上):
   [Python公式サイト](https://www.python.org/downloads/)からダウンロード

2. Pyxelライブラリをインストール:
```
pip install pyxel
```

3. ゲームを実行:
```
python main.py
```

## 操作方法
- 矢印キー または WASD: プレイヤー移動
- 自動発射: 常に有効
- スペース: ゲーム開始/リスタート

タッチスクリーン:
- タッチ＆ドラッグ: 移動
- タップ: ゲーム開始/リスタート

## パワーアップアイテム
- 黄色(S): 3段階の拡散ショット
- 赤(P): パワーショット
- 青(+): スピードアップ
- 緑(#): シールド

## ボスシステム
- 全10種類のユニークなボス
- ボスサイクル: すべてのボスを倒すと、新しいサイクルが始まります
"""
        zf.writestr('README.md', readme_content)
        
        # requirements.txtの追加
        requirements_content = """pyxel>=1.4.3
"""
        zf.writestr('requirements.txt', requirements_content)
        
    print(f"Source ZIP file created at {zip_path}")

if __name__ == "__main__":
    # アップロードディレクトリが存在することを確認
    os.makedirs('web_static/downloads', exist_ok=True)
    
    create_source_zip()