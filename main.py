from game import Game

# Read in high score from file
f = open("highscore.txt", "r")
highscore = f.read()
f.close()

# Create game object (from game.py)
game = Game(highscore)

# Run the game until game over
while not game.gameOver:

    # Display the board
    game.display()

    # Prompt for user input
    choice = input("w, a, s, d, or q? ")

    # If user chooses left...
    if choice == "a":
        # Move left
        game.next_move(0)

    # If user chooses right...
    elif choice == "d":
        # Move right
        game.next_move(1)

    # If user chooses up...
    elif choice == "w":
        # Move up
        game.next_move(2)

    # If user chooses down...
    elif choice == "s":
        # Move down
        game.next_move(3)

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