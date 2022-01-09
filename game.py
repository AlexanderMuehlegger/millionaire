import random
from questions import questions

class game:
    questionsArray = []
    difficulty = 0
    currentApp = None
    difficultyIsVisible = True

    def __init__(self, app):
        self.currentApp = app

    def readFile(self):
        file = open("millionaire.txt")
        allLines = file.readlines()
        gameDifficulty = 0

        return allLines;

    def setDifficulty(self, dif):
        self.difficulty = dif
    def setDifficultyVisibility(self, vis):
        self.difficultyIsVisible = vis

    def createQuestionsArray(self, singleLines):
        for x in singleLines:
            selectedQuestion = str(x).split("\t")
            answers = []
            answers.append(selectedQuestion[2])
            answers.append(selectedQuestion[3])
            answers.append(selectedQuestion[4])
            answers.append(selectedQuestion[5])
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
            response = self.currentApp.readInput("Which difficulty do you wish (0-5): ", True)
            try:

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

        while randomValue is None:
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

        if(self.difficultyIsVisible):
            print("\n" + str(question.question) + "\t\tDifficulty: %s" % (question.difficulty))
        else:
            print("\b" + str(question.question))

        for x in question.answers:
            print("\t" + str(x) + "\t\t\t(%d)" % (question.answers.index(x)+1))

        print()
