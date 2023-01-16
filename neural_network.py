import tensorflow as tf
from game import Game
import numpy as np


try:
    model = tf.keras.models.load_model('models/model', compile = False)
    model.load_weights('models/weights')
except:
    # Define the neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, input_shape=(
            30,), activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(11)
    ])

model.compile(loss='mse', optimizer='adam')

def play_game():
    game = Game()
    game.start()
    game_states = []
    rewards = []
    while not game.is_over():
        game_states.append(game.state)
        #print(game.state)
        points_before = game.points
        action = model.predict([game.state], verbose = 0)
        action = np.argmax(action) + 1
        #print(action)
        game.perform_action(action)
        reward = game.points - points_before
        if(game.points >= 400):
            reward = 1000
        rewards.append(reward)
    return game_states, rewards


rew = []
games = 1000
best = -400
suma = []
for j in range(2):
    for i in range(games):
        print(f"{i}/{games}")
        game_states, rewards = play_game()
        rew.append(np.sum(rewards))
        if(rew[-1] > best):
            best = rew[-1]
            best_sceniario = game_states
        model.fit(game_states, rewards)
    suma.append(sum(rew))
    suma = []

for s in suma:
    print(s)

print(rew)
for s in best_sceniario:
    print(s)
print(best)
tf.keras.models.save_model(model, 'models/model', save_format='tf')
model.save_weights('models/weights', save_format='tf')
