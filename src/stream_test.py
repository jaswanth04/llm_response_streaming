import requests
import time


url = "http://127.0.0.1:8000/query-stream/?query=Write a short story?"
# url = "http://127.0.0.1:8000/query-stream/"




with requests.get(url, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk.decode("utf-8"), sep="")