from flask import Flask, render_template, request, redirect
from game import game
from app import app

newApp = app(None)
newGame = game(newApp)

newApp.setGame(newGame)

newGame.createQuestionsArray(newGame.readFile())

app = Flask(__name__)


question = None
correctlyAnswered = 0


@app.route("/")
def index():
    reset()
    return render_template("index.html")

@app.route("/game", methods=['POST', 'GET'])
def game():
    global question
    global correctlyAnswered
    if request.method == 'POST':
        data = request.form["Transport"]

        if question == None:
            return "There was a Error"
        else:
            if question.rightAnswer + 1 == int(data):
                correctlyAnswered += 1
                if newGame.difficulty < 5 and correctlyAnswered % 2 == 0:
                    newGame.difficulty += 1
                return redirect("/game")
            else:
                print("WRONG")
                correctlyAnswered = 0
                return redirect("/wrong")
        return "error has occured"
    elif request.method == 'GET':
        difficulty = newGame.difficulty
        if difficulty >= 5:
            difficulty = "MAX"
        question = newGame.getRandomQuestion()
        data = [question.question, question.answers[0], question.answers[1], question.answers[2], question.answers[3],
                str(question.rightAnswer), difficulty]
        return render_template('game.html', data=data)

@app.route("/wrong")
def wrong():
    reset()
    return render_template('wrong.html')

@app.route("/questions")
def questions():
    return render_template("questions.html")

def reset():
    global question, correctlyAnswered
    newGame.difficulty = 0
    question = None
    correctlyAnswered = 0

if __name__ == "__main__":
    app.run(debug=True)