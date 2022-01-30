import random

class Questions:
    question = None
    rightAnswer = -1
    answers = None
    difficulty = None
    alreadyAsked = False
    id = -1

    def __init__(self, id, question, answers, difficulty, rightanswer):
        self.question = question
        if rightanswer == -1:
            self.answers = self.shuffleAnswers(answers)
        else:
            self.answers = answers
            self.rightAnswer = rightanswer
        self.difficulty = difficulty
        self.id = id


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

    def getJson(self):
        return{
            'id': self.id,
            'difficulty': self.difficulty,
            'question': self.question,
            'answers': self.answers,
            'rightanswer': self.rightAnswer
        }