from flask import Flask, render_template, request, redirect
from game import game
from app import app

newApp = app(None)
newGame = game(newApp)

newApp.setGame(newGame)

newGame.createQuestionsArray(newGame.readFile())

app = Flask(__name__)

question = None

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return "HELLO"
    elif request.method == 'GET':
        question = newGame.getRandomQuestion()
        data = [question.question, question.answers[0], question.answers[1], question.answers[2], question.answers[3], str(question.rightAnswer)]
        return render_template('index.html', data=data)

@app.route('/check/<string:id>')
def check():
    id = int(id)
    if question == None:
        return redirect("/")
    elif question.rightAnswer+1 == id:
        print("hello")
        return "Correct"
    else:
        return "WRONG"


if __name__ == "__main__":
    app.run(debug=True)