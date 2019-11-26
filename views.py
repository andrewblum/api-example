from flask import Flask, jsonify
from services import lock, students, exams

app = Flask(__name__)


@app.route("/students/")
def list_students():
    with lock:
        resp = jsonify(list(students))
    return resp


@app.route("/students/<student_id>")
def student_details(student_id):
    with lock:
        resp = jsonify(students[student_id])

    return resp
