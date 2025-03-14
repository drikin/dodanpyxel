import os
import shutil
import subprocess

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
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.makedirs(directory)

def create_html_with_custom_tags():
    """Pyxelカスタムタグを使用してHTMLファイルを作成"""
    web_dir = "custom_web"
    clean_directory(web_dir)
    
    # HTMLテンプレートを作成
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dodan Shooter - Pyxel Game</title>
    <script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js"></script>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #000;
            touch-action: none;
        }
        #game-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        pyxel-play {
            width: 100%;
            height: 100%;
            max-width: 100vw;
            max-height: 100vh;
        }
        #virtual-gamepad {
            position: fixed;
            bottom: 20px;
            left: 20px;
            width: 150px;
            height: 150px;
            background: rgba(100, 100, 100, 0.3);
            border-radius: 50%;
            touch-action: none;
            z-index: 1000;
        }
        #fire-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            background: rgba(255, 0, 0, 0.3);
            border-radius: 50%;
            touch-action: none;
            z-index: 1000;
        }
        .gamepad-dot {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 40px;
            height: 40px;
            margin-top: -20px;
            margin-left: -20px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
        }
        /* モバイル向けのスタイル */
        @media (max-width: 768px) {
            pyxel-play {
                width: 100vw;
                height: 100vh;
            }
        }
        /* ローディング表示 */
        #loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000;
            color: #fff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            font-family: sans-serif;
        }
        #loading-progress {
            width: 80%;
            max-width: 400px;
            height: 20px;
            background: #333;
            margin-top: 20px;
            border-radius: 10px;
            overflow: hidden;
        }
        #loading-bar {
            width: 0%;
            height: 100%;
            background: #0f0;
            transition: width 0.3s;
        }
    </style>
</head>
<body>
    <!-- ローディング表示 -->
    <div id="loading">
        <h2>ゲームをロード中...</h2>
        <div id="loading-progress">
            <div id="loading-bar"></div>
        </div>
        <p id="loading-status">初期化中...</p>
    </div>

    <div id="game-container">
        <pyxel-play
            name="main"
            root="."
            packages="pyxel"
            orientation="portrait"
            gamepad="enabled"
        ></pyxel-play>
    </div>
    
    <!-- モバイル用バーチャルゲームパッド -->
    <div id="virtual-gamepad">
        <div class="gamepad-dot"></div>
    </div>
    <div id="fire-button"></div>

    <script>
        // モバイルデバイス検出
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        
        // ローディング関連の要素
        const loadingElement = document.getElementById('loading');
        const loadingBar = document.getElementById('loading-bar');
        const loadingStatus = document.getElementById('loading-status');
        
        // Pyxel.jsのロード完了イベントを監視
        document.addEventListener('pyxel-play:load', function(e) {
            console.log('Pyxel play loaded:', e.detail);
            updateLoadingProgress(50, 'Pyxelをロードしました');
        });
        
        // Pyxel.jsのゲーム準備完了イベントを監視
        document.addEventListener('pyxel-play:ready', function(e) {
            console.log('Pyxel play ready:', e.detail);
            updateLoadingProgress(80, 'ゲームを準備中...');
            
            // 1秒後にローディング表示を消す
            setTimeout(function() {
                updateLoadingProgress(100, 'ゲーム起動完了！');
                setTimeout(function() {
                    loadingElement.style.display = 'none';
                }, 500);
            }, 1000);
        });
        
        // ローディングプログレスバーを更新
        function updateLoadingProgress(percent, message) {
            loadingBar.style.width = percent + '%';
            if (message) {
                loadingStatus.textContent = message;
            }
        }
        
        // 初期ローディング表示
        updateLoadingProgress(10, 'Pyxelをロード中...');
        
        // 30秒後にタイムアウト
        setTimeout(function() {
            if (loadingElement.style.display !== 'none') {
                loadingStatus.textContent = 'ロードに時間がかかっています。画面をリロードしてみてください。';
                loadingBar.style.background = '#f00';
            }
        }, 30000);
        
        if (isMobile) {
            // モバイルモードをPyxelに伝える
            window.pyxelMobileMode = true;
            
            // バーチャルゲームパッドの処理
            const gamepad = document.getElementById('virtual-gamepad');
            const gamepadDot = gamepad.querySelector('.gamepad-dot');
            const fireButton = document.getElementById('fire-button');
            
            let isPadActive = false;
            let isFireActive = false;
            let centerX = 0;
            let centerY = 0;
            let currentX = 0;
            let currentY = 0;
            let gamepadRect = gamepad.getBoundingClientRect();
            
            // 方向キー状態
            const keyStates = {
                up: false,
                down: false,
                left: false,
                right: false,
                fire: false
            };
            
            // ゲームパッド初期化
            function initGamepad() {
                gamepadRect = gamepad.getBoundingClientRect();
                centerX = gamepadRect.left + gamepadRect.width / 2;
                centerY = gamepadRect.top + gamepadRect.height / 2;
                gamepadDot.style.transform = 'translate(0, 0)';
            }
            
            // スクリーンサイズが変更されたときに再初期化
            window.addEventListener('resize', initGamepad);
            initGamepad();
            
            // タッチ操作処理
            document.addEventListener('touchstart', function(e) {
                for (let i = 0; i < e.changedTouches.length; i++) {
                    const touch = e.changedTouches[i];
                    const touchX = touch.clientX;
                    const touchY = touch.clientY;
                    
                    // ゲームパッドがタッチされたか
                    if (touchX >= gamepadRect.left && touchX <= gamepadRect.right &&
                        touchY >= gamepadRect.top && touchY <= gamepadRect.bottom) {
                        isPadActive = true;
                        currentX = touchX;
                        currentY = touchY;
                        updateGamepadPosition(touchX, touchY);
                    }
                    
                    // 発射ボタンがタッチされたか
                    const fireRect = fireButton.getBoundingClientRect();
                    if (touchX >= fireRect.left && touchX <= fireRect.right &&
                        touchY >= fireRect.top && touchY <= fireRect.bottom) {
                        isFireActive = true;
                        keyStates.fire = true;
                        fireButton.style.background = 'rgba(255, 0, 0, 0.6)';
                    }
                }
            }, { passive: true });
            
            document.addEventListener('touchmove', function(e) {
                for (let i = 0; i < e.changedTouches.length; i++) {
                    const touch = e.changedTouches[i];
                    if (isPadActive) {
                        updateGamepadPosition(touch.clientX, touch.clientY);
                    }
                }
            }, { passive: true });
            
            document.addEventListener('touchend', function(e) {
                for (let i = 0; i < e.changedTouches.length; i++) {
                    const touch = e.changedTouches[i];
                    const touchX = touch.clientX;
                    const touchY = touch.clientY;
                    
                    // ゲームパッドのタッチが終了したか
                    const fireRect = fireButton.getBoundingClientRect();
                    if (isPadActive && 
                        !(touchX >= gamepadRect.left && touchX <= gamepadRect.right &&
                          touchY >= gamepadRect.top && touchY <= gamepadRect.bottom)) {
                        isPadActive = false;
                        resetGamepadPosition();
                    }
                    
                    // 発射ボタンのタッチが終了したか
                    if (isFireActive && 
                        !(touchX >= fireRect.left && touchX <= fireRect.right &&
                          touchY >= fireRect.top && touchY <= fireRect.bottom)) {
                        isFireActive = false;
                        keyStates.fire = false;
                        fireButton.style.background = 'rgba(255, 0, 0, 0.3)';
                    }
                }
            }, { passive: true });
            
            function updateGamepadPosition(x, y) {
                const dx = x - centerX;
                const dy = y - centerY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const maxDistance = gamepadRect.width / 2 - 20;
                
                let moveX = dx;
                let moveY = dy;
                
                if (distance > maxDistance) {
                    const ratio = maxDistance / distance;
                    moveX = dx * ratio;
                    moveY = dy * ratio;
                }
                
                gamepadDot.style.transform = `translate(${moveX}px, ${moveY}px)`;
                
                // 方向キー状態を更新
                const threshold = maxDistance * 0.3;
                keyStates.up = dy < -threshold;
                keyStates.down = dy > threshold;
                keyStates.left = dx < -threshold;
                keyStates.right = dx > threshold;
            }
            
            function resetGamepadPosition() {
                gamepadDot.style.transform = 'translate(0, 0)';
                keyStates.up = false;
                keyStates.down = false;
                keyStates.left = false;
                keyStates.right = false;
            }
            
            // キー状態をPyxelに送信（10ミリ秒ごとに更新）
            function updateKeyStates() {
                if (window.dispatchEvent) {
                    if (keyStates.up) window.dispatchEvent(new KeyboardEvent('keydown', { keyCode: 38 }));
                    else window.dispatchEvent(new KeyboardEvent('keyup', { keyCode: 38 }));
                    
                    if (keyStates.down) window.dispatchEvent(new KeyboardEvent('keydown', { keyCode: 40 }));
                    else window.dispatchEvent(new KeyboardEvent('keyup', { keyCode: 40 }));
                    
                    if (keyStates.left) window.dispatchEvent(new KeyboardEvent('keydown', { keyCode: 37 }));
                    else window.dispatchEvent(new KeyboardEvent('keyup', { keyCode: 37 }));
                    
                    if (keyStates.right) window.dispatchEvent(new KeyboardEvent('keydown', { keyCode: 39 }));
                    else window.dispatchEvent(new KeyboardEvent('keyup', { keyCode: 39 }));
                    
                    if (keyStates.fire) window.dispatchEvent(new KeyboardEvent('keydown', { keyCode: 90 }));
                    else window.dispatchEvent(new KeyboardEvent('keyup', { keyCode: 90 }));
                }
                
                setTimeout(updateKeyStates, 10);
            }
            
            // キー状態更新ループ開始
            updateKeyStates();
            
            // 画面の向きが変わったときの処理
            window.addEventListener('orientationchange', function() {
                // 画面の向きが変わった時にゲームパッドを再初期化
                setTimeout(initGamepad, 300);
                
                // 全画面表示を維持
                if (document.documentElement.requestFullscreen) {
                    setTimeout(function() {
                        document.documentElement.requestFullscreen().catch(e => {
                            console.log('フルスクリーン化に失敗:', e);
                        });
                    }, 500);
                }
            });
            
            // 初期の全画面表示（iOSブラウザでは機能しないが、Androidでは動作）
            document.addEventListener('click', function fullscreenOnce() {
                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen().catch(e => {
                        console.log('フルスクリーン化に失敗:', e);
                    });
                }
                document.removeEventListener('click', fullscreenOnce);
            });
            
            updateLoadingProgress(20, 'モバイルコントロールを準備中...');
        } else {
            // PCの場合はバーチャルゲームパッドを非表示
            document.getElementById('virtual-gamepad').style.display = 'none';
            document.getElementById('fire-button').style.display = 'none';
            updateLoadingProgress(20, 'PCコントロールを準備中...');
        }
    </script>
</body>
</html>
"""

    # HTMLファイルを保存
    html_path = os.path.join(web_dir, "index.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"HTMLファイルを作成しました: {html_path}")
    return html_path

def main():
    """メイン実行関数"""
    print("Pyxelカスタムタグを使用したHTMLファイルを生成します...")
    html_path = create_html_with_custom_tags()
    print(f"HTMLファイルの生成が完了しました: {html_path}")
    print("Webサーバーを実行してHTMLファイルを提供します。")

if __name__ == "__main__":
    main()