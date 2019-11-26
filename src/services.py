from collections import deque
import json
import threading
import requests

lock = threading.RLock()

events = deque()  # thread safe for push/pop on either side

students = {}
exams = {}


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
                    add_event(event)


def add_event(event, students=students, exams=exams):
    student_id = event["studentId"]
    exam_id = event["exam"]
    score = event["score"]

    if student_id not in students:
        students[student_id] = {"results": [{exam_id: score}], "average": score}
    else:
        student = students[student_id]
        n_scores = len(student["results"])
        student["average"] = (student["average"] * n_scores + score) / (n_scores + 1)
        student["results"].append({exam_id: score})

    if exam_id not in exams:
        exams[exam_id] = {"results": [{student_id: score}], "average": score}
    else:
        exam = exams[exam_id]
        n_scores = len(exam["results"])
        exam["average"] = (exam["average"] * n_scores + score) / (n_scores + 1)
        exam["results"].append({student_id: score})
