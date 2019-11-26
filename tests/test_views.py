import pytest
from src.views import app


@pytest.fixture
def client():
    c = app.test_client()
    yield c


def test_students(client):
    r = client.get("/students", follow_redirects=True)
    assert r.get_json() == []


def test_student_not_found(client):
    r = client.get("/students/not_such_student", follow_redirects=True)
    assert r.status_code == 404
    assert r.get_json() == {"error": "404 Not Found: student does not exist"}


def test_exams(client):
    r = client.get("/exams", follow_redirects=True)
    assert r.get_json() == []
