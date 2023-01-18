import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from game import Game
import pickle
import os
import multiprocessing


def main():
    try:
        generation = load_generation("generations/gen.pkl")
    except:
        generation = create_first_candidates()  
    try:
        with open("game.pkl", "rb") as f:
            games = pickle.load(f)
    except:
        games = []  
        for i in range(3):   
            game = Game()
            game.start()
            games.append(game)

    game = Game()
    game.start()
    gens = 5
    for i in range(gens):
        print("Generation: " + str(i + 1))
        fitness= train(generation, game)
        print(fitness)
        generation = create_new_generation(generation, fitness)
        if(i % 10 == 9):
            save_generation(generation, "generations/gen.pkl")

    save_generation(generation, "generations/gen.pkl")

    with open("game.pkl", 'wb') as f:
        # Write the generation to the file
        pickle.dump(game, f)

def create_first_candidates():
    # Create a list to store the 100 neural networks
    neural_networks = []

    # Define the number of inputs and outputs for the neural networks
    num_inputs = 30
    num_outputs = 15
    # Create a loop to generate 100 neural networks
    for i in range(100):
        print("Creating new randomized model: " + str(i))
        # Create a new neural network
        model = Sequential()
        # Add a fully connected layer with 32 units and 'relu' activation
        model.add(Dense(32, activation='relu', input_shape=(30,)))

        # Add a fully connected layer with 15 units and 'softmax' activation
        model.add(Dense(15, activation='softmax'))

        # Compile the model with 'adam' optimizer and 'categorical_crossentropy' loss
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Randomize the weights of the neural network
        weights = model.get_weights()
        weights = [np.random.normal(size=w.shape) for w in weights]
        model.set_weights(weights)

        # Add the neural network to the list
        neural_networks.append(model)

    return neural_networks


def create_new_generation(neural_networks, fitness):
    # Define the number of new neural networks to create
    num_new_networks = 100

    # Create a list to store the new neural networks
    new_generation = []

    # Define the number of candidates to select for crossover
    num_candidates = 2

    # Create a loop to create the new neural networks
    for i in range(num_new_networks):
        # Select the candidates for crossover
        candidates = []
        for j in range(num_candidates):
            # Normalize the fitness values
            fitness_sum = sum(fitness)
            norm_fitness = [f/fitness_sum for f in fitness]

            # Select a random candidate based on its fitness
            r = random.random()
            for k, f in enumerate(norm_fitness):
                r -= f
                if r <= 0:
                    candidates.append(k)
                    break

        # Get the weights of the two selected candidates
        parent1_weights = neural_networks[candidates[0]].get_weights()
        parent2_weights = neural_networks[candidates[1]].get_weights()

        # Crossover the weights
        child_weights = []
        for p1_w, p2_w in zip(parent1_weights, parent2_weights):
            # Select a random point for crossover
            crossover_point = np.random.randint(p1_w.size)
            # Create the child weights
            child_w = np.concatenate(
                [p1_w.ravel()[:crossover_point], p2_w.ravel()[crossover_point:]])
            # reshape to original shape
            child_w = child_w.reshape(p1_w.shape)
            child_weights.append(child_w)

        # Mutate the weights
        mutation_rate = 0.3
        for i in range(len(child_weights)):
            if np.random.rand() < mutation_rate:
                child_weights[i] += np.random.normal(
                    scale=0.2, size=child_weights[i].shape)

        num_inputs = 30
        num_outputs = 15

        # Create a new neural network with the child weights
        model = Sequential()
        # Add a fully connected layer with 32 units and 'relu' activation
        model.add(Dense(32, activation='relu', input_shape=(30,)))

        # Add a fully connected layer with 15 units and 'softmax' activation
        model.add(Dense(15, activation='softmax'))

        # Compile the model with 'adam' optimizer and 'categorical_crossentropy' loss
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.set_weights(child_weights)

        # Add the new neural network to the new generation
        new_generation.append(model)

    return new_generation

def train(generation, game):
    fitness = []
    #template_game = Game()
    #template_game.start()
    i = 0
    for individual in generation:
        i += 1
        #template_game = games[random.randint(0, 2)].copy()
        template_game = Game()
        template_game.start()
       #print(template_game.state)
        print("Training Individual: " + str(i))
        fitness.append(play_game(individual, template_game))
        print(fitness)

    return fitness


def play_game(individual, template_game):
    game = template_game.copy()
    #game = Game()
    #game.start()
    while(not game.is_over()):
        #print(game.state)
        predictions = individual.predict([game.state], verbose=False)
        action = np.argmax(predictions) + 1
        #print(action)
        game.perform_action(action)
    
    return int(max(game.fitness, 1))

def save_generation(generation, file_name):
    if not os.path.exists(file_name):
        # Create the directory
        os.makedirs(file_name)

    with open(file_name, 'wb') as f:
        # Write the generation to the file
        pickle.dump(generation, f)


def load_generation(filename):
    with open(filename, "rb") as f:
        neural_networks = pickle.load(f)

    for model in neural_networks:
        model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    return neural_networks


if __name__ == '__main__':
    main()

