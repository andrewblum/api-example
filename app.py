import json
from collections import deque
import threading

import requests
from flask import Flask, jsonify

lock = threading.RLock()

events = deque()  # thread safe for push/pop on either side

students = {}
exams = {}

app = Flask(__name__)


def get_events(url):
    r = requests.get(url, stream=True)
    for line in r.iter_lines():
        if line.startswith(b"data:"):
            events.append(json.loads(line.decode()[6:]))


def process_events():
    while True:
        if events:
            new_events = []
            while events:
                new_events.append(events.popleft())

            with lock:
                for event in new_events:
                    student_id = event["studentId"]
                    exam = event["exam"]
                    score = event["score"]

                    if student_id not in students:
                        students[student_id] = {
                            "results": [{exam: score}],
                            "average": score,
                        }
                    else:
                        student = students[student_id]
                        n_scores = len(student["results"])
                        student["average"] = (student["average"] * n_scores + score) / (
                            n_scores + 1
                        )
                        student["results"].append({exam: score})


@app.route("/students")
def list_students():
    with lock:
        resp = jsonify(list(students))
    return resp


@app.route("/students/<student_id>")
def student_details(student_id):
    with lock:
        resp = jsonify(students[student_id])

    return resp


if __name__ == "__main__":
    t_fetch_events = threading.Thread(
        target=get_events, args=("http://live-test-scores.herokuapp.com/scores",)
    )
    t_process_vents = threading.Thread(target=process_events)

    t_fetch_events.start()
    t_process_vents.start()

    app.run(debug=True)
