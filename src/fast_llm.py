from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse
from load_model import load_model

from streamer import CustomStreamer
from threading import Thread

from queue import Queue


app = FastAPI()

model, tokenizer = load_model()
streamer_queue = Queue()
streamer = CustomStreamer(streamer_queue, tokenizer, True)

def start_generation(query):

    prompt = """

            # You are assistant that behaves very professionally. 
            # You will only provide the answer if you know the answer. If you do not know the answer, you will say I dont know. 

            # ###Human: {instruction},
            # ###Assistant: """.format(instruction=query)
    inputs = tokenizer([prompt], return_tensors="pt").to("cuda:0")
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=64, temperature=0.1)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()


async def response_generator(query):

    start_generation(query)

    while True:
        value = streamer_queue.get()
        if value == None:
            break
        yield value
        streamer_queue.task_done()
        await asyncio.sleep(0.1)
    

@app.get('/query-stream/')
async def stream(query: str):
    print(f'Query receieved: {query}')
    return StreamingResponse(response_generator(query), media_type='text/event-stream')