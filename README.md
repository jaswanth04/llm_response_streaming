# Streaming a FineTuned LLM response with FastAPI

This repo contains information of how to stream the responses of a fine tune LLM, with the help of Fast API.

### Medium Articles

For information or a tutorial on how a streaming works, please go through the following articles:  
- [Streaming of Locally deployed model](https://medium.com/@jaswanth04/streaming-llm-responses-using-fastapi-deb575554397)
- [Streaming using Langchain](https://medium.com/stackademic/streaming-responses-from-llm-using-langchain-fastapi-329f588d3b40)

### Fast API streaming

Go to the file [src/fast_trial.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_trial.py) to understand, how streaming works in Fast API

### LLM streaming
Go to the file [src/fast_llm.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_llm.py) to understand, how streaming works in case of LLM and Fast API

### Langchain Streaming
Go to the file [src/fast_langchain.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/fast_langchain.py) for streaming using langchain. OpenAI model was used in this. 
A custom handler was created in [src/handlers.py](https://github.com/jaswanth04/llm_response_streaming/blob/main/src/handlers.py)

### History Streaming
Go the the file 

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