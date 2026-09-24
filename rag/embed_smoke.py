from sentence_transformers import SentenceTransformer
from retrieve import load_chunks

chunks = load_chunks()
model = SentenceTransformer("all-MiniLM-L6-V2")
vec = model.encode(chunks[0]["text"])
print("chunks:",len(chunks))
print("first source:",chunks[0]["source"])
print("embedding length:",len(vec))
print("first 5 numbers:",vec[:5])
