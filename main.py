import pyxel
from game import Game

# Global game instance for module access
game_instance = None

# Initialize and run the game
def main():
    global game_instance
    game_instance = Game()
    pyxel.run(game_instance.update, game_instance.draw)

if __name__ == "__main__":
    main()
