import os
from game import game

class app:
    currentGame = None
    gameEnding = False
    thirstGame = True
    initialized = False

    def __init__(self, game):
        self.currentGame = game
        self.initialized = True

    def setGame(self, game):
        self.currentGame = game

    def startGame(self):
        while not self.gameEnding:
            if self.initialized and not self.currentGame is None:
                response = ""
                if not self.thirstGame:
                    self.readInput("Press Enter to Continue!", True)
                else:
                    self.thirstGame = False

                currentQuestion = self.currentGame.getRandomQuestion()
                self.currentGame.printQuestionCorrectly(currentQuestion)
                while True:
                    answerInput = self.readInput("Your Answer: ", True)
                    try:
                        answerInput = int(answerInput)

                        if (answerInput > 4):
                            raise ValueError("Out of Bounds")
                        if(answerInput == -2506):
                            raise RuntimeError
                        break
                    except:
                        if answerInput != -2506:
                            print("Check Input! (1-4)")

                if (currentQuestion.rightAnswer == answerInput - 1):
                    print("\nCorrect!\n")
                else:
                    print("\nWrong!\n")
            else:
                print("self.currentGame.__eq__(None)")

    def endGame(self):
        self.gameEnding = True
        print("Thanks for playing!")
        os.abort()


    def printInfo(self):
        print("\n")
        print("You always can enter: ")
        print("exit\t\t\tFor closing the game")
        print("info\t\t\tFor getting this information")
        print("change-d\t\tFor changing the difficulty of the game")
        print("toggle-q-v\t\tFor Toggeling the Visibility of the Question's difficulty")
        print("\n")

    def changeDifficulty(self):
        print("Enter 'cancle' to cancle")

        while True:
            wishedDifficulty = self.readInput("Which difficulty do you wish (0-5): ", False)
            try:
                wishedDifficulty = int(wishedDifficulty)

                if (wishedDifficulty > 5):
                    raise ValueError
                elif (wishedDifficulty < 0):
                    raise ValueError

                self.currentGame.setDifficulty(wishedDifficulty)

                print("Difficulty Changed!")
                break
            except:
                if (str(wishedDifficulty).lower() == "cancle"):
                    break
                raise ValueError

    def changeDifficultyVisibility(self):
        print("Enter 'cancle' to cancle\n")
        response = self.readInput("Enter True or False:", False)

        while True:
            try:
                if (str(response).lower() == "true"):
                    print("Visibility has been toggled on")
                    self.currentGame.setDifficultyVisibility(True)
                elif str(response).lower() == "false":
                    print("Visibility has been toggled off")
                    self.currentGame.setDifficultyVisibility(False)
                elif str(response).lower() == "cancle":
                    print("You cancled!")
                    break
                else:
                    raise ValueError
                break
            except:
                print("Check Input")

    def readInput(self, msg, readCommands):
        response = input(msg)

        if(bool(readCommands)):
           match str(response).lower():
               case "exit":
                   self.endGame()
                   return -2506
               case "info":
                   self.printInfo()
                   return -2506
               case "change-d":
                   self.changeDifficulty()
                   return -2506
               case "toggle-q-v":
                   self.changeDifficultyVisibility()
                   return -2506
               case _:
                   return response
        else:
            return response