import os
import shutil

def ensure_directory(directory):
    """指定されたディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_directory(directory):
    """指定されたディレクトリを空にする"""
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

def create_html_with_custom_tags():
    """Pyxelカスタムタグを使用してHTMLファイルを作成"""
    # HTML出力先ディレクトリの作成とクリーン
    output_dir = "custom_web"
    ensure_directory(output_dir)
    clean_directory(output_dir)

    # カスタムタグを使用したHTMLの作成
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dodan Shooter - Pyxel Custom Tag版</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
            font-family: sans-serif;
        }
        
        /* iPhoneに最適化したスタイル */
        @media (max-width: 844px) {
            #canvas {
                width: 100%;
                height: 100%;
            }
        }
        
        h1 {
            margin-bottom: 20px;
            color: #ffcc00;
        }
        
        .loading {
            margin-top: 20px;
            font-style: italic;
            color: #aaa;
        }
        
        .controls {
            margin-top: 30px;
            text-align: center;
        }
    </style>
    <script>
        // ページロード完了時の処理
        window.onload = function() {
            document.getElementById('loadingMessage').textContent = 'Pyxelゲームを読み込み中...';
        };
    </script>
</head>
<body>
    <h1>Dodan Shooter</h1>
    <div id="loadingMessage" class="loading">準備中...</div>
    
    <!-- Pyxelカスタムタグ - 必要なPythonコードファイルをインポート -->
    <pyxel-run 
        root="./"
        name="main.py"
        packages="[
            'main.py',
            'game.py',
            'player.py',
            'enemy.py',
            'bullet.py',
            'powerup.py',
            'explosion.py',
            'background.py',
            'highscores.py',
            'boss.py',
            'assets/sprites.py',
            'assets/sounds.py',
            'constants.py',
            'high_scores.json'
        ]"
    >
    </pyxel-run>
    
    <div class="controls">
        <p>※ スマートフォンの場合は画面をタップして操作します</p>
    </div>
</body>
</html>
"""

    # カスタムタグHTMLをファイルに保存
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(html_content)
    
    print(f"カスタムタグHTMLを {output_dir}/index.html に作成しました")

def main():
    """メイン実行関数"""
    create_html_with_custom_tags()
    print("Pyxelカスタムタグを使用したHTMLの作成が完了しました")

if __name__ == "__main__":
    main()