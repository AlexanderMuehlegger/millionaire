import sqlite3
from flask import g, Flask


app = Flask(__name__)

def addNew(connection, question):
    curser = connection.cursor()
    query = "INSERT INTO millionaire({}, {}, {}, {})".format(question.id, question.difficulty, question.question, question.right_answer,  )


