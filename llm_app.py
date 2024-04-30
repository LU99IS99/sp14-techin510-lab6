import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyAAJXpN2TlfW3ekgyBVGW9Y3JE4v8TaKlk"

data = {
    "contents":[
        {
            "parts":[
                {"text":"Write a story about a magic backpack in chinese"}
            ]
        }
                ]

}

res = requests.post(
    URL,
    headers={
        "content-type": "application/json",
    },
    json=data,
    params={"key":os.getenv("GOOGLE_API_KEY")}
)
json_res = res.json()
print(json_res)
