import argparse
import random
import numpy as np
from game import Game
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation

class Player(object):
	def __init__(self):
		self.model = self.build_model()
		self.num_actions = 4 # number of valid actions

	def build_model(self):

		# Initialize simple neural network model
		model = Sequential()

		# Hidden layer 1: 256 neurons, 'relu' activation
		model.add(Dense(units=256, input_dim=16))
		model.add(Activation('relu'))

		# Hidden layer 2: 256 neurons, 'relu' activation
		model.add(Dense(units=256))
		model.add(Activation('relu'))

		# Output layer: 4 neurons (one for each action), consider going back to softmax activation
		model.add(Dense(units=4))
		model.add(Activation('softmax'))

		# Compile model
		model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

		return model

	def q_predict(self, state):
		return self.model.predict(np.array([state.flatten()]))[0]

	def select_action(self, state):
		# Consider the policy where you act stochastically in accordance to the softmax output
		return np.argmax(self.q_predict(state))

