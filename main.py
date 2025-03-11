import pyxel
from game import Game

# Initialize and run the game
def main():
    game = Game()
    pyxel.run(game.update, game.draw)

if __name__ == "__main__":
    main()
