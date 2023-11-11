import requests
import time

url = "http://127.0.0.1:8000/query-stream/"

end = 1


with requests.get(url, stream=True) as r:
    for chunk in r.iter_content(1024):  # or, for line in r.iter_lines():
        # time.sleep(0.5)
        print(chunk)