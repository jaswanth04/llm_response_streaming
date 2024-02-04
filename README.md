# Streaming a FineTuned LLM response with FastAPI

This repo contains information of how to stream the responses of a fine tune LLM, with the help of Fast API.

### Medium Articles

For information or a tutorial on how a streaming works, please go through the following articles:  
- [Streaming of Locally deployed model](https://medium.com/@jaswanth04/streaming-llm-responses-using-fastapi-deb575554397)
- [Streaming using Langchain](https://medium.com/stackademic/streaming-responses-from-llm-using-langchain-fastapi-329f588d3b40)
- [Contextualization using History](https://medium.com/@jaswanth04/history-based-contextualization-in-llm-deployed-as-a-backend-service-fastapi-and-5a1759fdd32e)

### Fast API streaming

Go to the file [src/fast_trial.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_trial.py) to understand, how streaming works in Fast API

### LLM streaming
Go to the file [src/fast_llm.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_llm.py) to understand, how streaming works in case of LLM and Fast API

### Langchain Streaming
Go to the file [src/fast_langchain.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_langchain.py) for streaming using langchain. OpenAI model was used in this. 
A custom handler was created in [src/handlers.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/handlers.py)

### History Streaming
Go the the file [src/fast_llm_history.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_llm_history.py) for history based retrieval. 
We are using Mongodb to store the history, for it to work, we need to start the mongo server. If you have installed a mongo server locally, you can bring that up by 

```
sudo systemctl start mongod
```

For anyone to use this, please get the proper url for the mongo connection, create the necessary collections and db and modify the [src/db_utils.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/db_utils.py) file accordingly.

### Running 

The following commands are to be run in command line

```
cd src

# For running trial
uvicorn fast_trial:app

# For running local llm streaming
uvicorn fast_llm:app

# For running Langchain Streaming
uvicorn fast_langchain:app

# For running History based Streaming
uvicorn fast_llm_history:app

```

### Testing
For testing please take a look at [src/stream_test.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/stream_test.py).

You can also take a look at the notebook [notebooks/stream_test.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/notebooks/stream_test.ipynb)

### Support

For any questions of support, please create an issue or mail to jaswanth04@gmail.com