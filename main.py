from game import game
from app import app

newApp = app(None)
newGame = game(newApp)

newApp.printInfo()

newApp.setGame(newGame)

newGame.createQuestionsArray(newGame.readFile())
newGame.setUpGame()
newApp.startGame()

newGame.printInfo()