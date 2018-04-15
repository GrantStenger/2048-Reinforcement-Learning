#Packages
import matplotlib.pyplot as plt
from collections import deque
from player import Player
from game import Game
import numpy as np
import scipy.stats
import random
import keras
import time

#Parameters Used
EPISODES = 2000000 # number of times the game is played
EPSILON_INIT = 0.99 # initial probability of doing a random move
EPSILON_FINAL = 0.01
EPSILON_DECAY = 0.995 # rate that epsilon decreases every move (if 0.999, after 700 moves epsilon=.5)
BUFFER_BATCH_SIZE = 32 # number of states and targets sampled per training round (25)
GAMMA = 0.9 #(0.9)
REPLAY_MEMORY = 50000
#OBSERVE_COUNT = 100000
OBSERVE_COUNT = 500

num_actions = 4 # up, down, left, right
highscore = 0 # Initial high score set to 0
epsilon = EPSILON_INIT # Set initial value of epsilon
scores = [] # Stores the final score of every game

# Initialize replay memory D where the actions will be stored
D = deque()

# Initialize the player and the game
player = Player()
game = Game(highscore)

t = 1

# Play the game "EPISODES" number of times
for episode_i in range(1, EPISODES):
    # Start new game
    game.reset()
    state = np.array(game.board, copy=True) # 4x4 np array containing tile information

    game_move_count = 0
    # Play game until no more moves can be made
    start = time.time()
    while not game.gameOver:
        game_move_count += 1
        # With probability epsilon, select a random action
        if np.random.rand() <= epsilon:
            action = random.randrange(num_actions)
        # Otherwise, select the action with the highest predicted discounted future reward
        else:
            q_func = player.model.predict(np.array([state.flatten()]))[0]
            action = np.argmax(q_func)

        # Execute this action and observe reward r and new state
        reward = game.next_move(action)
        new_state = np.array(game.board, copy=True)
        done = game.gameOver

        # Store experience in replay memory D

        D.append((state, action, reward, new_state, done))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        # If there are enough items in the deque...
        if t > OBSERVE_COUNT:
            # Sample random transitions from replay memory D
            replay_batch = random.sample(list(D), BUFFER_BATCH_SIZE)
            states, actions, rewards, new_states, dones = zip(*replay_batch)

            rewards = np.array(rewards)

            new_states = np.array(new_states)
            new_states = new_states.reshape(-1, new_states.shape[1] *
                    new_states.shape[2])

            states = np.array(states)
            states = states.reshape(-1, states.shape[1] * states.shape[2])

            evaluated = player.model.predict(new_states)

            targets = []
            for i in range(BUFFER_BATCH_SIZE):
                if dones[i]:
                    targets.append(rewards[i])
                else:
                    targets.append(rewards[i] + GAMMA * np.max(evaluated[i]))
            targets = np.array(targets)

            for i in range(len(evaluated)):
                evaluated[i][actions[i]] = targets[i]

            player.model.fit(states, evaluated, verbose=0)

            if epsilon > EPSILON_FINAL:
                epsilon *= EPSILON_DECAY

        state = new_state # Update state
        t += 1 # increment timestep

    end = time.time()
    if episode_i % 1 == 0:
        if t < OBSERVE_COUNT:
            state = 'Observing'
        else:
            state = 'Exploring'
        print("%s %i (%i): %i, %.2f, %.2f" % (state, game_move_count, episode_i, int(game.score),
            np.mean(scores), (end - start)))

    scores.append(game.score)
    if len(scores) > 100:
        scores.pop(0)


print(scores)

"""
Next Steps:
Try Monte Carlo tree search just to get the game working. Deep RL is hard.
Tweak hyperparameters
Train for WAY more time.

"""