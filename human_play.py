from game import Game

# Define Constants
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

# Create game object (from game.py)
game = Game()

# Run the game until game over
while not game.gameOver:

    # Display the board
    game.display()

    # Prompt for user input
    choice = input("w, a, s, d, or q? ")

    # If user chooses left...
    if choice == "a":
        # Move left
        game.move(LEFT)

    # If user chooses right...
    elif choice == "d":
        # Move right
        game.move(RIGHT)

    # If user chooses up...
    elif choice == "w":
        # Move up
        game.move(UP)

    # If user chooses down...
    elif choice == "s":
        # Move down
        game.move(DOWN)

    # If user chooses to quit
    elif choice == "q":
        # Set gameOver to True
        game.gameOver = True

    # Otherwise...
    else:
        print("That wasn't a choice")

    # Check for game over sequence
    if game.gameOver:
        game.display()
        game.update_high_score()
        print("Game Over.")
        print()
