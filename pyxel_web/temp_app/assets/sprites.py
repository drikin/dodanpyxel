import pyxel

def init_sprites():
    """Define sprite data for the game"""
    
    # Create sprite bank for player ship
    player_ship = [
        0x00999000,
        0x09AAA900,
        0x9AAAAA90,
        0x9AAAAA90,
        0x9AAAAA90,
        0x9A9A9A90,
        0x99A9A990,
        0x09999900,
    ]
    
    # Create sprite bank for small enemy
    small_enemy = [
        0x00090000,
        0x00999000,
        0x09A9A900,
        0x99AAA990,
        0x9AAAAA90,
        0x09AAA900,
        0x00999000,
        0x00090000,
    ]
    
    # Create sprite bank for medium enemy
    medium_enemy = [
        0x0099990,
        0x09AAA90,
        0x9AAAA90,
        0x9A9A990,
        0x9A9A990,
        0x9AAAA90,
        0x09AAA90,
        0x0099990,
    ]
    
    # Create sprite bank for large enemy
    large_enemy = [
        0x0009900000,
        0x0099990000,
        0x099AA99000,
        0x99AAAA9900,
        0x9AAAAAA900,
        0x9AAAAAA900,
        0x99AAAA9900,
        0x099AA99000,
        0x0099990000,
        0x0009900000,
    ]
    
    # You would normally place these in the Pyxel resource file
    # Since we're working with minimal assets, these sprite definitions 
    # are provided for reference, but we'll use primitive shapes in the code
