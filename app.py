import threading
from flask import Flask, jsonify
from services import students, exams, get_events, process_events

lock = threading.RLock()

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


if __name__ == "__main__":
    t_fetch_events = threading.Thread(
        target=get_events, args=("http://live-test-scores.herokuapp.com/scores",)
    )
    t_process_vents = threading.Thread(target=process_events)

    t_fetch_events.start()
    t_process_vents.start()

    app.run(debug=True)
