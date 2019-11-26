"""
Our API endpoints are defined here as Flask views.
Each read from the students or exams data is
done under a lock, lest the data changes during the read.
"""


from flask import Flask, jsonify, abort
from src.services import lock, students, exams

app = Flask(__name__)  # the Flask application object


@app.errorhandler(404)
def resource_not_found(e):
    """Handler for when resource is not found."""
    return jsonify(error=str(e)), 404


@app.route("/students/")
def list_students():
    """Return list of students."""
    with lock:
        resp = jsonify(list(students))

    return resp


@app.route("/students/<student_id>")
def student_details(student_id):
    """Return scores and average of a student."""
    with lock:
        if student_id not in students:
            abort(404, description="student does not exist")

        resp = jsonify(students[student_id])

    return resp


@app.route("/exams/")
def list_exams():
    """Returns list of exams."""
    with lock:
        resp = jsonify(list(exams))

    return resp


@app.route("/exams/<int:exam_id>")
def exam_details(exam_id):
    """Returns scores and average of an exam."""
    with lock:
        if exam_id not in exams:
            abort(404, description="exam does not exist")

        resp = jsonify(exams[exam_id])

    return resp
