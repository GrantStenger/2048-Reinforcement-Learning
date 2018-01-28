#Packages
import numpy as np
from game import Game
from collections import deque
import random
from player import Player

#Parameters Used
EPISODES = 1 # number of times the game is played
EPSILON = 1 # initial probability of doing a random move
EPSILON_DECAY = .99
NUM_ACTIONS = 4 # up, down, left, right
BUFFER_BATCH_SIZE = 10
highscore = 0

# Parameters Currently Unused
EPOCHS = 5 # initially set to 5 for fast training time
BATCH_SIZE = 32 
GAMMA = 0.9 # decay rate of past observations (try .98)
LEARNING_RATE = .0001


# Initialize replay memory D to capacity N
D = deque() # Where the actions will be stored

# Initialize action-value function with random weights

# Initialize the player and the game
player = Player()
game = Game(highscore)

# Play the game "EPISODES" number of times
for i in range(EPISODES):
	game.reset() # Start new game
	state = np.array(game.board, copy=True) # 4x4 np array containing tile information
	t = 0 # timestep value

	# Plays game until no more moves can be made
	while not game.gameOver:
		t += 1 # increment timestep

		# With probability epsilon, select a random action
		if np.random.rand() <= EPSILON:
			action = random.randrange(NUM_ACTIONS)
		# Otherwise, select the action with the highest predicted discounted future reward
		else:
			action = player.select_action(state)

		# Execute this action and observe reward r and new state
		reward = game.next_move(action)
		new_state = np.array(game.board, copy=True)

		# Store experience <s, a_t, r, s'> in replay memory D
		D.append((state, action, reward, new_state))

		# If there are enough items in the deque...
		if len(D) >= BUFFER_BATCH_SIZE:

			# Sample random transitions from replay memory D
			replay_batch = random.sample(D, BUFFER_BATCH_SIZE)

			states = np.array([e[0].flatten() for e in replay_batch])
			actions = np.array([e[1] for e in replay_batch])
			rewards = np.array([e[2] for e in replay_batch])
			new_states = np.array([e[3].flatten() for e in replay_batch])

			# Use the information from the replay_batch to predict the target value
			target = reward + np.amax(player.model.predict(new_states), axis=0)

			# Train the Q network using (tt - Q(ss, aa))^2 as loss
			

		print("action: " + str(action))
		print("reward: " + str(reward))
		print("State: ")
		print(state)
		print()

		EPSILON = EPSILON * EPSILON_DECAY
		state = new_state


	print("Score: " + str(game.score))

	"""
		# With probability epsilon, select a random action a_t
		

		# Otherwise:
			Given a state (s), score (R) every possible action a' (a1 …ai … an)
			using a function R = Q(s|a'), in terms of expected future reward R.

			select a_t as the action with the highest score

		Execute action a_t
		
		Observe reward r and new state s'

		Store experience <s, a_t, r, s'> in replay memory D
			( After every action, the current state (s'), the previous state (s),
			  the previous action (a), and the reward for the previous action (r)
			  is stored in what’s called an experience replay (a list). )

		sample random transitions <ss, aa, rr, ss’> from replay memory D

		calculate target tt for each minibatch transition
	        if ss’ is terminal state then tt = rr
	        otherwise tt = rr + γmaxa’Q(ss’, aa’)

	    train the Q network using (tt - Q(ss, aa))^2 as loss

	    s = s'

		if state.gameOver:
			alive = False
			#return game.highscore
	"""

	"""
	Assume the reward is received at time step T, just update all
	the previous time steps t1 … tn where tn = T with the same reward,
	however slightly discount the reward each time.

	Then train the Q function to predict the correct reward for the
	state at every time step.
	"""

