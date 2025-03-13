import os
import shutil
import subprocess
import zipfile

def build_linux_binary():
    print("Linux用の実行可能ファイルを作成中...")
    
    # 公開用ディレクトリを作成
    os.makedirs('public/downloads', exist_ok=True)
    
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
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("PyInstallerの実行が完了しました。")
        
        # ZIPファイルを作成
        with zipfile.ZipFile('public/downloads/dodanpyxel-linux.zip', 'w') as zipf:
            # 生成された実行ファイルを追加
            zipf.write('dist/DodanPyxel', 'DodanPyxel')
            
            # READMEファイルを追加
            with open('linux_readme.txt', 'w') as readme:
                readme.write("""DodanPyxel - 縦スクロールシューティングゲーム (Linux版)

実行方法:
1. ZIPファイルを解凍します
2. 実行権限を付与します: chmod +x DodanPyxel
3. ターミナルから実行します: ./DodanPyxel

操作方法:
- 矢印キー: 移動
- Zキー: 発射 (常時自動発射も有効)
- Xキー: ボム発射
- ESCキー: 終了

注意事項:
- このバイナリはLinux向けにコンパイルされています
- Windows版やMac版が必要な場合は、ソースコードパッケージをダウンロードし、build_guide.txtの手順に従ってください

© 2025 DodanPyxel
""")
            zipf.write('linux_readme.txt', 'README.txt')
        
        print("Linux用バイナリパッケージの作成が完了しました。")
        print(f"ファイル: public/downloads/dodanpyxel-linux.zip")
        return True
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    build_linux_binary()