import random
import numpy as np
from game import Game
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation

class player:
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

		model.compile(loss='categorical_crossentropy',
			optimizer='rmsprop',
			metrics=['accuracy'])

		return model

	def act(self, state):
		if np.random.rand() <= self.epsilon:
			return random.randrange(self.num_actions)
		act_values = self.model.predict(state)
		return np.argmax(act_values[0])

""" main """
agent = player()
done = False
batch_size = 32
max_score = 0
best = []
episodes = 100

for e in range(episodes):
	frames = []
	state = Game(0)
	for time in range(500):
		action = agent.act(state)
