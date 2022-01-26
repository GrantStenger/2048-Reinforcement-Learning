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
    print("Possible inputs:")
    print("w, a, s, d")
    print("vim shortcuts")
    print("arrow keys")
    print("or q to quit")
    print()
    choice = input("Input: ")

    # If user chooses left...
    if choice in ["a", "^[[D", "h"]:
        # Move left
        game.move(LEFT)

    # If user chooses right...
    elif choice in ["d", "\x1b[D", "l"]:
        # Move right
        game.move(RIGHT)

    # If user chooses up...
    elif choice in ["w", "\x1b[A", "k"]:
        # Move up
        game.move(UP)

    # If user chooses down...
    elif choice in ["s", "\x1b[B", "j"]:
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
