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
EPISODES = 100000 # number of times the game is played
EPSILON_INIT = 0.99 # initial probability of doing a random move
EPSILON_FINAL = 0.0001
EPSILON_DECAY = 0.999 # rate that epsilon decreases every move (if 0.999, after 700 episodes epsilon=.5)
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
# D = deque()
D = np.zeros([REPLAY_MEMORY, 35])

# Initialize the player and the game
player = Player()
game = Game(highscore)

t = 0

# Play the game "EPISODES" number of times
for episode_i in range(1, EPISODES):
    # Start new game
    game.reset()
    state = np.array(game.board, copy=True).flatten() # 4x4 np array containing tile information

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
            q_func = player.model.predict(state.reshape(1,16))[0]
            action = np.argmax(q_func)

        # Execute this action and observe reward r and new state
        game.move(action)
        reward = game.getReward()
        new_state = np.array(game.board, copy=True).flatten()
        done = game.gameOver

        if len(D) > REPLAY_MEMORY:
            # Pop off the old data from the deque
            D[:-1,:] = D[1:,:]
            # Store experience in replay memory D
            D[-1,:] = np.hstack((state, action, reward, new_state, done))
        else:
            # If the deque isn't full yet, add new data to the correct location
            D[t,:] = np.hstack((state, action, reward, new_state, done))

        # If there are enough items in the deque...
        if t > OBSERVE_COUNT:
            # Sample random transitions from replay memory D
            # replay_batch = random.sample(list(D), BUFFER_BATCH_SIZE)
            randomRows = np.random.choice(min(t, REPLAY_MEMORY), size=BUFFER_BATCH_SIZE)
            replay_batch = D[randomRows, :]
            # states, actions, rewards, new_states, dones = zip(*replay_batch)
            states = replay_batch[:,0:16]
            actions = replay_batch[:,16]
            rewards = replay_batch[:,17]
            new_states = replay_batch[:,18:-1]
            dones = replay_batch[:,-1]

            evaluations = player.model.predict(new_states)
            print("evaluations")
            print(evaluations)
            exit()

            targets = rewards
            targets[np.where(dones==0)] += GAMMA * np.max(evaluations[np.where(dones==0)])



            

            # targets = np.zeros(BUFFER_BATCH_SIZE)
            # for i in range(BUFFER_BATCH_SIZE):
            #     if dones[i]:
            #         targets[i] = rewards[i]
            #     else:
            #         targets[i] = rewards[i] + GAMMA * np.max(evaluations[i]))

            for i in range(len(evaluations)):
                evaluations[i][actions[i]] = targets[i]

            player.model.fit(states, evaluations, verbose=0)

            if epsilon > EPSILON_FINAL:
                epsilon *= EPSILON_DECAY
        else:
            t += 1 # increment timestep

        state = new_state # Update state

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