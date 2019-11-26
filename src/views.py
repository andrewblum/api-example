from flask import Flask, jsonify, abort
from src.services import lock, students, exams

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/students/")
def list_students():
    with lock:
        resp = jsonify(list(students))

    return resp


@app.route("/students/<student_id>")
def student_details(student_id):
    with lock:
        if student_id not in students:
            abort(404, description="student does not exist")

        resp = jsonify(students[student_id])

    return resp


@app.route("/exams/")
def list_exams():
    with lock:
        resp = jsonify(list(exams))

    return resp


@app.route("/exams/<int:exam_id>")
def exam_details(exam_id):
    with lock:
        if exam_id not in exams:
            abort(404, description="exam does not exist")

        resp = jsonify(exams[exam_id])

    return resp
