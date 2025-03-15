import pyxel
from game import Game
import platform
import os

# Global game instance for module access
game_instance = None

# 純粋なPyxelアプリケーションとして実行
TITLE = "LAST DESCENT: THE FINAL HOPE"
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
    
    # キーボード操作をメインにするため、モバイルモードをオフに設定
    print("Mobile mode disabled - keyboard controls only")
    MOBILE_MODE = False
    return False

# Initialize and run the game
def main():
    global game_instance, MOBILE_MODE, WEB_MODE, MOUSE_BUTTON_LEFT
    
    # Pyxel初期化（ここでウィンドウサイズとフレームレートを設定）
    pyxel.init(160, 240, title=TITLE, fps=60, quit_key=pyxel.KEY_NONE)
    
    # Apply compatibility patches
    patch_pyxel_compatibility()
    
    # キーボード専用モードに設定
    detect_mobile_mode()
    
    # サウンドの初期化を明示的に行う
    from assets.sounds import init_sounds
    try:
        init_sounds()
        print("DEBUG: Sounds initialized successfully")
    except Exception as e:
        print(f"ERROR initializing sounds: {e}")
    
    # ゲームを初期化
    game_instance = Game()
    
    # デバッグ情報
    print("DEBUG: game_instance initialized:", game_instance)
    print("DEBUG: Has player_bullets attribute:", hasattr(game_instance, 'player_bullets'))
    
    # Start the game loop
    pyxel.run(game_instance.update, game_instance.draw)

if __name__ == "__main__":
    main()
