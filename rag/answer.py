import sys 
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer
from retrieve import load_chunks, cosine

load_dotenv()

THRESHOLD=0.40
MODEL_NAME = "all-MiniLM-L6-v2"

if len(sys.argv)<2:
    print("Usage: python rag/answer.py \"your question\"")
    sys.exit(1)
question = sys.argv[1]


chunks = load_chunks()
model = SentenceTransformer(MODEL_NAME)
chunk_vecs = model.encode([c["text"]for c in chunks])

q_vec = model.encode(question)
scored = [(cosine(q_vec,v),c) for v, c in zip(chunk_vecs,chunks)]
ranked = sorted(scored,key=lambda pair:pair[0],reverse= True)
best_score,best_chunk = ranked[0]
top3 = ranked[:3]

print("best_score:",best_score)
print("best_source:",best_chunk["source"])
print("top3:",[c["source"]for score,c in top3])




if best_score < THRESHOLD:
    print(
        "I don't have enough grounding in Northwind policies for that."
        "I can hand you off to a human."
    )
    sys.exit(0)


client = genai.Client()

sources_block = "\n\n".join(
    f"SOURCE file: {c['source']}\nHeading: {c['heading']}\n{c['text']}"
    for score, c in top3
)

prompt = (
    "you are Northwind Bank's assistant"
    "Answer only using the SOURCE text below"
    "do not invent fees or rates"
    "Name the source file in your answer"
    "if the source does not contain the answer, refuse and offer a handoff.\n\n"
    f"{sources_block}\n\n"
    f"User question:{question}"
)

response = client.models.generate_content(
    model = "gemini-3.6-flash",
    contents = prompt,
)

print(response.text)

