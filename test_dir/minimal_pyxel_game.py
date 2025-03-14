import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Minimal Pyxel Game")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.text(31, 61, "Press Q to quit.", 13)
        
App()