from game import Game
from card import Card

def main():
    game = Game()
    game.shuffle_cards(game.unused_cards)
    game.start()
    print(game.state)
    game.remove_card(1)
    print(game.state)
    


if __name__ == '__main__':
    main()
