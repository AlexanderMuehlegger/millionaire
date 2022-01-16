from flask import Flask, render_template, request, redirect
from flask_session import Session
from game import game
from app import app

newApp = app(None)
newGame = game(newApp)

newApp.setGame(newGame)

newGame.createQuestionsArray(newGame.readFile())

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

question = None
correctlyAnswered = 0

@app.route("/")
def index():

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
    q  = []
    thirst = True
    for x in newGame.questionsArray:
        if thirst:
            thirst = False
        else:
            q_temp = {"level" : x.difficulty, "frage" : str(x.question).replace(" ", ""), "answer1" : x.answers[0], "answer2" : x.answers[1], "answer3" : x.answers[2], "answer4" : x.answers[3]}
            q.append(q_temp)

    return render_template("questions.html", data = q)


if __name__ == "__main__":
    app.run(debug=True)