document.addEventListener('DOMContentLoaded', function() {
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
});