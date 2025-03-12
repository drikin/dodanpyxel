import os
import zipfile

def create_source_zip():
    print("ソースコードパッケージを作成中...")
    
    # 含めるファイルのリスト
    source_files = [
        'main.py',
        'game.py',
        'player.py',
        'enemy.py',
        'bullet.py',
        'explosion.py',
        'background.py',
        'powerup.py',
        'boss.py',
        'constants.py'
    ]
    
    # assetsディレクトリのファイル
    assets_files = []
    if os.path.exists('assets'):
        for root, dirs, files in os.walk('assets'):
            for file in files:
                assets_files.append(os.path.join(root, file))
    
    # 公開用ディレクトリを作成
    os.makedirs('public/downloads', exist_ok=True)
    
    # ZIPファイルを作成
    with zipfile.ZipFile('public/downloads/dodanpyxel-source.zip', 'w') as zipf:
        # ソースファイルを追加
        for file in source_files:
            if os.path.exists(file):
                zipf.write(file)
        
        # アセットファイルを追加
        for file in assets_files:
            zipf.write(file)
        
        # ビルドガイドを追加
        if os.path.exists('build_guide.txt'):
            zipf.write('build_guide.txt')
        
        # READMEファイルを追加
        with open('source_readme.txt', 'w') as readme:
            readme.write("""DodanPyxel - 縦スクロールシューティングゲーム (ソースコード)

実行方法:
1. ZIPファイルを解凍します
2. Python 3.x と Pyxel ライブラリをインストールします:
   pip install pyxel
3. main.py を実行します:
   python main.py

バイナリのビルド方法:
詳細は同梱の build_guide.txt ファイルを参照してください。
PyInstallerを使用して、Windows用の.exeファイルやMac用の.appファイルを作成できます。

操作方法:
- 矢印キー: 移動
- Zキー: 発射 (常時自動発射も有効)
- Xキー: ボム発射
- ESCキー: 終了

ファイル構成:
- main.py: ゲームのエントリーポイント
- game.py: ゲームのメインロジック
- player.py: プレイヤーに関するクラスと機能
- enemy.py: 敵に関するクラスと機能
- bullet.py: 弾に関するクラスと機能
- explosion.py: 爆発エフェクトに関するクラス
- background.py: 背景に関するクラスと機能
- powerup.py: パワーアップアイテムに関するクラス
- boss.py: ボスキャラクターに関するクラス
- constants.py: ゲーム内で使用される定数
- assets/: ゲームのアセット（画像、音声など）
- build_guide.txt: バイナリのビルド方法を説明するガイド

© 2025 DodanPyxel
""")
        zipf.write('source_readme.txt', 'README.txt')
    
    print("ソースコードパッケージ作成完了！")
    print(f"ファイル: public/downloads/dodanpyxel-source.zip")

if __name__ == "__main__":
    create_source_zip()