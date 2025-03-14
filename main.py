import pyxel
from game import Game
import platform
import os

# Global game instance for module access
game_instance = None

# モバイルモード判定
MOBILE_MODE = False
WEB_MODE = False

# マウスボタン定数（異なるPyxelバージョンで互換性を持たせる）
MOUSE_BUTTON_LEFT = 0

# Pyxel versions compatibility patch
def patch_pyxel_compatibility():
    """Add compatibility for different pyxel versions"""
    global MOUSE_BUTTON_LEFT, WEB_MODE
    
    # Direct key code support for older Pyxel versions
    if not hasattr(pyxel, 'KEY_Z'):
        pyxel.KEY_Z = 122  # ASCII code for 'z'
    if not hasattr(pyxel, 'KEY_X'):
        pyxel.KEY_X = 120  # ASCII code for 'x'
    if not hasattr(pyxel, 'KEY_SPACE'):
        pyxel.KEY_SPACE = 32  # ASCII code for space
    if not hasattr(pyxel, 'KEY_RETURN'):
        pyxel.KEY_RETURN = 13  # ASCII code for return/enter
    
    # Add btn_direct method for direct key code checking
    if not hasattr(pyxel, 'btn_direct'):
        def btn_direct(key_code):
            """Check key by direct ASCII code, fallback for older pyxel versions"""
            try:
                # Try normal btn first
                return pyxel.btn(key_code)
            except:
                # Fall back to lowercase ASCII codes
                key_map = {
                    122: pyxel.btn(pyxel.KEY_Z) if hasattr(pyxel, 'KEY_Z') else False,  # z key
                    32: pyxel.btn(pyxel.KEY_SPACE) if hasattr(pyxel, 'KEY_SPACE') else False,  # space
                }
                return key_map.get(key_code, False)
        
        # Monkey patch the function
        pyxel.btn_direct = btn_direct
        
    # Add direct key_press detection (macOS compatibility)
    if not hasattr(pyxel, 'key_press'):
        def key_press(key_value):
            """Multi-method key detection that works across environments"""
            try:
                # Try built-in methods
                if isinstance(key_value, int):
                    return pyxel.btn(key_value)
                elif isinstance(key_value, str) and len(key_value) == 1:
                    # Try to check by ASCII code
                    return pyxel.btn(ord(key_value.lower()))
            except:
                pass
            
            # Last resort - try keyboard module
            try:
                import keyboard
                return keyboard.is_pressed(key_value)
            except:
                return False
        
        # Add our custom function
        pyxel.key_press = key_press
    
    # Check for web mode
    WEB_MODE = hasattr(pyxel, 'app2html')
    
    # Fix mouse button constants
    if not hasattr(pyxel, 'MOUSE_BUTTON_LEFT'):
        MOUSE_BUTTON_LEFT = 0
    else:
        MOUSE_BUTTON_LEFT = pyxel.MOUSE_BUTTON_LEFT

# モバイルモードを検出
def detect_mobile_mode():
    """モバイルデバイスかどうかを検出する"""
    global MOBILE_MODE
    
    # 環境変数でモバイルモードを強制的に設定可能
    if os.environ.get('FORCE_MOBILE_MODE') == '1':
        print("Mobile mode forced by environment variable")
        MOBILE_MODE = True
        return True
    
    # WEB_MODEではJavaScriptから検出されるので、カスタムタグ用に対応
    # Webブラウザからの実行の場合
    try:
        # Pyxelのグローバル変数にアクセスを試みる
        mobile_detected = False
        if hasattr(pyxel, "app") and hasattr(pyxel.app, "mobile_detected"):
            mobile_detected = pyxel.app.mobile_detected
            print(f"Mobile detection from Pyxel: {mobile_detected}")
            MOBILE_MODE = mobile_detected
            return mobile_detected
    except Exception as e:
        print(f"Error detecting mobile mode: {e}")
    
    # UserAgentベースの検出は不可能なので、画面サイズベースの推測
    # Pyxelの低解像度ゲームなのでタッチコントロールは常に有効にするのが良い
    MOBILE_MODE = True
    return True

# Initialize and run the game
def main():
    global game_instance, MOBILE_MODE, WEB_MODE, MOUSE_BUTTON_LEFT
    
    # Apply compatibility patches
    patch_pyxel_compatibility()
    
    # モバイルモード検出
    detect_mobile_mode()
    
    # Initialize game
    game_instance = Game()
    
    # モバイルモードの設定
    if MOBILE_MODE or WEB_MODE:
        print("Mobile mode detected - enabling touch controls")
        game_instance.touch_enabled = True
        game_instance.mobile_mode = True
        
        # モバイル用の調整を行う
        try:
            # マウス入力を有効にする
            pyxel.mouse(True)
        except Exception as e:
            print(f"Error enabling mouse for touch: {e}")
    
    # トラブルシューティング: game_instanceが正しく設定されているか確認
    print("DEBUG: game_instance initialized:", game_instance)
    print("DEBUG: Has player_bullets attribute:", hasattr(game_instance, 'player_bullets'))
    print(f"DEBUG: Mobile mode: {MOBILE_MODE}, Web mode: {WEB_MODE}")
    
    # Start the game loop
    pyxel.run(game_instance.update, game_instance.draw)

if __name__ == "__main__":
    main()
