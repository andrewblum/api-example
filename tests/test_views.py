import pytest
from src.views import app
from src import views


@pytest.fixture
def client():
    views.students = {
        "Alice": {
            "results": [{"exam": 3, "score": 0.9}, {"exam": 4, "score": 0.7}],
            "average": (0.7 + 0.9) / 2,
        },
        "Bob": {"results": [{"exam": 3, "score": 0.8}], "average": 0.8},
    }

    views.exams = {
        3: {
            "results": [
                {"studentId": "Alice", "score": 0.9},
                {"studentId": "Bob", "score": 0.8},
            ],
            "average": (0.8 + 0.9) / 2,
        },
        4: {"results": [{"studentId": "Alice", "score": 0.7}], "average": 0.7},
    }

    c = app.test_client()
    yield c

    views.students = {}
    views.exams = {}


def test_students(client):
    r = client.get("/students", follow_redirects=True)
    assert r.get_json() == {"studentIds": ["Alice", "Bob"]}


def test_student_detail(client):
    r = client.get("/students/Alice")
    assert r.get_json() == {
        "results": [{"exam": 3, "score": 0.9}, {"exam": 4, "score": 0.7}],
        "average": (0.7 + 0.9) / 2,
    }


def test_student_not_found(client):
    r = client.get("/students/not_such_student", follow_redirects=True)
    assert r.status_code == 404
    assert r.get_json() == {"error": "404 Not Found: student does not exist"}


def test_exams(client):
    r = client.get("/exams", follow_redirects=True)
    assert r.get_json() == {"examIds": [3, 4]}


def test_exam_detail(client):
    r = client.get("/exams/3")
    assert r.get_json() == {
        "results": [
            {"studentId": "Alice", "score": 0.9},
            {"studentId": "Bob", "score": 0.8},
        ],
        "average": (0.8 + 0.9) / 2,
    }


def test_exam_not_found(client):
    r = client.get("/exams/2", follow_redirects=True)
    assert r.status_code == 404
    assert r.get_json() == {"error": "404 Not Found: exam does not exist"}
