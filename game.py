from card import Card
import random
import numpy as np
import pickle
import math

PUNISHMENT_FOR_INVALID_MOVE = 5

class Game:
    def __init__(self):
        self.hand = [0, 0, 0, 0, 0]
        self.unused_cards = self.generate_cards()
        self.unused_cards_sorted = np.ones(len(self.unused_cards))
        self.points = 0
        self.state = []
        self.chamber = [-1, -1, -1]
        self.update_state()
        self.moves = 0
        self.fitness = 240
        self.chosen_action = 0
        self.history = []
 
    def copy(self):
        new_game = Game()
        new_game.hand = self.hand.copy()
        new_game.unused_cards = self.unused_cards.copy()
        new_game.unused_cards_sorted = self.unused_cards_sorted.copy()
        new_game.points = self.points
        new_game.state = self.state.copy()
        new_game.fitness = self.fitness 
        new_game.chamber = self.chamber
        new_game.history = self.history

        return new_game

    def start(self):
        self.shuffle_cards(self.unused_cards)
        self.refill_cards()
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
        if(len(self.hand) <= 5 and 0 in self.hand):
            card_taken = self.unused_cards.pop()
            self.hand[self.hand.index(0)] = card_taken
            self.unused_cards_sorted[self.card_to_number(card_taken) - 1] = 0

    def refill_cards(self):
        while(0 in self.hand and len(self.unused_cards)):
            self.take_new_card()

    def remove_card(self, index):
        if(self.hand[index - 1]):
            self.hand[index - 1] = 0
            self.fitness -= PUNISHMENT_FOR_INVALID_MOVE/2
            self.refill_cards()
            return True
        else:
            self.fitness -= (PUNISHMENT_FOR_INVALID_MOVE * 2)
            return False
            
    
    def combine_cards(self, card_a, card_b, card_c):
        if(abs(card_a.number - card_b.number) + abs(card_a.number - card_c.number) + abs(card_b.number - card_c.number) == 4):
            if(card_a.color == card_b.color and card_a.color == card_c.color):
                self.points += 100
                self.fitness += 100
            else:
                self.points += min(card_a.number, card_b.number, card_c.number) * 10
                self.fitness += min(card_a.number, card_b.number, card_c.number) * 10

            self.hand[self.hand.index(card_a)] = 0
            self.hand[self.hand.index(card_b)] = 0
            self.hand[self.hand.index(card_c)] = 0

            return True

        elif(card_a.number == card_b.number and card_a.number == card_c.number):
            self.points += int((card_a.number + 1) * 10)
            self.fitness += int((card_a.number + 1) * 10)

            self.hand[self.hand.index(card_a)] = 0
            self.hand[self.hand.index(card_b)] = 0
            self.hand[self.hand.index(card_c)] = 0

            return True

        self.fitness -= PUNISHMENT_FOR_INVALID_MOVE * 2
        return False

    def card_to_number(self, card):
        if(card.color == "blue"):
            return card.number
        elif(card.color == "red"):
            return 8 + card.number
        else:
            return 16 + card.number

    def number_to_card(sefl, number):
        num = (number % 8) + 1
        col = math.floor(number / 8)
        if(col == 0):
            color = "blue"
        elif(col == 1):
            color = "red"
        else:
            color = "yellow"

        return Card(num, color)

    def update_state(self):
        state = []
        hand_sorted = []
        
        for i in range(len(self.hand)):
            if(self.hand[i] != 0):
                hand_sorted.append(self.card_to_number(self.hand[i]))
            else:
                hand_sorted.append(0)
            
        hand_sorted.sort()

        for c in hand_sorted:
                state.append(c)

        for i in range(5 -len(self.hand)):
            state.append(0)

        for c in self.unused_cards_sorted:
            state.append(int(c))
        
        state.append(self.points)

        self.state = state

    def reset_game(self):
        game = Game()
        game.start()
        return game

    def is_over(self):
        if(self.points >= 400):
            self.fitness += 300
        return (len(self.hand) - self.hand.count(0) + len(self.unused_cards)) < 3 or self.moves >= 24


    def perform_action(self, action):
        self.moves += 1
        success = False
        try:
            if(action == 1):
                success = self.remove_card(1)
            elif(action == 2):
                success = self.remove_card(2)
            elif(action == 3):
                success = self.remove_card(3)
            elif(action == 4):
                success = self.remove_card(4)
            elif(action == 5):
                success = self.remove_card(5)
            elif(action == 6):
                success = self.combine_cards(self.hand[0], self.hand[1], self.hand[2])
            elif(action == 7):
                success = self.combine_cards(self.hand[0], self.hand[1], self.hand[3])
            elif(action == 8):
                success = self.combine_cards(self.hand[0], self.hand[1], self.hand[4])
            elif(action == 9):
                success = self.combine_cards(self.hand[0], self.hand[2], self.hand[3])
            elif(action == 10):
                success = self.combine_cards(self.hand[0], self.hand[2], self.hand[4])
            elif(action == 11):
                success = self.combine_cards(self.hand[0], self.hand[3], self.hand[4])
            elif(action == 12):
                success = self.combine_cards(self.hand[1], self.hand[2], self.hand[3])
            elif(action == 13):
                success = self.combine_cards(self.hand[1], self.hand[2], self.hand[4])
            elif(action == 14):
                success = self.combine_cards(self.hand[1], self.hand[3], self.hand[4])            
            elif(action == 15):
                success = self.combine_cards(self.hand[2], self.hand[3], self.hand[4])
        except Exception as e:
            print(e)
            self.fitness -= PUNISHMENT_FOR_INVALID_MOVE * 2
            return False

        self.refill_cards()

        self.update_state()
        return success


    def combine_indexes_to_action(self, combine_indexes):
        if(0 in combine_indexes and 1 in combine_indexes and 2 in combine_indexes):
            return 6
        elif(0 in combine_indexes and 1 in combine_indexes and 3 in combine_indexes):
            return 7
        elif(0 in combine_indexes and 1 in combine_indexes and 4 in combine_indexes):
            return 8
        elif(0 in combine_indexes and 2 in combine_indexes and 3 in combine_indexes):
            return 9
        elif(0 in combine_indexes and 2 in combine_indexes and 4 in combine_indexes):
            return 10
        elif(0 in combine_indexes and 3 in combine_indexes and 4 in combine_indexes):
            return 11
        elif(1 in combine_indexes and 2 in combine_indexes and 3 in combine_indexes):
            return 12
        elif(1 in combine_indexes and 2 in combine_indexes and 4 in combine_indexes):
            return 13
        elif(1 in combine_indexes and 3 in combine_indexes and 4 in combine_indexes):
            return 14
        elif(2 in combine_indexes and 3 in combine_indexes and 4 in combine_indexes):
            return 15

    def save_history(self):
        try:
            with open("games_history.pkl", "rb") as f:
                full_history = pickle.load(f)
        except:
            full_history = []

        full_history.append(self.history)

        with open("games_history.pkl", 'wb') as f:
            pickle.dump(full_history, f)

    def load_personal_score(self):
        try:
            with open("personal_score.pkl", "rb") as f:
                personal_score = pickle.load(f)
        except:
            personal_score = {
                "wins": 0,
                "loses": 0,
                "resets": 0
            }
        return personal_score

    def update_personal_score(self, personal_score):  
        with open("personal_score.pkl", 'wb') as f:
            pickle.dump(personal_score, f)


        


        
        
