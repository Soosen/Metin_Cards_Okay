from game import Game
import gui
import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Metin2 Okey Cards Simulator"

def main():
    game = Game()
    GameWin = gui.GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, game)
    GameWin.setup()
    arcade.run()
    

if __name__ == '__main__':
    main()
