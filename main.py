import os
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()


SYSTEM_PROMPT = (
    "you are Nothwind Banks assistant"
    "Answer only about Northwind's published topics"
    "Do not invent fees or rates"
    "if the user asks for a human, or the question is out of scope, offer a handoff"
)

class Turn(BaseModel):
    utterance:str

app = FastAPI()



@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/score-turn")
def score_turn(turn:Turn):
    text = turn.utterance.lower()
    if "lost my card" in text:
        return{"intent":"card_block"}
    return{"intent":"fallback"}

@app.post("/reply")
def reply(turn:Turn):
    client = genai.Client()
    prompt = SYSTEM_PROMPT + "\n\nUser: " +turn.utterance
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    print("PROMPT:",prompt)
    print("REPLY: ",response.text)
    return{"reply":response.text}