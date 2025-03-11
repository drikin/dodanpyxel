import pyxel
from constants import *

def init_sounds():
    """Initialize game sound effects"""
    
    # Sound effect 0: Player shot
    pyxel.sounds[0] = pyxel.Sound()
    pyxel.sounds[0].set("C3C4", "T", "7", "N", 20)
    
    # Sound effect 1: Explosion
    pyxel.sounds[1] = pyxel.Sound()
    pyxel.sounds[1].set("F2F1", "N", "7", "F", 10)
    
    # Sound effect 2: Game Start
    pyxel.sounds[2] = pyxel.Sound()
    pyxel.sounds[2].set("C3E3G3C4", "T", "7", "N", 10)
    
    # Sound effect 3: Game Over
    pyxel.sounds[3] = pyxel.Sound()
    pyxel.sounds[3].set("C4G3E3C3", "S", "7", "F", 5)
