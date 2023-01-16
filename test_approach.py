from game import Game
import math

def play_game(game):
    #check if there are any triples in hand and use them
    #print(game.state)
    while(not game.is_over()):
        while(not game.is_over()):
            triples = check_for_tirples_in_hand(game)

            if(len(triples) != 0):
                index = find_best_triple(triples, game)
                game.combine_cards(game.hand[triples[index][0]], game.hand[triples[index][1]], game.hand[triples[index][2]])

                while(len(game.hand) < 5 and len(game.unused_cards) != 0):
                    game.take_new_card()

                game.update_state()
                #print(game.state)
            else:
                break
    
        #check which card remove leaves the most triples
        index = find_best_remove(game)
        if(len(game.hand) != 0):
            game.remove_card(index)
        if(len(game.hand) < 5 and len(game.unused_cards) != 0):
            game.take_new_card()
        game.update_state()
       #print(game.state)

    return game.points
    

def find_best_remove(game):

    game_cards_state = game.unused_cards_sorted
    for c in game.hand:
        game_cards_state[game.card_to_number(c) - 1] = 1

    importance = [0,0,0,0,0]
    for c in range(len(game.hand)):
        for k in range(c):
            if(k != c):
                if(abs(game.card_to_number(game.hand[c]) - game.card_to_number(game.hand[k])) == 1 and game.hand[c].color == game.hand[k].color):
                    min_card = min(game.card_to_number(game.hand[c]), game.card_to_number(game.hand[k]))
                    max_card = max(game.card_to_number(game.hand[c]), game.card_to_number(game.hand[k]))
                    if(min_card >= 2 and game_cards_state[min_card - 2] == 1):
                        importance[c] += 1
                        importance[k] += 1
                    if(max_card <= 22 and game_cards_state[max_card] == 1):
                        importance[c] += 1
                        importance[k] += 1

                if(abs(game.card_to_number(game.hand[c]) - game.card_to_number(game.hand[k])) == 2 and game.hand[c].color == game.hand[k].color):
                    min_card = min(game.card_to_number(game.hand[c]), game.card_to_number(game.hand[k]))
                    max_card = max(game.card_to_number(game.hand[c]), game.card_to_number(game.hand[k]))
                    if(game_cards_state[min_card] == 1):
                        importance[c] += 1
                        importance[k] += 1

    best_score = -math.inf
    best_index = -1
    worst_importance = 3
    for i in range(len(game.hand)):
        temp_game = game.copy()
        temp_game.remove_card(i + 1)

        if(importance[i] <= worst_importance):
            if(importance[i] < worst_importance):
                best_score = -math.inf
                
            remaining_triples = calculate_remaining_triples(temp_game)
            worst_importance = importance[i]
            if(remaining_triples > best_score):
                best_score = remaining_triples
                best_index = i
        
        return best_index + 1
    

def check_for_tirples_in_hand(game):
    triples = []

    try:
        if(is_triple(game.hand[0], game.hand[1], game.hand[2])):
            triples.append([0, 1, 2])
    except:
        pass
    try:
        if(is_triple(game.hand[0], game.hand[1], game.hand[3])):
            triples.append([0, 1, 3])
    except:
        pass

    try:
        if(is_triple(game.hand[0], game.hand[1], game.hand[4])):
            triples.append([0, 1, 4])
    except:
        pass
    try:
        if(is_triple(game.hand[1], game.hand[2], game.hand[3])):
            triples.append([1, 2, 3])
    except:
        pass

    try:
        if(is_triple(game.hand[1], game.hand[2], game.hand[4])):
            triples.append([1, 2, 4])
    except:
        pass

    try:
        if(is_triple(game.hand[2], game.hand[3], game.hand[4])):
            triples.append([2, 3, 4])
    except:
        pass

    return triples

def is_triple(card_a, card_b, card_c):
    if(abs(card_a.number - card_b.number) + abs(card_a.number - card_c.number) + abs(card_b.number - card_c.number) == 4):
        if(card_a.color == card_b.color and card_a.color == card_c.color):
            return True
    
    return False

def calculate_remaining_triples(game):
    game_cards_state = game.unused_cards_sorted
    for c in game.hand:
        game_cards_state[game.card_to_number(c) - 1] = 1

    triples = 0
    for i in range(6):
        for j in range(3):
            if(game_cards_state[i + 8 * j] == 1 and game_cards_state[(i + 1) + 8 * j] == 1 and game_cards_state[(i + 2) + 8 * j] == 1):
                triples += 1

    return triples

def find_best_triple(triples, game):
    best_score = -math.inf
    best_index = -1
    for i in range(len(triples)):
        test_game = game.copy()
        test_game.combine_cards(
            test_game.hand[triples[i][0]], test_game.hand[triples[i][1]], test_game.hand[triples[i][2]])

        remaining_triples = calculate_remaining_triples(test_game)

        if(remaining_triples > best_score):
            best_score = remaining_triples
            best_index = i

    return best_index


results = dict()
for i in range(5):
    results[i * 100] = 0

for i in range(1000):
    game = Game()
    game.start()
    res = play_game(game)
    results[res] = results[res] + 1

print(results)

