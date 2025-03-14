import os
import shutil
import json
import subprocess
import time

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

def create_html_template():
    """モバイル用のHTMLテンプレートを作成"""
    # モバイルウェブ版のベースディレクトリ
    mobile_web_dir = "mobile_web_version"
    ensure_directory(mobile_web_dir)
    
    # アセットディレクトリ
    assets_dir = os.path.join(mobile_web_dir, "assets")
    ensure_directory(assets_dir)
    
    # 静的ファイルディレクトリ
    static_dir = os.path.join(mobile_web_dir, "static")
    ensure_directory(static_dir)
    
    # 既にファイルが存在しているか確認
    index_html_path = os.path.join(mobile_web_dir, "index.html")
    iframe_html_path = os.path.join(mobile_web_dir, "iframe.html")
    
    # インデックスHTMLがない場合は作成
    if not os.path.exists(index_html_path):
        with open(index_html_path, "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DodanPyxel Mobile</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            background-color: #000;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            overflow: hidden;
        }
        
        #container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 20px;
            box-sizing: border-box;
        }
        
        h1 {
            color: #ff9900;
            margin-bottom: 20px;
            font-size: 24px;
        }
        
        p {
            margin-bottom: 30px;
            font-size: 16px;
            line-height: 1.5;
            max-width: 600px;
        }
        
        .button {
            display: inline-block;
            background-color: #ff9900;
            color: black;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            text-decoration: none;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            transition: transform 0.2s, background-color 0.2s;
        }
        
        .button:active {
            transform: scale(0.95);
            background-color: #e68a00;
        }
        
        #instructions {
            margin-top: 40px;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            max-width: 600px;
        }
        
        #instructions h2 {
            color: #ff9900;
            margin-top: 0;
            font-size: 20px;
        }
        
        #instructions ul {
            text-align: left;
            padding-left: 25px;
        }
        
        #instructions li {
            margin-bottom: 10px;
        }
        
        #footer {
            margin-top: 40px;
            font-size: 14px;
            color: #888;
        }
    </style>
</head>
<body>
    <div id="container">
        <h1>DodanPyxel Shooter</h1>
        <p>スマートフォン対応 縦型シューティングゲーム</p>
        
        <a href="/game" class="button">ゲームをプレイ</a>
        
        <div id="instructions">
            <h2>操作方法</h2>
            <ul>
                <li>画面の上半分をタップ: 弾を発射</li>
                <li>画面の下半分をドラッグ: 自機を移動</li>
                <li>画面を横向きにすると、より大きく表示されます</li>
                <li>画面をタップで開始・再開します</li>
            </ul>
        </div>
        
        <div id="footer">
            Powered by Pyxel &copy; 2025
        </div>
    </div>
</body>
</html>""")
    
    # iframeページがない場合は作成
    if not os.path.exists(iframe_html_path):
        create_iframe_html()

def create_css_file():
    """モバイル用のCSSファイルを作成"""
    static_dir = os.path.join("mobile_web_version", "static")
    ensure_directory(static_dir)
    
    css_path = os.path.join(static_dir, "mobile.css")
    if not os.path.exists(css_path):
        with open(css_path, "w", encoding="utf-8") as f:
            f.write("""body, html {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background-color: #000;
    touch-action: none;
    -webkit-user-select: none;
    user-select: none;
    font-family: Arial, sans-serif;
    color: white;
}

#game-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    align-items: center;
    justify-content: center;
}

#loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 20px;
    z-index: 100;
}

#game-frame {
    position: relative;
    width: 100%;
    max-width: 600px;
    height: 80vh;
    margin: 0 auto;
    background-color: #111;
    border: 2px solid #555;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
    overflow: hidden;
}

#vnc-container {
    width: 100%;
    height: 100%;
    overflow: hidden;
}

#game-iframe {
    width: 100%;
    height: 100%;
    border: none;
    transform-origin: center top;
}

#mobile-controls {
    width: 100%;
    max-width: 600px;
    background-color: #222;
    padding: 10px;
    border-radius: 0 0 10px 10px;
    text-align: center;
}

#mobile-message {
    font-size: 14px;
}

#mobile-message h2 {
    margin: 5px 0;
    color: #ff9900;
}

#mobile-message p {
    margin: 5px 0;
    color: #eee;
}

#game-info {
    margin-top: 20px;
    text-align: center;
    max-width: 600px;
}

#game-info h1 {
    color: #ff9900;
    margin: 10px 0;
    font-size: 24px;
}

#game-info p {
    color: #ccc;
    margin: 5px 0;
    font-size: 16px;
}

/* For landscape orientation */
@media (orientation: landscape) {
    #game-frame {
        height: 80vh;
    }
    
    #mobile-controls {
        padding: 5px;
    }
    
    #mobile-message {
        display: flex;
        justify-content: space-around;
    }
    
    #mobile-message h2 {
        font-size: 14px;
    }
    
    #mobile-message p {
        font-size: 12px;
        margin: 2px 10px;
    }
}

/* iPhone Safari specific fixes */
@supports (-webkit-touch-callout: none) {
    #game-frame {
        height: 65vh;
    }
}""")

def create_js_file():
    """モバイル用のJavaScriptファイルを作成"""
    static_dir = os.path.join("mobile_web_version", "static")
    ensure_directory(static_dir)
    
    js_path = os.path.join(static_dir, "mobile.js")
    if not os.path.exists(js_path):
        with open(js_path, "w", encoding="utf-8") as f:
            f.write("""document.addEventListener('DOMContentLoaded', function() {
    // iPhoneブラウザのアドレスバーの高さによる調整
    let gameFrame = document.getElementById('game-frame');
    let gameIframe = document.getElementById('game-iframe');
    
    // ゲームフレームのリサイズ処理
    function resizeGameFrame() {
        // iPhoneのSafariでは画面の高さが変わることがあるため、
        // ビューポートの高さに合わせてフレームをリサイズ
        let viewportHeight = window.innerHeight;
        let frameWidth = gameFrame.offsetWidth;
        
        // 縦横比を保持しながらリサイズ
        // Pyxelのデフォルト解像度は128x128
        // フレームの高さは画面の80%以下に
        let maxHeight = Math.min(viewportHeight * 0.8, frameWidth * (128/128));
        
        gameFrame.style.height = maxHeight + 'px';
        
        // iFrameのサイズとコンテンツをスケーリング
        if (window.innerWidth < window.innerHeight) {
            // 縦向き: 幅に合わせる
            let scale = frameWidth / 128;
            gameIframe.style.transform = 'scale(' + scale + ')';
        } else {
            // 横向き: 高さに合わせる
            let scale = maxHeight / 128;
            gameIframe.style.transform = 'scale(' + scale + ')';
        }
    }
    
    // 初期リサイズとロード状態の更新
    window.addEventListener('load', function() {
        resizeGameFrame();
        document.getElementById('loading').style.display = 'none';
    });
    
    // ウィンドウサイズ変更時のリサイズ
    window.addEventListener('resize', resizeGameFrame);
    
    // デバイスの回転時のリサイズ
    window.addEventListener('orientationchange', function() {
        setTimeout(resizeGameFrame, 100);
    });
    
    // iOSのSafariでアドレスバーが表示/非表示になる際のリサイズ
    window.addEventListener('scroll', function() {
        setTimeout(resizeGameFrame, 100);
    });
    
    // ゲームの起動
    fetch('/start_game')
        .then(response => response.json())
        .then(data => {
            console.log('Game process started:', data);
        })
        .catch(error => {
            console.error('Error starting game:', error);
        });
    
    // ページを離れる際にゲームプロセスを停止
    window.addEventListener('beforeunload', function() {
        fetch('/stop_game').catch(err => console.log('Error stopping game:', err));
    });
});""")

def create_iframe_html():
    """ゲームを表示するためのiframeページを作成"""
    iframe_path = os.path.join("mobile_web_version", "iframe.html")
    
    if not os.path.exists(iframe_path):
        with open(iframe_path, "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DodanPyxel Game Frame</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            background-color: #000;
            overflow: hidden;
            width: 100%;
            height: 100%;
            touch-action: none;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }
        
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }
        
        #touch-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 100;
            background: transparent;
        }
        
        #debug {
            position: absolute;
            top: 10px;
            left: 10px;
            color: yellow;
            font-family: monospace;
            font-size: 10px;
            pointer-events: none;
            z-index: 200;
            display: none;
        }
    </style>
</head>
<body>
    <!-- Pyxelのキャンバスがここに挿入されます -->
    <div id="game-canvas-container"></div>
    
    <!-- タッチ操作のためのオーバーレイ -->
    <div id="touch-overlay"></div>
    
    <!-- デバッグ情報表示 -->
    <div id="debug"></div>
    
    <script>
        // タッチ操作を有効化（モバイルデバイス用）
        let touchOverlay = document.getElementById('touch-overlay');
        let debugElement = document.getElementById('debug');
        
        // タッチ状態の追跡
        let touchActive = false;
        let touchX = 0;
        let touchY = 0;
        let startTouchX = 0;
        let startTouchY = 0;
        
        // ゲームへの入力を送信
        function sendTouchToGame(x, y, pressed, action) {
            // デバッグ情報を表示
            debugElement.textContent = `X: ${x}, Y: ${y}, Pressed: ${pressed}, Action: ${action}`;
            
            // ウィンドウの親フレームにメッセージを送信
            window.parent.postMessage({
                type: 'touch',
                x: x,
                y: y,
                pressed: pressed,
                action: action
            }, '*');
        }
        
        // タッチイベントハンドラ
        touchOverlay.addEventListener('touchstart', function(e) {
            e.preventDefault();
            
            // マルチタッチ対応
            for (let i = 0; i < e.changedTouches.length; i++) {
                let touch = e.changedTouches[i];
                touchActive = true;
                touchX = touch.clientX;
                touchY = touch.clientY;
                startTouchX = touchX;
                startTouchY = touchY;
                
                // 上半分と下半分でアクションを変える
                let action = (touchY < window.innerHeight / 2) ? 'shoot' : 'move';
                sendTouchToGame(touchX, touchY, true, action);
            }
        });
        
        touchOverlay.addEventListener('touchmove', function(e) {
            e.preventDefault();
            
            // マルチタッチ対応
            for (let i = 0; i < e.changedTouches.length; i++) {
                let touch = e.changedTouches[i];
                touchX = touch.clientX;
                touchY = touch.clientY;
                
                // 上半分と下半分でアクションを変える
                let action = (touchY < window.innerHeight / 2) ? 'shoot' : 'move';
                sendTouchToGame(touchX, touchY, true, action);
            }
        });
        
        touchOverlay.addEventListener('touchend', function(e) {
            e.preventDefault();
            
            // マルチタッチ対応
            for (let i = 0; i < e.changedTouches.length; i++) {
                let touch = e.changedTouches[i];
                touchActive = false;
                
                // 上半分と下半分でアクションを変える
                let action = (touchY < window.innerHeight / 2) ? 'shoot' : 'move';
                sendTouchToGame(touchX, touchY, false, action);
            }
        });
        
        // マウス操作のサポート (デスクトップテスト用)
        touchOverlay.addEventListener('mousedown', function(e) {
            e.preventDefault();
            touchActive = true;
            touchX = e.clientX;
            touchY = e.clientY;
            startTouchX = touchX;
            startTouchY = touchY;
            
            // 上半分と下半分でアクションを変える
            let action = (touchY < window.innerHeight / 2) ? 'shoot' : 'move';
            sendTouchToGame(touchX, touchY, true, action);
        });
        
        touchOverlay.addEventListener('mousemove', function(e) {
            e.preventDefault();
            if (touchActive) {
                touchX = e.clientX;
                touchY = e.clientY;
                
                // 上半分と下半分でアクションを変える
                let action = (touchY < window.innerHeight / 2) ? 'shoot' : 'move';
                sendTouchToGame(touchX, touchY, true, action);
            }
        });
        
        touchOverlay.addEventListener('mouseup', function(e) {
            e.preventDefault();
            touchActive = false;
            
            // 上半分と下半分でアクションを変える
            let action = (touchY < window.innerHeight / 2) ? 'shoot' : 'move';
            sendTouchToGame(touchX, touchY, false, action);
        });
    </script>
</body>
</html>""")

def take_game_screenshot():
    """ゲームのスクリーンショットを撮る（デモ用）"""
    static_dir = os.path.join("mobile_web_version", "static")
    ensure_directory(static_dir)
    
    screenshot_path = os.path.join(static_dir, "screenshot.png")
    
    # スクリーンショットがなければサンプル画像をコピー
    if not os.path.exists(screenshot_path):
        # まずはプロジェクト内の既存のスクリーンショットを探す
        potential_screenshots = [
            "screenshot.png",
            "public/screenshot.png",
            "static/screenshot.png"
        ]
        
        for path in potential_screenshots:
            if os.path.exists(path):
                shutil.copy(path, screenshot_path)
                print(f"スクリーンショットを{path}からコピーしました")
                return
        
        # 既存のスクリーンショットが見つからなければデモ用の画像を作成
        print("スクリーンショットが見つかりませんでした。デモ画像を作成します...")
        try:
            # サンプルの画像データを作成
            with open(screenshot_path, "wb") as f:
                # 空の画像ファイルを作成
                f.write(b"")
            print(f"デモスクリーンショットを作成しました: {screenshot_path}")
        except Exception as e:
            print(f"スクリーンショット作成エラー: {e}")

def build_mobile_web_version():
    """モバイル対応のウェブ版ゲームファイルを生成する"""
    print("モバイルウェブ版ゲームファイルの生成を開始...")
    
    # ベースディレクトリの作成
    mobile_web_dir = "mobile_web_version"
    ensure_directory(mobile_web_dir)
    
    # アセットディレクトリの作成
    assets_dir = os.path.join(mobile_web_dir, "assets")
    ensure_directory(assets_dir)
    
    # HTML、CSS、JSファイルの作成
    create_html_template()
    create_css_file()
    create_js_file()
    create_iframe_html()
    
    # スクリーンショットの準備
    take_game_screenshot()
    
    print("モバイルウェブ版ゲームファイルの生成が完了しました")
    
    return True

if __name__ == "__main__":
    build_mobile_web_version()