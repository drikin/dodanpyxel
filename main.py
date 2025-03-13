import os
# VNC互換性のために環境変数を設定 - Pyxelのインポート前に実行する必要があります
os.environ['PYXEL_RENDERER'] = 'software'
# OpenGLを無効化
os.environ['PYXEL_GRAPHICS_DRIVER'] = 'software'
os.environ['PYXEL_GLFW_WINDOW_API'] = 'x11'

# 環境変数を設定した後でPyxelをインポート
import pyxel
from game import Game

# Global game instance for module access
game_instance = None

# Pyxel versions compatibility patch
def patch_pyxel_compatibility():
    """Add compatibility for different pyxel versions"""
    # Direct key code support for older Pyxel versions
    if not hasattr(pyxel, 'KEY_Z'):
        pyxel.KEY_Z = 122  # ASCII code for 'z'
    if not hasattr(pyxel, 'KEY_SPACE'):
        pyxel.KEY_SPACE = 32  # ASCII code for space
    
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

# Initialize and run the game
def main():
    global game_instance
    
    # VNC互換性のためのデバッグ情報を表示
    print("DEBUG: Using software renderer for VNC compatibility")
    print(f"DEBUG: PYXEL_RENDERER={os.environ.get('PYXEL_RENDERER', 'not set')}")
    print(f"DEBUG: PYXEL_GRAPHICS_DRIVER={os.environ.get('PYXEL_GRAPHICS_DRIVER', 'not set')}")
    
    # 追加の設定 - 最新のPyxelバージョン向け
    try:
        if hasattr(pyxel, 'settings'):
            try:
                pyxel.settings.renderer = 'software'
                print("DEBUG: Set renderer via pyxel.settings.renderer")
            except Exception as e:
                print(f"NOTICE: Could not set pyxel.settings.renderer: {e}")
    except Exception as e:
        print(f"WARNING: Settings error: {e}")
    
    # Apply compatibility patches
    patch_pyxel_compatibility()
    
    # Initialize game
    game_instance = Game()
    
    # トラブルシューティング: game_instanceが正しく設定されているか確認
    print("DEBUG: game_instance initialized:", game_instance)
    print("DEBUG: Has player_bullets attribute:", hasattr(game_instance, 'player_bullets'))
    
    # Start the game loop
    pyxel.run(game_instance.update, game_instance.draw)

if __name__ == "__main__":
    main()
