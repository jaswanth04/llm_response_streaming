from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse

from handlers import MyCustomHandler
from threading import Thread

from dotenv import load_dotenv
from queue import Queue
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage

load_dotenv()


app = FastAPI()

streamer_queue = Queue()
my_handler = MyCustomHandler(streamer_queue)

llm = ChatOpenAI(streaming=True, callbacks=[my_handler], temperature=0.7)

def generate(query):
    response = llm.invoke([HumanMessage(content=query)])
    print(response)

def start_generation(query):

    thread = Thread(target=generate, kwargs={"query": query})
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