from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse
import time
from threading import Thread

from queue import Queue


app = FastAPI()

some_i = 30

streamer_queue = Queue()

def put_data():
    global some_i
    for i in range(20):
        streamer_queue.put(some_i + i)
        
def start_generation():
    thread = Thread(target=put_data)
    time.sleep(0.5)
    thread.start()


async def serve_data():

    start_generation()

    while True:
        if streamer_queue.empty():
            break
        else:
            value = streamer_queue.get()
            yield str(value)
            streamer_queue.task_done()
        await asyncio.sleep(2)


@app.get('/put-item/')
async def add_item(item: int):
    streamer_queue.put(item)
    return True

@app.get('/query-stream/')
async def stream():
    return StreamingResponse(serve_data(), media_type='text/event-stream')