import threading
from collections import deque
from src.services import add_event, get_events, process_events


def test_get_events(mocker):
    """Fetching of events from stream and populating queue."""

    mocker.patch(
        "src.services.stream",
        new=[
            b"",
            b"event: score",
            b'data: {"studentId":"Susana_Langworth","exam":13857,"score":0.8310771952183729}',
        ],
    )
    events = mocker.patch("src.services.events", new=deque())

    get_events()

    assert events == deque(
        [{"studentId": "Susana_Langworth", "exam": 13857, "score": 0.8310771952183729}]
    )


def test_process_events(mocker):
    """Emptying queue and updating students and exams."""

    mocker.patch(
        "src.services.events",
        new=deque(
            [
                {
                    "studentId": "Susana_Langworth",
                    "exam": 13857,
                    "score": 0.8310771952183729,
                }
            ]
        ),
    )
    students = mocker.patch("src.services.students", new={})
    exams = mocker.patch("src.services.exams", new={})

    process_events(testing=True)

    assert students == {
        "Susana_Langworth": {
            "average": 0.8310771952183729,
            "results": [{"exam": 13857, "score": 0.8310771952183729}],
        }
    }
    assert exams == {
        13857: {
            "average": 0.8310771952183729,
            "results": [{"score": 0.8310771952183729, "studentId": "Susana_Langworth"}],
        }
    }


def test_add_event(mocker):
    """Adding of individual events from queue to exams / students."""

    students = mocker.patch("src.services.students", new={})
    exams = mocker.patch("src.services.exams", new={})

    add_event({"studentId": "Alice", "exam": 3, "score": 0.9})

    add_event({"studentId": "Bob", "exam": 3, "score": 0.8})

    add_event({"studentId": "Alice", "exam": 4, "score": 0.7})

    assert students == {
        "Alice": {
            "results": [{"exam": 3, "score": 0.9}, {"exam": 4, "score": 0.7}],
            "average": (0.7 + 0.9) / 2,
        },
        "Bob": {"results": [{"exam": 3, "score": 0.8}], "average": 0.8},
    }
    assert exams == {
        3: {
            "results": [
                {"studentId": "Alice", "score": 0.9},
                {"studentId": "Bob", "score": 0.8},
            ],
            "average": (0.8 + 0.9) / 2,
        },
        4: {"results": [{"studentId": "Alice", "score": 0.7}], "average": 0.7},
    }


def test_threads(mocker):
    """Integration test of the ingestion and processing threads."""

    mocker.patch(
        "src.services.stream",
        new=[
            b"",
            b"event: score",
            b'data: {"studentId":"Susana_Langworth","exam":13857,"score":0.8310771952183729}',
        ],
    )

    mocker.patch("src.services.events", new=deque())

    students = mocker.patch("src.services.students", new={})
    exams = mocker.patch("src.services.exams", new={})

    t_fetch_events = threading.Thread(target=get_events)
    t_process_events = threading.Thread(target=process_events, kwargs={"testing": True})

    t_fetch_events.start()
    t_process_events.start()

    t_fetch_events.join()
    t_process_events.join()

    assert students == {
        "Susana_Langworth": {
            "average": 0.8310771952183729,
            "results": [{"exam": 13857, "score": 0.8310771952183729}],
        }
    }
    assert exams == {
        13857: {
            "average": 0.8310771952183729,
            "results": [{"score": 0.8310771952183729, "studentId": "Susana_Langworth"}],
        }
    }
