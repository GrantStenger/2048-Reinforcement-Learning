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

    # Check for and perform game over sequence
    if game.gameOver:
        game.display()
        game.update_high_score()
        print("Game Over.")
        print()
