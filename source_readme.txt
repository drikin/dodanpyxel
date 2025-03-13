DodanPyxel - 縦スクロールシューティングゲーム (ソースコード)

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
