import urllib.request
import json


response = urllib.request.urlopen("https://jsonplaceholder.typicode.com/todos/1")
print(response.status)

body = json.loads(response.read())
print(body["title"])


