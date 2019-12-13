from sanic import Sanic
from sanic.response import json
import asyncio
import httpx
from collections import deque
from json import loads

app = Sanic()


EVENTS_URL = "http://live-test-scores.herokuapp.com/scores"

events = deque()


async def get_events():
    """Consume events from the events stream and add to deque."""
    r = await httpx.get(EVENTS_URL)
    async for line in r.stream():
        print(line)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_events())
    # app.add_task(get_events())
    print("added")
    # app.run(host="0.0.0.0", port=8000)

    print("done")
