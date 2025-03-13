from flask import Flask, render_template, send_from_directory, send_file, url_for
import os
import sys
import base64
import io
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    # テンプレートを使用する
    return render_template('index.html')

@app.route('/download')
def download():
    # ダウンロードページの表示
    return render_template('download.html')

@app.route('/download/windows')
def download_windows():
    # 実際のバイナリーを送信する代わりに、テストダウンロードを提供
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
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
        for file_name in ['main.py', 'game.py', 'player.py', 'enemy.py', 'bullet.py', 'constants.py']:
            try:
                with open(file_name, 'r') as f:
                    zf.writestr(file_name, f.read())
            except:
                pass
    
    # ファイルポインタをリセット
    memory_file.seek(0)
    
    # ファイルを送信
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='dodanpyxel-windows.zip'
    )

@app.route('/download/mac')
def download_mac():
    # macOS向けダウンロード
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # READMEファイルの内容
        readme_content = """
        # DodanPyxel - macOS版
        
        ## インストール方法
        1. ダウンロードしたZIPファイルを解凍します。
        2. ターミナルで dodanpyxel.sh を実行します。
        
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
        for file_name in ['main.py', 'game.py', 'player.py', 'enemy.py', 'bullet.py', 'constants.py']:
            try:
                with open(file_name, 'r') as f:
                    zf.writestr(file_name, f.read())
            except:
                pass
    
    # ファイルポインタをリセット
    memory_file.seek(0)
    
    # ファイルを送信
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='dodanpyxel-mac.zip'
    )

@app.route('/download/source')
def download_source():
    # ソースコード一式のダウンロード
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
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
        
    # ファイルポインタを先頭に戻す
    memory_file.seek(0)
    
    # ZIPファイルをダウンロード
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='dodanpyxel-source.zip'
    )

if __name__ == '__main__':
    # Replitの環境変数をチェック
    if os.environ.get('REPLIT_DB_URL'):
        print("Running in Replit environment")
    
    # 明示的にポート5000を使用
    port = 5000
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)