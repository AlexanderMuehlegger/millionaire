import random

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