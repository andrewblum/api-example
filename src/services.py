"""
Procedures to consume the events and update the data that our API returns.

We use a queue to hold the events in order to separate and simplify the ingestion
and the processing. For example, since the events come in bursts, we can process
them in batches.

"""

from collections import deque
import json

import requests
from src.datastore import datastore

EVENTS_URL = "http://live-test-scores.herokuapp.com/scores"


# thread safe for push/pop on either side
# https://docs.python.org/3/library/collections.html#collections.deque
events = deque()


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

            datastore.add_batch(new_events)

            if testing:  # need to allow test to finish
                break
