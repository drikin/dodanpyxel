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

# Initialize and run the game
def main():
    global game_instance
    
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
