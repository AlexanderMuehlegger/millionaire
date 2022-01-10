from flask import Flask, render_template, request, redirect
from flask_session import sessions
from game import game
from app import app

newApp = app(None)
newGame = game(newApp)

newApp.setGame(newGame)

newGame.createQuestionsArray(newGame.readFile())

app = Flask(__name__)

SESSION_TYPE = 'redis'

question = None


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    global question
    if request.method == 'POST':
        data = request.form["Transport"]

        if question == None:
            return "There was a Error"
        else:
            if question.rightAnswer + 1 == int(data):
                newGame.difficulty += 1
                print("Correct")
                return redirect("/")
            else:
                return redirect("/wrong")
        return "error has occured"
    elif request.method == 'GET':
        question = newGame.getRandomQuestion()
        data = [question.question, question.answers[0], question.answers[1], question.answers[2], question.answers[3],
                str(question.rightAnswer)]
        return render_template('index.html', data=data)

@app.route("/wrong")
def wrong():
    return render_template('wrong.html')

@app.route("/questions")
def questions():
    return render_template("questions.html")

if __name__ == "__main__":
    app.run(debug=True)