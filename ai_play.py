#Packages
import matplotlib.pyplot as plt
from collections import deque
from player import Player
from game import Game
import numpy as np
import scipy.stats
import random
import keras

#Parameters Used
EPISODES = 20000 # number of times the game is played
EPSILON_INIT = .99 # initial probability of doing a random move
EPSILON_DECAY = .999 # rate that epsilon decreases every move (if 0.999, after 700 moves epsilon=.5)
EPSILON_FINAL = 0.01 # to make sure the agent keeps exploring, minimum e of 0.01
BUFFER_BATCH_SIZE = 25 # number of states and targets sampled per training round

num_actions = 4 # up, down, left, right
highscore = 0 # Initial high score set to 0
epsilon = EPSILON_INIT # Set initial value of epsilon
scores = [] # Stores the final score of every game

# Initialize replay memory D where the actions will be stored
D = deque()

# Initialize the player and the game
player = Player()
game = Game(highscore)

# Play the game "EPISODES" number of times
for i in range(1, EPISODES):

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
			player.model.fit(states, targets, verbose=0)

		#print("action: " + str(action))
		#print("reward: " + str(reward))
		#print("State: ")
		#print(state)
		#print()

		t += 1 # increment timestep
		epsilon = EPSILON_INIT * EPSILON_DECAY**2 + EPSILON_FINAL # Update Epsilon
		state = new_state # Update state

	#print("Score: " + str(game.score))
	scores.append(game.score)

	# Display current training progress
	if i % 10 == 0:
		print(i)

# Plot Results
x_axis = np.arange(0, len(scores), 1)
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x_axis, scores)
print("Slope: ", slope)
print("Intercept: ", intercept)
print("R_value: ", r_value)
print("P_value: ", p_value)
print("Std_err: ", std_err)
plt.scatter(x_axis, scores, s=10)
plt.plot(x_axis, intercept + slope*x_axis, 'r', label='fitted line', alpha=0.4)
plt.title("Scores as Model Learns")
plt.ylabel('Score')
plt.xlabel('Episode')
plt.show()

print(scores)

"""
Next Steps:
Try a convolutional model
Tweak hyperparameters, learning rate, epsilon value, etc.
"""