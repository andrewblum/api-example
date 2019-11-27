"""
Procedures to consume the events and update the data that our API returns.

We use a queue to hold the events in order to separate and simplify the ingestion
and the processing. For example, since the events come in bursts, we can process
them in batches.

"""

from collections import deque
import json
import threading
import requests

EVENTS_URL = "http://live-test-scores.herokuapp.com/scores"

lock = threading.Lock()

# thread safe for push/pop on either side
# https://docs.python.org/3/library/collections.html#collections.deque
events = deque()


# These two dictionaries play the role of a datastore.
students = {}
exams = {}


stream = requests.get(EVENTS_URL, stream=True).iter_lines()


def get_events():
    """Consume events from the events stream and add to deque."""
    for line in stream:
        if line.startswith(b"data:"):
            events.append(json.loads(line.decode()[6:]))


def process_events(testing=False):
    """Processes and clears items from deque and updates students and exams."""
    while True:
        if events:
            new_events = []
            while events:
                new_events.append(events.popleft())

            with lock:
                for event in new_events:
                    add_event(event)

            if testing:  # need to allow test to finish
                break


def add_event(event):
    """Takes an event and updates the students and exams dicts.
    We sacrifice normalization so that each API request causes
    a read, ie, no additional computation."""

    student_id = event["studentId"]
    exam_id = event["exam"]
    score = event["score"]

    if student_id not in students:
        students[student_id] = {
            "results": [{"exam": exam_id, "score": score}],
            "average": score,
        }
    else:
        student = students[student_id]
        n_scores = len(student["results"])
        student["average"] = (student["average"] * n_scores + score) / (n_scores + 1)
        student["results"].append({"exam": exam_id, "score": score})

    if exam_id not in exams:
        exams[exam_id] = {
            "results": [{"studentId": student_id, "score": score}],
            "average": score,
        }
    else:
        exam = exams[exam_id]
        n_scores = len(exam["results"])
        exam["average"] = (exam["average"] * n_scores + score) / (n_scores + 1)
        exam["results"].append({"studentId": student_id, "score": score})
