import threading
from collections import deque
from src.services import get_events, process_events
from src.datastore import datastore

Datastore = type(datastore)


def test_get_events(mocker):
    """Fetching of events from stream and populating queue."""

    events = mocker.patch("src.services.events", new=deque())

    get_events(
        [
            b"",
            b"event: score",
            b'data: {"studentId":"Susana_Langworth","exam":13857,"score":0.8310771952183729}',
        ]
    )

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

    datastore = mocker.patch("src.services.datastore", new=Datastore())

    process_events(testing=True)

    assert datastore.students == {
        "Susana_Langworth": {
            "average": 0.8310771952183729,
            "results": [{"exam": 13857, "score": 0.8310771952183729}],
        }
    }
    assert datastore.exams == {
        13857: {
            "average": 0.8310771952183729,
            "results": [{"score": 0.8310771952183729, "studentId": "Susana_Langworth"}],
        }
    }


def test_add_event():
    """Adding of individual events from queue to exams / students."""

    datastore = Datastore()

    datastore.add_event({"studentId": "Alice", "exam": 3, "score": 0.9})

    datastore.add_event({"studentId": "Bob", "exam": 3, "score": 0.8})

    datastore.add_event({"studentId": "Alice", "exam": 4, "score": 0.7})

    assert datastore.students == {
        "Alice": {
            "results": [{"exam": 3, "score": 0.9}, {"exam": 4, "score": 0.7}],
            "average": (0.7 + 0.9) / 2,
        },
        "Bob": {"results": [{"exam": 3, "score": 0.8}], "average": 0.8},
    }
    assert datastore.exams == {
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

    mocker.patch("src.services.events", new=deque())

    datastore = mocker.patch("src.services.datastore", new=Datastore())

    t_fetch_events = threading.Thread(
        target=get_events,
        args=(
            [
                b"",
                b"event: score",
                b'data: {"studentId":"Susana_Langworth","exam":13857,"score":0.8310771952183729}',
            ],
        ),
    )
    t_process_events = threading.Thread(target=process_events, kwargs={"testing": True})

    t_fetch_events.start()
    t_process_events.start()

    t_fetch_events.join()
    t_process_events.join()

    assert datastore.students == {
        "Susana_Langworth": {
            "average": 0.8310771952183729,
            "results": [{"exam": 13857, "score": 0.8310771952183729}],
        }
    }
    assert datastore.exams == {
        13857: {
            "average": 0.8310771952183729,
            "results": [{"score": 0.8310771952183729, "studentId": "Susana_Langworth"}],
        }
    }
