from fastapi import FastAPI, HTTPException
import asyncio
from fastapi.responses import StreamingResponse
from load_mistral import load_model

from streamer import CustomStreamer
from threading import Thread
from db_utils import MongoConnector, remove_inst_tags
from queue import Queue
from pydantic import BaseModel

class SessionRequest(BaseModel):
    session_id: str
    query: str

app = FastAPI()

model, tokenizer = load_model()
streamer_queue = Queue()
streamer = CustomStreamer(streamer_queue, tokenizer, True)
mongo_connector = MongoConnector()

def generate(session_id, messages):
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda:0")
    
    outputs = model.generate(inputs=inputs, streamer=streamer, 
                         pad_token_id=tokenizer.eos_token_id, 
                         max_new_tokens=512, 
                        #  temperature=0.1, do_sample=True
                         )

    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = remove_inst_tags(decoded_output)
    print('\n', '-'*15, 'Displaying Output', '-'*15, '\n')
    print(answer)
    print('\n', '-'*15, 'End of Display', '-'*15, '\n')

    question = messages[-1]["content"]
    mongo_connector.insert_record(session_id=session_id, question=question, answer=answer)

    

def start_generation(session_id, query):

    history = mongo_connector.retrieve_history(session_id)
    messages = None

    if not history:
        text = """You are an assistant that helps people in reminding what they are here for. 
                Please follow the below rules(1, 2, 3 and 4) for answering the questions:
                1. The people will given you information and if asked you will provide the information back to them.
                2. Please dont remind the user that you are here to remember information in the conversations.
                3. Only provide answer to the required question.
                4. Answer the question in less than 10 words.
                The input from the user is following:
                {question}""".format(question=query)

        messages = [{"role": "user", 
                    "content": text}]
    else:
        messages = []
        for previous_question, previous_answer in history:
            messages.append({
                "role": "user",
                "content": previous_question
            }) 
            messages.append({
                "role": "assistant",
                "content": previous_answer
            })
        messages.append({
            "role": "user",
            "content": query
        })
    if messages:
        thread = Thread(target=generate, kwargs=dict(session_id=session_id, 
                                                    messages=messages))
        thread.start()


async def response_generator(session_id: str, query: str) -> str:

    start_generation(session_id, query)

    while True:
        value = streamer_queue.get()
        if value == None:
            break
        yield value
        streamer_queue.task_done()
        await asyncio.sleep(0.1)
    

@app.post('/query-stream/')
async def stream(session_request: SessionRequest):
    print(f'Query receieved: {session_request.query}')
    if session_request.query is None:
        raise HTTPException(400, "Query is missing")
    return StreamingResponse(response_generator(session_request.session_id , 
                                                session_request.query), media_type='text/event-stream')