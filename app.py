import os
import random
import sys

class questions:
    question = None
    rightAnswer = -1
    answers = None
    difficulty = None
    alreadyAsked = False

    def __init__(self, question, answers, difficulty):
        self.question = question
        self.answers = self.shuffleAnswers(answers)
        self.difficulty = difficulty

    def shuffleAnswers(self, answers):
        correctAnswer = answers[0]
        answers[len(answers)-1] = str(answers[len(answers)-1]).replace("\n", "")
        random.shuffle(answers)
        random.shuffle(answers)
        self.rightAnswer = answers.index(correctAnswer)
        return answers

    def __str__(self):
        print("Right Anwers Index: " + str(self.rightAnswer))
        return str(self.difficulty) + " " + str(self.question) + " " + str(self.answers) + " Correct Answer: " + str(self.answers[self.rightAnswer])

class game:
    questionsArray = []
    difficulty = 0
    def readFile(self):
        file = open("millionaire.txt")
        allLines = file.readlines()
        gameDifficulty = 0

        return allLines;

    def createQuestionsArray(self, singleLines):
        for x in singleLines:
            selectedQuestion = str(x).split("\t")
            answers = []
            answers.append(selectedQuestion[2])
            answers.append(selectedQuestion[3])
            answers.append(selectedQuestion[4])
            answers.append(selectedQuestion[5])
            print(selectedQuestion)
            self.questionsArray.append(questions(selectedQuestion[1], answers, selectedQuestion[0]))

    def getQuestion(self, index):
        if len(self.questionsArray) < 1:
            return;
        if index > len(self.questionsArray):
            return;
        return self.questionsArray[index]

    def setUpGame(self):
        setUpComplete = False

        while not setUpComplete:
            try:
                response = readInput("Which difficulty do you wish (0-5): ")
                try:
                    tempDiff = int(response)
                    if (tempDiff > 5):
                        raise ValueError("Out of Bounds!")
                    elif tempDiff > 0:
                        self.difficulty = tempDiff
                        setUpComplete = True
                except:
                    raise ValueError("Wrong input!")
            except:
                print("ERROR")

    def getRandomQuestion(self):
        listLenght = len(self.questionsArray)
        randomValue = None

        while (randomValue.__eq__(None) == True):
            if self.difficulty == 0:
                randomValue = random.randint(1, 41)
            elif self.difficulty == 1:
                randomValue = random.randint(42, 100)
            elif self.difficulty == 2:
                randomValue = random.randint(102, 167)
            elif self.difficulty == 3:
                randomValue = random.randint(169, 218)
            elif self.difficulty == 4:
                randomValue = random.randint(220, 232)
            else:
                randomValue = random.randint(1, listLenght - 1)
            if(self.questionsArray[randomValue].alreadyAsked == True):
                randomValue = None
            else:
                self.questionsArray[randomValue].alreadyAsked = False

        return self.questionsArray[randomValue]

    def printQuestionCorrectly(self, question):
        print(str(question.question))
        for x in question.answers:
            print("\t" + str(x) + "\t\t\t(%d)" % (question.answers.index(x)+1))

    def printInfo(self):
        print("You always can enter: ")
        print("exit\t\t For closing the game")
        print("info\t\t For getting this information")
        print("restart\t\t For restarting the whole game")
        print("change-d\t\t  For changing the difficulty of the game")
        print("toggle-q-v\t\t For Toggeling the Visibility of the Question's difficulty")
        print()

def readInput(msg):
    response = input(msg)
    match str(response).lower():
        case "exit":
            endGame()
            return -1
        case "info":
            printInfo()
            return -1
        case "restart":
            restartGame()
            return -1
        case "change-d":
            changeDifficulty()
            return -1
        case "toggle-q-v":
            changeDifficultyVisibility()
            return -1
        case _:
            print("hello")
            return response




newGame = game()
gameEnding = False
newGame.createQuestionsArray(newGame.readFile())
newGame.setUpGame()
newGame.printInfo()
thirstGame = True

while not gameEnding:
    response = ""
    if not thirstGame:
        readInput("Press Enter to Continue!")
    else:
        thirstGame = False

    currentQuestion = newGame.getRandomQuestion()
    newGame.printQuestionCorrectly(currentQuestion)
    while True:
        answerInput = readInput("Your Answer: ")
        try:
            answerInput = int(answerInput)

            if(answerInput > 4):
                raise ValueError("Out of Bounds")

            break
        except:
            print("Check Input! (1-4)")
    if(currentQuestion.rightAnswer == answerInput-1):
        print("Correct!")
    else:
        print("Wrong!")

def endGame():
    print("Thanks for playing!")
    os.abort()

def printInfo():
    print("info")

def restartGame():
    x = 0
    while(x < 10):
        print("\n")
        x += 1

    newGame = game()
    newGame.createQuestionsArray(newGame.readFile())
    newGame.setUpGame()

def changeDifficulty():
    print("change Difficulty")

def changeDifficultyVisibility():
    print("change Visibility of Difficulty")
