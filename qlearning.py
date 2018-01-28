""" Major improvements being made rn. Check in tomorrow. """

import argparse
import random
import numpy as np
from game import Game
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation

class Player(object):
	def __init__(self, ):
		self.model = self.buildModel()
		self.num_actions = 4 # number of valid actions

	def buildModel(self):

		# Initialize simple neural network model
		model = Sequential()

		# Hidden layer 1: 256 neurons, 'relu' activation
		model.add(Dense(units=256, input_dim=16))
		model.add(Activation('relu'))

		# Hidden layer 2: 256 neurons, 'relu' activation
		model.add(Dense(units=256))
		model.add(Activation('relu'))

		# Output layer: 4 neurons (one for each action), softmax activation
		model.add(Dense(units=4))
		model.add(Activation('softmax'))

		# Compile model
		model.compile(loss='mse',
			optimizer='adam',
			metrics=['accuracy'])
		
		return model

	def act(self, state):
		if np.random.rand() <= self.epsilon:
			return random.randrange(self.num_actions)
		act_values = self.model.predict(state)
		return np.argmax(act_values[0])

def Train():
	# Variables
	episodes = 100 # number of times the game is played
	gamma = 0.9 # decay rate of past observations (try .98)
	isFinished = False
	batch_size = 32
	learning_rate = .0001
	D = deque() # Register where the actions will be stored
	epsilon = 0.9 # Probability of doing a random move

	# Initialize player and build model
	agent = Player()
	model = agent.model

	# model.load_weights("model.h5")

	for e in range(epochs):
		game_state = Game(0).board
		state_vector = game_state.flatten() # Flattens board
		print(state_vector)
		prediction = model.predict(np.array([state_vector])) # Predicts best move 
		print(prediction)

	"""
    # Save trained model
    model.save_weights("model.h5", overwrite=True)
    with open("model.json", "w") as outfile:
        json.dump(model.to_json(), outfile)
    """

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='2048 QDL AI')
	parser.add_argument('-m','--mode', help='Train / Run', required=True)
	args = vars(parser.parse_args())
	if args['mode'] == "Train":
		Train()
	elif args['mode'] == "Run":
		Run() #Functionality coming soon
	else:
		print()
		print("Input takes form 'python qlearning.py -m Train' or 'python qlearning.py -m Run'")

# Initialize Q Matrix
# Choose an Action from Q
# Perform action
# Measure reward
# Update Q
# Repeat
