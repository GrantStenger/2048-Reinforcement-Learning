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
		self.num_actions = 4
		self.epsilon = 1.0

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

		print("Finished building the model")
		return model

	def trainNetwork(self, model, args):



		# Initialize game state to communicate with emulator
		game_state = Game(0)

		# Store previous observations in replay memory
		D = deque()

		# Get information about the first state
		x_t = game_state.board
		r_0 = 0
		isFinished = False

		if args["mode"] == "Run":
			# Run program
			print("Load weights")
			model.load_weights("model.h5")
			adam = Adam(lr=LEARNING_RATE)
		#else:

	def act(self, state):
		if np.random.rand() <= self.epsilon:
			return random.randrange(self.num_actions)
		act_values = self.model.predict(state)
		return np.argmax(act_values[0])

def playGame(args):
	actions = 4 # number of valid actions
	GAMMA = 0.98 # decay rate of past observations
	done = False
	BATCH_SIZE = 32
	LEARNING_RATE = .0001

	player = Player()
	model = player.model
	player.trainNetwork(model, args)

def main():
	parser = argparse.ArgumentParser(description='2048 QDL AI')
	parser.add_argument('-m','--mode', help='Train / Run', required=True)
	args = vars(parser.parse_args())
	print(args)
	playGame(args)

if __name__ == "__main__":
	main()









""" main """ 
"""
agent = player()
actions = 4 # number of valid actions
gamma = 0.98 # decay rate of past observations
done = False
batch_size = 32
learning_rate = .0001
max_score = 0
best = []
episodes = 100

for e in range(episodes):
	frames = []
	state = Game(0)
	for time in range(500):
		action = agent.act(state)


# Initialize Q Matrix
# Choose an Action from Q
# Perform action
# Measure reward
# Update Q
# Repeat


"""
