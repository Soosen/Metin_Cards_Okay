from card import Card
import random
import numpy as np

PUNISHMENT_FOR_INVALID_MOVE = 5

class Game:
    def __init__(self):
        self.hand = list()
        self.unused_cards = self.generate_cards()
        self.unused_cards_sorted = np.ones(len(self.unused_cards))
        self.points = 0
        self.state = []
        self.update_state()
        self.moves = 0
        self.fitness = 300
 
    def copy(self):
        new_game = Game()
        new_game.hand = self.hand.copy()
        new_game.unused_cards = self.unused_cards.copy()
        new_game.unused_cards_sorted = self.unused_cards_sorted.copy()
        new_game.points = self.points
        new_game.state = self.state.copy()

        return new_game

    def start(self):
        self.shuffle_cards(self.unused_cards)
        for i in range(5):
            self.take_new_card()
        self.update_state()

    def generate_cards(self):
        cards = list()
        colors = ["blue", "red", "yellow"]
        for c in colors:
            for i in range(8):
                cards.append(Card(i + 1, c))
        return cards

    def shuffle_cards(self, cards):
        return random.shuffle(cards)

    def print_cards(self, cards):
        for c in cards:
            print(f"[{c.number}, {c.color}]")

    def take_new_card(self):
        if(len(self.hand) < 5):
            card_taken = self.unused_cards.pop()
            self.hand.append(card_taken)
            self.unused_cards_sorted[self.card_to_number(card_taken) - 1] = 0

    def remove_card(self, index):
        if(self.hand[index - 1]):
            del self.hand[index - 1]
            self.ftiness -= PUNISHMENT_FOR_INVALID_MOVE/2
        else:
            self.ftiness -= (PUNISHMENT_FOR_INVALID_MOVE * 2)
            pass
            
        if(len(self.unused_cards) > 0):
            self.take_new_card()

    
    def combine_cards(self, card_a, card_b, card_c):
        if(abs(card_a.number - card_b.number) + abs(card_a.number - card_c.number) + abs(card_b.number - card_c.number) == 4):
            if(card_a.color == card_b.color and card_a.color == card_c.color):
                self.points += 100
                self.fitness += 100
            else:
                self.points += min(card_a.number, card_b.number, card_c.number) * 10
                self.fitness += min(card_a.number, card_b.number, card_c.number) * 10

            self.hand.remove(card_a)
            self.hand.remove(card_b)
            self.hand.remove(card_c)

            return True

        elif(card_a.number == card_b.number and card_a.number == card_c.number):
            self.points += (card_a.number + 1) * 10
            self.hand.remove(card_a)
            self.hand.remove(card_b)
            self.hand.remove(card_c)

            return True

        self.fitness -= PUNISHMENT_FOR_INVALID_MOVE
        return False

    def card_to_number(self, card):
        if(card.color == "blue"):
            return card.number
        elif(card.color == "red"):
            return 8 + card.number
        else:
            return 16 + card.number

    def update_state(self):
        state = []

        self.hand.sort(key=lambda x:self.card_to_number(x))

        for c in self.hand:
            state.append(self.card_to_number(c))

        for i in range(5 -len(self.hand)):
            state.append(0)

        for c in self.unused_cards_sorted:
            state.append(int(c))
        
        state.append(self.points)

        self.state = state

    def reset_game(self):
        self.hand = list()
        self.unused_cards = self.generate_cards()
        self.unused_cards_sorted = np.ones(len(self.unused_cards))
        self.points = 0
        self.state = []
        self.update_state()

    def is_over(self):
        if(self.points >= 400):
            self.fitness += 300
        return (len(self.hand) + len(self.unused_cards)) < 3 or self.moves >= 24 or self.points >= 400


    def perform_action(self, action):
        action = round(action)
        self.moves += 1

        try:
            if(action == 1):
                self.remove_card(1)
            elif(action == 2):
                self.remove_card(2)
            elif(action == 3):
                self.remove_card(3)
            elif(action == 4):
                self.remove_card(4)
            elif(action == 5):
                self.remove_card(5)
            elif(action == 6):
                self.combine_cards(self.hand[0], self.hand[1], self.hand[2])
            elif(action == 7):
                self.combine_cards(self.hand[0], self.hand[1], self.hand[3])
            elif(action == 8):
                self.combine_cards(self.hand[0], self.hand[1], self.hand[4])
            elif(action == 9):
                self.combine_cards(self.hand[1], self.hand[2], self.hand[3])
            elif(action == 10):
                self.combine_cards(self.hand[1], self.hand[2], self.hand[4])
            elif(action == 11):
                self.combine_cards(self.hand[2], self.hand[3], self.hand[4])
        except:
            self.fitness -= PUNISHMENT_FOR_INVALID_MOVE * 2
            return

        while(len(self.hand) < 5 and len(self.unused_cards) > 0):
            self.take_new_card()

        self.update_state()




        
        
