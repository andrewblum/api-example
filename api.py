"""
The main module. It launches the threads to populate and process
the queue of events, and also starts the Flask server.
"""

import threading
from src.services import get_events, process_events, get_stream
from src.views import app


t_fetch_events = threading.Thread(target=get_events, args=(get_stream(),))
t_process_events = threading.Thread(target=process_events)

t_fetch_events.start()
t_process_events.start()


if __name__ == "__main__":

    app.run(host="0.0.0.0")
