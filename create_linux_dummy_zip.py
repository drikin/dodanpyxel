import os
import zipfile
import shutil

# 必要なディレクトリの作成
os.makedirs('temp_linux_package', exist_ok=True)
os.makedirs('public/downloads', exist_ok=True)

# 実行ファイルの作成
with open('temp_linux_package/dodanpyxel', 'w') as f:
    f.write('''#!/bin/bash
echo "DodanPyxel シューティングゲーム"
echo "このバイナリは実際のゲームを起動するものではなく、デモ用です。"
echo "実際のゲームを実行するには、ソースコードをダウンロードして実行してください。"
''')

# 実行権限を付与
os.chmod('temp_linux_package/dodanpyxel', 0o755)

# READMEファイルの作成
with open('temp_linux_package/README.txt', 'w') as f:
    f.write('''DodanPyxel - 縦スクロールシューティングゲーム (Linux版)

実行方法:
1. ZIPファイルを解凍します
2. 実行権限を付与します: chmod +x dodanpyxel
3. ターミナルから実行します: ./dodanpyxel

操作方法:
- 矢印キー: 移動
- Zキー: 発射 (常時自動発射も有効)
- Xキー: ボム発射
- ESCキー: 終了

注意事項:
- 実際にゲームをプレイするには、PyxelとPythonをインストールして、ソースコードパッケージを使用してください

© 2025 DodanPyxel''')

# ZIPファイルの作成
with zipfile.ZipFile('public/downloads/dodanpyxel-linux.zip', 'w') as zipf:
    zipf.write('temp_linux_package/dodanpyxel', 'dodanpyxel')
    zipf.write('temp_linux_package/README.txt', 'README.txt')

# 一時ディレクトリの削除
shutil.rmtree('temp_linux_package')

print("Linux用ダミーバイナリパッケージの作成が完了しました。")
print("ファイル: public/downloads/dodanpyxel-linux.zip")