// DodanPyxel用の簡易Webゲーム実装
// このファイルはPyxelゲームの基本的な機能をHTMLキャンバス上で再現します

// ゲーム設定
const SCREEN_WIDTH = 256;
const SCREEN_HEIGHT = 256;
const PLAYER_SPEED = 3;
const BULLET_SPEED = 5;
const ENEMY_SPEED = 2;

// ゲーム状態
let gameState = {
  player: {
    x: SCREEN_WIDTH / 2,
    y: SCREEN_HEIGHT - 30,
    width: 16,
    height: 16,
    speed: PLAYER_SPEED,
    bullets: [],
    fireRate: 10,
    fireCounter: 0,
    score: 0,
    lives: 3
  },
  enemies: [],
  background: {
    stars: []
  },
  gameOver: false,
  isPaused: false
};

// キャンバスとコンテキスト
let canvas, ctx;

// 入力状態
const keys = {
  ArrowLeft: false,
  ArrowRight: false,
  ArrowUp: false,
  ArrowDown: false,
  z: false,
  x: false
};

// ゲーム初期化
function init() {
  canvas = document.getElementById('gameCanvas');
  ctx = canvas.getContext('2d');
  
  canvas.width = SCREEN_WIDTH;
  canvas.height = SCREEN_HEIGHT;
  
  // 星の初期化（背景）
  for (let i = 0; i < 50; i++) {
    gameState.background.stars.push({
      x: Math.random() * SCREEN_WIDTH,
      y: Math.random() * SCREEN_HEIGHT,
      size: Math.random() * 2 + 1,
      speed: Math.random() * 2 + 1
    });
  }
  
  // 敵の作成
  spawnEnemies();
  
  // イベントリスナー
  window.addEventListener('keydown', handleKeyDown);
  window.addEventListener('keyup', handleKeyUp);
  
  // ゲームループ開始
  requestAnimationFrame(gameLoop);
}

// キー入力処理
function handleKeyDown(e) {
  if (keys.hasOwnProperty(e.key)) {
    keys[e.key] = true;
    if (e.key === 'x') {
      useBomb();
    }
    e.preventDefault();
  }
}

function handleKeyUp(e) {
  if (keys.hasOwnProperty(e.key)) {
    keys[e.key] = false;
    e.preventDefault();
  }
}

// ボム使用
function useBomb() {
  // すべての敵を破壊
  gameState.enemies.forEach(enemy => {
    gameState.player.score += 100;
    createExplosion(enemy.x, enemy.y);
  });
  gameState.enemies = [];
  
  // 少し待ってから新しい敵を生成
  setTimeout(spawnEnemies, 1000);
}

// 敵の生成
function spawnEnemies() {
  for (let i = 0; i < 5; i++) {
    gameState.enemies.push({
      x: Math.random() * (SCREEN_WIDTH - 20) + 10,
      y: Math.random() * 100 + 10,
      width: 16,
      height: 16,
      speed: ENEMY_SPEED,
      health: 2,
      fireRate: 100,
      fireCounter: Math.floor(Math.random() * 100)
    });
  }
}

// 弾の発射
function fireBullet(isPlayer, x, y) {
  const bullet = {
    x: x,
    y: y,
    width: isPlayer ? 4 : 6,
    height: isPlayer ? 8 : 8,
    speed: isPlayer ? BULLET_SPEED : BULLET_SPEED / 2,
    isPlayer: isPlayer
  };
  
  if (isPlayer) {
    gameState.player.bullets.push(bullet);
  } else {
    gameState.enemies.forEach(enemy => {
      if (Math.random() < 0.1) {
        enemy.bullets = enemy.bullets || [];
        enemy.bullets.push({
          x: enemy.x + enemy.width / 2 - 2,
          y: enemy.y + enemy.height,
          width: 4,
          height: 8,
          speed: BULLET_SPEED / 2
        });
      }
    });
  }
}

// 爆発エフェクト
function createExplosion(x, y) {
  // 簡易的な爆発の視覚効果として円を描画
  ctx.fillStyle = '#FFA500';
  ctx.beginPath();
  ctx.arc(x, y, 20, 0, Math.PI * 2);
  ctx.fill();
  
  ctx.fillStyle = '#FF4500';
  ctx.beginPath();
  ctx.arc(x, y, 15, 0, Math.PI * 2);
  ctx.fill();
  
  ctx.fillStyle = '#FFFF00';
  ctx.beginPath();
  ctx.arc(x, y, 10, 0, Math.PI * 2);
  ctx.fill();
}

// プレイヤーの更新
function updatePlayer() {
  // 移動
  if (keys.ArrowLeft) gameState.player.x -= gameState.player.speed;
  if (keys.ArrowRight) gameState.player.x += gameState.player.speed;
  if (keys.ArrowUp) gameState.player.y -= gameState.player.speed;
  if (keys.ArrowDown) gameState.player.y += gameState.player.speed;
  
  // 画面境界チェック
  gameState.player.x = Math.max(0, Math.min(SCREEN_WIDTH - gameState.player.width, gameState.player.x));
  gameState.player.y = Math.max(0, Math.min(SCREEN_HEIGHT - gameState.player.height, gameState.player.y));
  
  // 自動発射
  gameState.player.fireCounter++;
  if (gameState.player.fireCounter >= gameState.player.fireRate) {
    fireBullet(true, gameState.player.x + gameState.player.width / 2 - 2, gameState.player.y - 8);
    gameState.player.fireCounter = 0;
  }
  
  // プレイヤーの弾の更新
  for (let i = gameState.player.bullets.length - 1; i >= 0; i--) {
    const bullet = gameState.player.bullets[i];
    bullet.y -= bullet.speed;
    
    // 画面外の弾を削除
    if (bullet.y < 0) {
      gameState.player.bullets.splice(i, 1);
    }
  }
}

// 敵の更新
function updateEnemies() {
  // 敵がいない場合は新しく生成
  if (gameState.enemies.length === 0) {
    spawnEnemies();
  }
  
  // 敵の更新
  for (let i = gameState.enemies.length - 1; i >= 0; i--) {
    const enemy = gameState.enemies[i];
    
    // 横移動
    enemy.x += Math.sin(Date.now() / 1000 + i) * 1.5;
    
    // 弾の発射
    enemy.fireCounter++;
    if (enemy.fireCounter >= enemy.fireRate) {
      if (!enemy.bullets) enemy.bullets = [];
      enemy.bullets.push({
        x: enemy.x + enemy.width / 2 - 2,
        y: enemy.y + enemy.height,
        width: 4,
        height: 8,
        speed: BULLET_SPEED / 2
      });
      enemy.fireCounter = 0;
    }
    
    // 敵の弾の更新
    if (enemy.bullets) {
      for (let j = enemy.bullets.length - 1; j >= 0; j--) {
        const bullet = enemy.bullets[j];
        bullet.y += bullet.speed;
        
        // 画面外の弾を削除
        if (bullet.y > SCREEN_HEIGHT) {
          enemy.bullets.splice(j, 1);
          continue;
        }
        
        // プレイヤーとの当たり判定
        if (detectCollision(bullet, gameState.player)) {
          enemy.bullets.splice(j, 1);
          gameState.player.lives--;
          createExplosion(gameState.player.x + gameState.player.width / 2, gameState.player.y + gameState.player.height / 2);
          
          if (gameState.player.lives <= 0) {
            gameState.gameOver = true;
          }
        }
      }
    }
  }
}

// 背景の更新
function updateBackground() {
  // 星の移動
  gameState.background.stars.forEach(star => {
    star.y += star.speed;
    if (star.y > SCREEN_HEIGHT) {
      star.y = 0;
      star.x = Math.random() * SCREEN_WIDTH;
    }
  });
}

// 当たり判定
function detectCollision(obj1, obj2) {
  return obj1.x < obj2.x + obj2.width &&
         obj1.x + obj1.width > obj2.x &&
         obj1.y < obj2.y + obj2.height &&
         obj1.y + obj1.height > obj2.y;
}

// 衝突判定
function checkCollisions() {
  // プレイヤーの弾と敵の当たり判定
  for (let i = gameState.player.bullets.length - 1; i >= 0; i--) {
    const bullet = gameState.player.bullets[i];
    
    for (let j = gameState.enemies.length - 1; j >= 0; j--) {
      const enemy = gameState.enemies[j];
      
      if (detectCollision(bullet, enemy)) {
        // 弾を削除
        gameState.player.bullets.splice(i, 1);
        
        // 敵のダメージ処理
        enemy.health--;
        
        if (enemy.health <= 0) {
          // 敵を倒した
          gameState.enemies.splice(j, 1);
          gameState.player.score += 100;
          createExplosion(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2);
        }
        
        break;
      }
    }
  }
}

// ゲーム描画
function drawGame() {
  // 背景クリア
  ctx.fillStyle = '#111133';
  ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  
  // 星を描画
  ctx.fillStyle = '#FFFFFF';
  gameState.background.stars.forEach(star => {
    ctx.fillRect(star.x, star.y, star.size, star.size);
  });
  
  // プレイヤーを描画
  ctx.fillStyle = '#00FFFF';
  ctx.fillRect(gameState.player.x, gameState.player.y, gameState.player.width, gameState.player.height);
  
  // プレイヤーの弾を描画
  ctx.fillStyle = '#FFFFFF';
  gameState.player.bullets.forEach(bullet => {
    ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
  });
  
  // 敵を描画
  ctx.fillStyle = '#FF6347';
  gameState.enemies.forEach(enemy => {
    ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    
    // 敵の弾を描画
    if (enemy.bullets) {
      ctx.fillStyle = '#FFFF00';
      enemy.bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
      });
    }
  });
  
  // UIを描画
  drawUI();
  
  // ゲームオーバー画面
  if (gameState.gameOver) {
    drawGameOver();
  }
}

// UI描画
function drawUI() {
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '12px Arial';
  ctx.fillText(`Score: ${gameState.player.score}`, 10, 20);
  ctx.fillText(`Lives: ${gameState.player.lives}`, SCREEN_WIDTH - 70, 20);
}

// ゲームオーバー表示
function drawGameOver() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '24px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('GAME OVER', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10);
  
  ctx.font = '16px Arial';
  ctx.fillText(`Score: ${gameState.player.score}`, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20);
  ctx.fillText('Press R to restart', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50);
  
  // リスタート処理
  if (keys.r) {
    resetGame();
  }
}

// ゲームリセット
function resetGame() {
  gameState = {
    player: {
      x: SCREEN_WIDTH / 2,
      y: SCREEN_HEIGHT - 30,
      width: 16,
      height: 16,
      speed: PLAYER_SPEED,
      bullets: [],
      fireRate: 10,
      fireCounter: 0,
      score: 0,
      lives: 3
    },
    enemies: [],
    background: {
      stars: []
    },
    gameOver: false,
    isPaused: false
  };
  
  // 星の初期化（背景）
  for (let i = 0; i < 50; i++) {
    gameState.background.stars.push({
      x: Math.random() * SCREEN_WIDTH,
      y: Math.random() * SCREEN_HEIGHT,
      size: Math.random() * 2 + 1,
      speed: Math.random() * 2 + 1
    });
  }
  
  spawnEnemies();
}

// メインゲームループ
function gameLoop() {
  if (!gameState.gameOver && !gameState.isPaused) {
    updatePlayer();
    updateEnemies();
    updateBackground();
    checkCollisions();
  }
  
  drawGame();
  
  requestAnimationFrame(gameLoop);
}

// キーボード入力のリセット関数を追加
function resetKeys() {
  Object.keys(keys).forEach(key => {
    keys[key] = false;
  });
}

// Rキー検出のためのイベントリスナーを追加
window.addEventListener('keydown', function(e) {
  if (e.key === 'r' && gameState.gameOver) {
    resetGame();
  }
  // ESCキーでゲームを一時停止/再開
  if (e.key === 'Escape') {
    gameState.isPaused = !gameState.isPaused;
  }
});

// タッチスクリーンサポート
function setupTouchControls() {
  const touchZones = {
    left: { x: 0, y: SCREEN_HEIGHT / 2, width: SCREEN_WIDTH / 3, height: SCREEN_HEIGHT / 2 },
    right: { x: SCREEN_WIDTH * 2/3, y: SCREEN_HEIGHT / 2, width: SCREEN_WIDTH / 3, height: SCREEN_HEIGHT / 2 },
    up: { x: SCREEN_WIDTH / 3, y: 0, width: SCREEN_WIDTH / 3, height: SCREEN_HEIGHT / 2 },
    down: { x: SCREEN_WIDTH / 3, y: SCREEN_HEIGHT / 2, width: SCREEN_WIDTH / 3, height: SCREEN_HEIGHT / 2 },
    bomb: { x: 0, y: 0, width: SCREEN_WIDTH, height: SCREEN_HEIGHT }
  };
  
  function handleTouch(e) {
    e.preventDefault();
    
    // リセットすべてのタッチ入力
    resetKeys();
    
    // 各タッチポイントを処理
    for (let i = 0; i < e.touches.length; i++) {
      const touch = e.touches[i];
      const touchX = touch.clientX - canvas.getBoundingClientRect().left;
      const touchY = touch.clientY - canvas.getBoundingClientRect().top;
      
      // 画面サイズに合わせてスケーリング
      const scaleX = SCREEN_WIDTH / canvas.clientWidth;
      const scaleY = SCREEN_HEIGHT / canvas.clientHeight;
      const scaledX = touchX * scaleX;
      const scaledY = touchY * scaleY;
      
      // 方向キー入力をタッチ位置から設定
      if (scaledX < SCREEN_WIDTH / 3) keys.ArrowLeft = true;
      if (scaledX > SCREEN_WIDTH * 2/3) keys.ArrowRight = true;
      if (scaledY < SCREEN_HEIGHT / 2) keys.ArrowUp = true;
      if (scaledY > SCREEN_HEIGHT / 2) keys.ArrowDown = true;
      
      // ダブルタップでボム使用（簡易実装）
      if (e.touches.length >= 2 && !gameState.gameOver) {
        keys.x = true;
        setTimeout(() => { keys.x = false; }, 100);
      }
    }
  }
  
  function handleTouchEnd() {
    resetKeys();
  }
  
  canvas.addEventListener('touchstart', handleTouch, false);
  canvas.addEventListener('touchmove', handleTouch, false);
  canvas.addEventListener('touchend', handleTouchEnd, false);
}

// ゲーム初期化とスタート
window.onload = function() {
  init();
  setupTouchControls();
};