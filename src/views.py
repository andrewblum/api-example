"""
Our API endpoints are defined here as Flask views.
Each read from the students or exams data is
done under a lock, lest the data changes during the read.
"""


from flask import Flask, jsonify, abort

from src.datastore import datastore

app = Flask(__name__)  # the Flask application object


@app.errorhandler(404)
def resource_not_found(e):
    """Handler for when resource is not found."""
    return jsonify(error=str(e)), 404


@app.route("/students/")
def list_students():
    """Return list of students."""
    resp = jsonify(studentIds=datastore.student_ids)

    return resp


@app.route("/students/<student_id>")
def student_details(student_id):
    """Return scores and average of a student."""
    data = datastore.get_student(student_id)
    if data is None:
        abort(404, description="student does not exist")

    resp = jsonify(data)

    return resp


@app.route("/exams/")
def list_exams():
    """Returns list of exams."""
    resp = jsonify(examIds=datastore.exam_ids)

    return resp


@app.route("/exams/<int:exam_id>")
def exam_details(exam_id):
    """Returns scores and average of an exam."""
    data = datastore.get_exam(exam_id)
    if data is None:
        abort(404, description="exam does not exist")

    resp = jsonify(data)

    return resp
