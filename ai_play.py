#Packages
import numpy as np
from game import Game
from collections import deque
import random
from player import Player
import tensorflow as tf
import keras

#Parameters Used
EPISODES = 5 # number of times the game is played
EPSILON_INIT = 1 # initial probability of doing a random move
EPSILON_DECAY = .999 # rate that epsilon decreases every move (after 700 moves epsilon=.5)
BUFFER_BATCH_SIZE = 10

# Parameters Currently Unused
EPOCHS = 5 # initially set to 5 for fast training time
BATCH_SIZE = 32 
GAMMA = 0.9 # decay rate of past observations (try .98)
LEARNING_RATE = .0001

num_actions = 4 # up, down, left, right
highscore = 0 # Initial high score set to 0
epsilon = EPSILON_INIT # Set initial value of epsilon
scores = []

# Initialize replay memory D where the actions will be stored
D = deque()

# Initialize the player and the game
player = Player()
game = Game(highscore)

# Play the game "EPISODES" number of times
for i in range(EPISODES):

	# Start new game
	game.reset() 
	state = np.array(game.board, copy=True) # 4x4 np array containing tile information
	t = 1 # timestep value

	# Play game until no more moves can be made
	while not game.gameOver:

		# With probability epsilon, select a random action
		if np.random.rand() <= epsilon:
			action = random.randrange(num_actions)
		# Otherwise, select the action with the highest predicted discounted future reward
		else:
			action = player.select_action(state)

		# Execute this action and observe reward r and new state
		reward = game.next_move(action)
		new_state = np.array(game.board, copy=True)

		# Store experience in replay memory D
		D.append((state, action, reward, new_state))

		# If there are enough items in the deque...
		if len(D) >= BUFFER_BATCH_SIZE:

			# Sample random transitions from replay memory D
			replay_batch = random.sample(D, BUFFER_BATCH_SIZE)

			# Parse tupes for states, actions, rewards, and new_states
			states = np.array([e[0].flatten() for e in replay_batch])
			actions = np.array([e[1] for e in replay_batch])
			rewards = np.array([e[2] for e in replay_batch])
			new_states = np.array([e[3].flatten() for e in replay_batch])

			# Use the information from the replay_batch to predict the target value
			targets = reward + GAMMA * player.model.predict(new_states)

			# Train the Q network
			player.model.fit(states, targets)

		#print("action: " + str(action))
		#print("reward: " + str(reward))
		#print("State: ")
		#print(state)
		#print()

		t += 1 # increment timestep
		epsilon = epsilon * EPSILON_DECAY # Update Epsilon
		state = new_state # Update state

	#print("Score: " + str(game.score))
	scores.append(game.score)

print(scores)

"""
Next Steps:
Try a convolutional model
Tweak hyperparameters, learning rate, epsilon value, etc.
"""