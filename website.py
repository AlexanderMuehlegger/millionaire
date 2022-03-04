import requests
import sqlite3
from flask import Flask, render_template, request, redirect, session, g
from flask_restful import Resource, Api
from sqlalchemy.orm import sessionmaker, scoped_session
from game import game
from app import app
import random
import string
from questions import Questions
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

engine = create_engine(r'sqlite:///C:\Users\alexa\PycharmProjects\millionaire\millionaire.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()


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

    def getJson(self):
        return{
            'id': self.id,
            'difficulty': self.difficulty,
            'question': self.question,
            'answers': [self.correct_answer, self.answer2, self.answer3, self.answer4]
        }


def get_questions_from_db():
    newGame.questionsArray = []
    questions = Millionaire.query.all()

    for x in questions:
        print(x.getJson())
        answers = [x.correct_answer, x.answer2, x.answer3, x.answer4]
        random.shuffle(answers)
        newGame.questionsArray.append(
            Questions(x.id, x.question, answers, x.difficulty, answers.index(x.correct_answer)))

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

@app.route("/")
def index():
    session['score'] = 0
    session['difficulty'] = 0
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
    get_questions_from_db()
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
        question = Millionaire.query.get(id)
        return question.getJson() if question!=None else {"Response" : "404: Frage mit ID: {} existiert nicht!".format(id)}

    def put(self, id):
        question = Questions(id, request.form["frage"], request.form.getlist("antworten"), int(request.form["difficulty"]), request.form["rightanswer"])
        exists = Millionaire.query.get(question.id)
        if not exists:
            question_answers = question.sort_answers()
            data = Millionaire(id=question.id, difficulty=question.difficulty, question=question.question, correct_answer=question_answers[0],
                                 answer2=question_answers[1], answer3=question_answers[2], answer4=question_answers[3])
            db_session.add(data)
            db_session.flush();
            app.logger.info("Frage mit ID: {} hinzugefügt!".format(id))
            get_questions_from_db()
            return {'Response' : '200: Frage mit ID: {} hinzugefügt!'.format(id)}
        return {'Response' : '500: Frage mit ID: {} konnte nicht hinzugefügt werden!'.format(id)}

    def delete(self, id):
        status = Millionaire.query.get(id)
        if not status:
            return {'Response' : '404: Frage mit ID: {} existiert nicht!'.format(id)}

        db_session.delete(status)
        db_session.flush()
        get_questions_from_db()
        return {'Response' : '200: Frage mit ID: {} wurde gelöscht!'.format(id)} if status else {'Response' : '500: Frage mit ID: {} konnte nicht gelöscht werden!'.format(id)}
    def patch(self, id):
        status = Millionaire.query.get(id)
        if not status:
            app.logger.error("Frage existiert nicht!")
            return {'Response' : '404: Frage mit ID: {} konnte nicht gefunden werden!'.format(id)}

        question = Questions(id, request.form["frage"], request.form.getlist("antworten"), int(request.form["difficulty"]), request.form["rightanswer"])

        question_answers = question.sort_answers()
        data = Millionaire(id=id, difficulty=question.difficulty, question=question.question,
                           correct_answer=question_answers[0],
                           answer2=question_answers[1], answer3=question_answers[2], answer4=question_answers[3])

        status.difficulty = data.difficulty
        status.question = data.question
        status.correct_answer = data.correct_answer
        status.answer2 = data.answer2
        status.answer3 = data.answer3
        status.answer4 = data.answer4

        db_session.add(status)
        db_session.flush();

        get_questions_from_db()

        return {'Response' : '200: Frage mit ID: {} wurde geändert!'.format(id)}

class All_questions(Resource):
    def get(self):
        questions = newGame.questionsArray
        response = []
        for q in questions:
            response.append(q.getJson())
        return {'Response' : response}

api.add_resource(QuestionSer, '/question/<int:id>')
api.add_resource(All_questions, '/allquestions')

@app.before_first_request
def initialize_server():
    get_questions_from_db()
    app.logger.info("Server successfully initiated")

if __name__ == "__main__":
    app.run(debug=True)