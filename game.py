"""
To Do:
Fix camelCase
* Combine move funtions by rotating the board
Write funtion disciptions
"""

import numpy as np
import os
import math

# Define Constants
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

class Game:

	def __init__(self):

		# Read in high score from file and initialize
		f = open("highscore.txt", "r")
		self.highscore = int(f.read())
		f.close()

		# Initialize current score as 0
		self.score = 0

		# Initialize the board with two random tiles
		self.board = np.zeros((4, 4), dtype=np.int)
		self.totalTiles = 0 # Incremented by add_tile
		self.add_tile()
		self.add_tile()

		# Use boolean to check if the game is over
		self.gameOver = False

	# Add a new tile to an empty cell of the board
	def add_tile(self):

		# Make a list of tuples of all the empty cells
		xVal, yVal = np.where(self.board == 0)
		emptyCells = list(zip(xVal,yVal))

		# Select one of these cells at random
		emptyCell = emptyCells[np.random.choice(len(emptyCells))]

		# Select a value of 2 or 4 with a ratio of 9:1
		tileVal = np.random.choice([2, 4], p=[0.9, 0.1])

		# Update the board
		self.board[emptyCell[0]][emptyCell[1]] = tileVal

		# Update totalTiles
		self.totalTiles += 1

		# Check if high score needs to be updated
		self.check_high_score()

		# Check for game over
		self.check_for_game_over()

	# Print the board and all other necessary information
	def display(self):

		# Clear the screen and print the score
		os.system('clear')
		print()
		print("Current Score: " + str(self.score))
		print("High Score: " + str(self.highscore))
		print()

		# Iterate through each tile and print accordingly
		for row in range(4):
			print(end="  ")
			for col in range(4):
				if self.board[row][col] == 0:
					print(end=".   ")
				elif int(math.log10(self.board[row][col])) == 0:
					print(self.board[row][col], end="   ")
				elif int(math.log10(self.board[row][col])) == 1:
					print(self.board[row][col], end="  ")
				elif int(math.log10(self.board[row][col])) == 2:
					print(self.board[row][col], end=" ")
				elif self.board[row][col] == 1024:
					print("1k", end="  ")
				elif self.board[row][col] == 2048:
					print("2k", end="  ")
				elif self.board[row][col] == 4096:
					print("4k", end="  ")
				else:
					print(self.board[row][col])
			print()
		print()

	# Implements slide logic by rotating the board as necessary, sliding left,
	# and rotating back. If the move is real, change the board of this object,
	# otherwise create a new state with the new board.
	def move(self, input_action, real = True):

		board = self.board
		score = self.score
		totalTiles = self.totalTiles

		# The logic slides left, so to slide up, for example, rotate counter-clockwise
		num_rotations = input_action
		board = np.rot90(board, num_rotations)

		# The cells changed counter makes sure we don't make moves where the
		# board does not change.
		cells_changed = 0

		# Store the original score to later determine how many points were earned
		# from this turn specifically.
		original_score = score

		# Iterate through each row to perform sliding logic
		for row in range(4):

			# As we move across the row, we will keep track of the value that
			# a tile "could be merged with".
			possible_merge_val = 0

			next_open_index = 0

			for col in range(4):
				currVal = board[row][col]

				# If the tile is not empty (i.e. curr_val is not 0), check if
				# merge logic is necessary.
				if currVal != 0:
					# If the value of the current column is the mergable value,
					# then merge.
					if currVal == possible_merge_val:
						# Change the left cell to be merged to 2 times itself
						board[row][next_open_index-1] = (currVal * 2)
						# Set the current cell to 0
						board[row][col] = 0
						# Update the score
						score += (currVal * 2)
						# Decrement the counter for total tiles on the board
						totalTiles -= 1
						# Increment the counter for cells changed
						cells_changed += 1
						# After we've merged, no more cells can merge with this
						possible_merge_val = 0
					# If the current tile is empty,
					else:
						# If there's an open spot somewhere to the left, slide.
						if next_open_index != col:
							# Put this tile in the leftmost open spot
							board[row][next_open_index] = currVal
							# Empty the current cell
							board[row][col] = 0
							# Increment the cell changed counter
							cells_changed += 1
						# Update the "mergable value"
						possible_merge_val = currVal
						# Update the next open index
						next_open_index += 1

		# Rotate the board back to its original orientation
		board = np.rot90(board, 4-num_rotations)

		if real:
			self.board = board
			self.score = score
			self.totalTiles = totalTiles

		# Add a new tile only if the board has changed
		if cells_changed != 0:
			self.add_tile()

		# Return the score_increase to help train the AI
		score_increase = self.score - original_score
		return score_increase

	def check_high_score(self):
		# If the score is greater than the high score...
		if self.score > self.highscore:
			# Update high score
			self.highscore = self.score

	def check_for_game_over(self):
		# If there are 16 non-zero tiles...
		if self.totalTiles == 16:
			# The game is over
			self.gameOver = True

	def update_high_score(self):
		# Write high score to file
		f = open("highscore.txt", "w")
		f.write(str(self.highscore))
		f.close()

	def reset(self):

		# Set score back to 0
		self.score = 0

		# Clear board and re-initilize with two random tiles
		self.board = np.zeros((4, 4), dtype=np.int)
		self.totalTiles = 0 # Incremented by add_tile
		self.add_tile()
		self.add_tile()

		self.gameOver = False
