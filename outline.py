#Packages
import numpy as np
from game import Game
from collections import deque
import random


#Parameters
epochs = 5 # initially set to 5 for fast training time
batch_size = 32 
episodes = 1 # number of times the game is played
gamma = 0.9 # decay rate of past observations (try .98)
learning_rate = .0001
epsilon = 0.9 # Probability of doing a random move
num_actions = 4 # up, down, left, right
highscore = 0


# Initialize replay memory D to capacity N
D = deque() # Where the actions will be stored

# Initialize action-value function with random weights

game = Game(highscore)

for i in range(episodes):
	game.reset() # Start new game
	state = game.board # 4x4 np array containing tile information
	t = 0 # timestep value

	while not game.gameOver:
		t += 1 # increment timestep
		print()
		# pick a random action
		rand_action = random.randrange(num_actions)
		print(rand_action)
		reward = game.next_move(rand_action) # Make next move and return reward
		print(state)
		print("Reward: " + str(reward))
		print("Timestep: " + str(t))

	print("Score: " + str(game.score))
	"""
		# With probability epsilon, select a random action a_t
		if np.random.rand() <= epsilon:
			return random.randrange(self.num_actions)

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
	"""
	"""
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



"""
Questions to Answer:

What do they mean by state? Is this the full game object? Just the board?
"""
