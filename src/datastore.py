import threading
from copy import deepcopy


lock = threading.Lock()


class Datastore:
    def __init__(self):
        self.students = {}
        self.exams = {}

    def add_batch(self, events):
        with lock:
            for event in events:
                self._add_event(event)

    def _add_event(self, event):
        """Takes an event and updates the students and exams dicts.
        We sacrifice normalization so that each API request causes
        a read, ie, no additional computation.

        This method is NOT threadsafe. Do not use directly!
        """

        student_id = event["studentId"]
        exam_id = event["exam"]
        score = event["score"]

        if student_id not in self.students:
            self.students[student_id] = {
                "results": [{"exam": exam_id, "score": score}],
                "average": score,
            }
        else:
            student = self.students[student_id]
            n_scores = len(student["results"])
            student["average"] = (student["average"] * n_scores + score) / (
                n_scores + 1
            )
            student["results"].append({"exam": exam_id, "score": score})

        if exam_id not in self.exams:
            self.exams[exam_id] = {
                "results": [{"studentId": student_id, "score": score}],
                "average": score,
            }
        else:
            exam = self.exams[exam_id]
            n_scores = len(exam["results"])
            exam["average"] = (exam["average"] * n_scores + score) / (n_scores + 1)
            exam["results"].append({"studentId": student_id, "score": score})

    def get_student(self, student_id):
        with lock:
            return deepcopy(self.students.get(student_id))

    def get_exam(self, exam_id):
        with lock:
            return deepcopy(self.exams.get(exam_id))

    @property
    def exam_ids(self):
        with lock:
            return list(self.exams)

    @property
    def student_ids(self):
        with lock:
            return list(self.students)


datastore = Datastore()

del Datastore
