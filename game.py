import numpy as np
import os
import math

class Game(object):

	def __init__(self, highscore):

		# Initialize high score
		self.highscore = int(highscore)

		# Initialize current score as 0
		self.score = 0

		# Initialize the board with two random tiles
		self.board = np.zeros((4, 4), dtype=np.int)
		self.totalTiles = 0 # Incremented by add_tile
		self.add_tile()
		self.add_tile()

		# Use boolean to check if the game is over
		self.gameOver = False

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

	def display(self):
		os.system('clear')
		print()
		print("Current Score: " + str(self.score))
		print("High Score: " + str(self.highscore))
		print()

		for row in range(4):
			print(end="  ")
			for col in range(4):
				if self.board[row][col] == 0:
					print(end=".   ")
				elif int(math.log10(self.board[row][col])) == 0: 
					print(self.board[row][col], end="   ")
					#print(Fore.RED + 'hi')
					#print(Fore.BLACK)
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

	def slide_left(self):
		cellsChanged = 0
		for row in range(4):
			possibleMergeVal = 0
			nextOpenIndex = 0
			for col in range(4):
				currVal = self.board[row][col]
				if currVal != 0:
					if currVal == possibleMergeVal:
						# Merge
						self.board[row][nextOpenIndex-1] = (currVal * 2)
						self.board[row][col] = 0
						possibleMergeVal = (currVal * 2)
						self.score += (currVal * 2)
						self.totalTiles -= 1
						cellsChanged += 1
					else:
						if nextOpenIndex != col:
							# Slide to the left
							self.board[row][nextOpenIndex] = currVal
							self.board[row][col] = 0
							cellsChanged += 1
						possibleMergeVal = currVal
						nextOpenIndex += 1
		if cellsChanged != 0:
			self.add_tile()

	def slide_right(self):
		cellsChanged = 0
		for row in range(4):
			possibleMergeVal = 0
			nextOpenIndex = 3
			for col in range(3, -1, -1):
				currVal = self.board[row][col]
				if currVal != 0:
					if currVal == possibleMergeVal:
						# Merge
						self.board[row][nextOpenIndex+1] = (currVal * 2)
						self.board[row][col] = 0
						possibleMergeVal = (currVal * 2)
						self.score += (currVal * 2)
						self.totalTiles -= 1
						cellsChanged += 1
					else:
						if nextOpenIndex != col:
							# Slide to the right
							self.board[row][nextOpenIndex] = currVal
							self.board[row][col] = 0
							cellsChanged += 1
						possibleMergeVal = currVal
						nextOpenIndex -= 1
		if cellsChanged != 0:
			self.add_tile()

	def slide_up(self):
		cellsChanged = 0
		for col in range(4):
			possibleMergeVal = 0
			nextOpenIndex = 0
			for row in range(4):
				currVal = self.board[row][col]
				if currVal != 0:
					if currVal == possibleMergeVal:
						# Merge
						self.board[nextOpenIndex-1][col] = (currVal * 2)
						self.board[row][col] = 0
						possibleMergeVal = (currVal * 2)
						self.score += (currVal * 2)
						self.totalTiles -= 1
						cellsChanged += 1
					else:
						if nextOpenIndex != row:
							# Slide up
							self.board[nextOpenIndex][col] = currVal
							self.board[row][col] = 0
							cellsChanged += 1
						possibleMergeVal = currVal
						nextOpenIndex += 1
		if cellsChanged != 0:
			self.add_tile()

	def slide_down(self):
		cellsChanged = 0
		for col in range(4):
			possibleMergeVal = 0
			nextOpenIndex = 3
			for row in range(3, -1, -1):
				currVal = self.board[row][col]
				if currVal != 0:
					if currVal == possibleMergeVal:
						# Merge
						self.board[nextOpenIndex+1][col] = (currVal * 2)
						self.board[row][col] = 0
						possibleMergeVal = (currVal * 2)
						self.score += (currVal * 2)
						self.totalTiles -= 1
						cellsChanged += 1
					else:
						if nextOpenIndex != row:
							# Slide up
							self.board[nextOpenIndex][col] = currVal
							self.board[row][col] = 0
							cellsChanged += 1
						possibleMergeVal = currVal
						nextOpenIndex -= 1
		if cellsChanged != 0:
			self.add_tile()

	def check_high_score(self):
		if self.score > self.highscore:
			self.highscore = self.score

	def check_for_game_over(self):
		if self.totalTiles == 16:
			self.gameOver = True

	def update_high_score(self):
		# Write high score to file
		f = open("highscore.txt", "w")
		f.write(str(self.highscore))
		f.close()