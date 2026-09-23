
from fastapi import FastAPI
from pydantic import BaseModel


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
