import numpy as np
import os
import math

class Game(object):

	def __init__(self):

		# Initialize score as 0
		self.score = 0

		# Initialize the board with two random tiles
		self.board = np.zeros((4, 4), dtype=np.int)
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

		# Check for game over
		self.check_for_game_over()


	def display(self):
		os.system('clear')
		print()
		print("Current Score: " + str(self.score))
		print("High Score: 10090")
		print()

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

	def slide_left(self):
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
						self.possibleMergeVal = (currVal * 2)
					else:
						if nextOpenIndex != col:
							# Slide to the left
							self.board[row][nextOpenIndex] = currVal
							self.board[row][col] = 0
						possibleMergeVal = currVal
						nextOpenIndex += 1
		self.add_tile()

	def slide_right(self):
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
						self.possibleMergeVal = (currVal * 2)
					else:
						if nextOpenIndex != col:
							# Slide to the right
							self.board[row][nextOpenIndex] = currVal
							self.board[row][col] = 0
						possibleMergeVal = currVal
						nextOpenIndex -= 1
		self.add_tile()

	def slide_up(self):
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
						self.possibleMergeVal = (currVal * 2)
					else:
						if nextOpenIndex != row:
							# Slide up
							self.board[nextOpenIndex][col] = currVal
							self.board[row][col] = 0
						possibleMergeVal = currVal
						nextOpenIndex += 1
		self.add_tile()

	def slide_down(self):
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
						self.possibleMergeVal = (currVal * 2)
					else:
						if nextOpenIndex != row:
							# Slide up
							self.board[nextOpenIndex][col] = currVal
							self.board[row][col] = 0
						possibleMergeVal = currVal
						nextOpenIndex -= 1
		self.add_tile()

	def check_for_game_over(self):

		# Update the list of empty cells
		xVal, yVal = np.where(self.board == 0)
		emptyCells = list(zip(xVal,yVal))

		# Check if the board is now full
		if len(emptyCells) == 0:
			# If full, the game is over
			self.gameOver = True






game = Game()

while not game.gameOver:
	
	game.display()
	print(int(math.log10(8)))

	choice = input("w, a, s, d, or q? ")
	if choice == "w":
		game.slide_up()
	elif choice == "a":
		game.slide_left()
	elif choice == "s":
		game.slide_down()
	elif choice == "d":
		game.slide_right()
	elif choice == "q":
		game.gameOver = True
	else:
		print("That wasn't a choice")

	if game.gameOver:
		game.display()
		print("Game Over.")
		print()