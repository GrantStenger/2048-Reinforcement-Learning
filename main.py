from game import Game


f = open("highscore.txt", "r")
highscore = f.read()
f.close()

game = Game(highscore)

while not game.gameOver:
    
    game.display()

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
        game.update_high_score()
        print("Game Over.")
        print()