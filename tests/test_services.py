from src.services import add_event


def test_add_event():
    students = {}
    exams = {}

    add_event(
        {"studentId": "Beth_Cronin", "exam": 10393, "score": 0.6878397196487688},
        students=students,
        exams=exams,
    )

    add_event(
        {"studentId": "Susana_Langworth", "exam": 10393, "score": 0.7499897269800325},
        students=students,
        exams=exams,
    )

    add_event(
        {"studentId": "Beth_Cronin", "exam": 11663, "score": 0.8561364166412366},
        students=students,
        exams=exams,
    )

    assert students
    assert exams
