import requests
import sqlite3
from flask import Flask, render_template, request, redirect, session, g
from flask_restful import Resource, Api
from game import game
from app import app
import random
import string
from questions import Questions
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

newApp = app(None)
newGame = game(newApp)

newApp.setGame(newGame)

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_letters) for i in range(25))

api = Api(app)

question = None
correctlyAnswered = 0

class Millionaire(Base):
    __tablename__ = 'millionaire'

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    question = Column(Text)
    correct_answer = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    answer4 = Column(Text)
    background_information = Column(Text)

def get_question():
    global question
    ques = newGame.getRandomQuestion()
    question = ques
    session['question'] = ques.question
    data = [
        {
            'frage': ques.question,
            'difficulty': ques.difficulty,
            'antwort1': ques.answers[0],
            'antwort2': ques.answers[1],
            'antwort3': ques.answers[2],
            'antwort4': ques.answers[3]
        }
    ]
    return data

DATABASE = './millionaire.sqlite3'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print("Connection established")
    return db

def executeDBQuerry():


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def startWebsite():
    db = get_db()
    cursor = db.cursor()
    query1 = "SELECT * FROM millionaire"
    result = cursor.execute(query1)
    newGame.createQuestionsArrayDB(result.fetchall())
    db.commit()

@app.route("/")
def index():
    if len(newGame.questionsArray) <= 0:
        startWebsite()
    session['score'] = 0
    session['difficulty'] = 0
    return render_template("index.html")

@app.route("/game", methods=['POST', 'GET'])
def game():
    if len(newGame.questionsArray) <= 0:
        startWebsite()
        print('GET')
    global question
    global correctlyAnswered
    if request.method == 'POST':
        data = request.form["Transport"]

        if question == None:
            return "There was a Error"
        else:
            if question.rightAnswer + 1 == int(data):
                correctlyAnswered += 1
                currentScore = session['score']
                currentScore += newGame.difficulty * 10
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

        session['difficulty'] = difficulty

        data = get_question()
        return render_template('game.html', data=data)

@app.route("/wrong")
def wrong():
    global correctlyAnswered
    newGame.difficulty = 0
    session['score'] = 0
    correctlyAnswered = 0
    return render_template('wrong.html')

@app.route("/questions")
def questions():
    q  = []
    thirst = True
    for x in newGame.questionsArray:
        if thirst:
            thirst = False
        else:
            q_temp = {"id": x.id, "level" : x.difficulty, "frage" : str(x.question), "answer1" : x.answers[0], "answer2" : x.answers[1], "answer3" : x.answers[2], "answer4" : x.answers[3]}
            q.append(q_temp)

    return render_template("questions.html", data = q)

class QuestionSer(Resource):
    def get(self, id):
        question = newGame.get_question_by_id(id)
        return question.getJson() if question!=None else {"Response" : "404: Frage mit ID: {} existiert nicht!".format(id)}

    def put(self, id):
        question = Questions(id, request.form["frage"], request.form.getlist("antworten"), int(request.form["difficulty"]), request.form["rightanswer"])

        executeDBQuerry();
        return {'Response' : '200: Frage mit ID: {} hinzugefügt!'.format(id)}

    def delete(self, id):
        status = newGame.delete_question(id)

        return {'Response' : '200: Frage mit ID: {} wurde gelöscht!'.format(id)} if status else {'Response' : '500: Frage mit ID: {} konnte nicht gelöscht werden!'.format(id)}
    def patch(self, id):
        question = Questions(id, request.form["frage"], request.form.getlist("antworten"), int(request.form["difficulty"]), request.form["rightanswer"])

        status = newGame.update_question(id, question)

        return {'Response' : '200: Frage mit ID: {} wurde geändert!'.format(id)} if status else {'Response' : '500: Frage mit ID: {} konnte nicht geändert werden!'.format(id)}

class All_questions(Resource):
    def get(self):
        questions = newGame.questionsArray
        response = []
        for q in questions:
            response.append(q.getJson())
        return {'Response' : response}

api.add_resource(QuestionSer, '/question/<int:id>')
api.add_resource(All_questions, '/allquestions')

if __name__ == "__main__":
    app.run(debug=True)