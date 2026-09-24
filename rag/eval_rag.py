import csv
from pathlib import Path
from sentence_transformers import SentenceTransformer
from retrieve import load_chunks, cosine

THRESHOLD = 0.4
CSV_PATH = Path(__file__).resolve().parent.parent /"data"/"rag_eval.csv"

rows =[]
with CSV_PATH.open(encoding="utf=8",newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

chunks = load_chunks()
model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vecs = model.encode([c["text"]for c in chunks])

retrieval_hits = 0
retrieval_total = 0
refusal_correct = 0

for row in rows:
    question = row["question"]
    q_vec = model.encode(question)
    scored = [(cosine(q_vec, v), c) for v, c in zip(chunk_vecs, chunks)]
    ranked = sorted(scored, key=lambda pair: pair[0], reverse=True)
    best_score = ranked[0][0]
    top3_files = [c["source"] for score, c in ranked[:3]]

    predict_refuse = best_score < THRESHOLD

    should_answer = row["should_answer"].strip().lower()
    expect_refuse = should_answer == "no"
    if predict_refuse == expect_refuse:
        refusal_correct += 1

    if should_answer == "yes":
        retrieval_total += 1
        expected = row["expected_sources"].strip()
        if expected in top3_files:
            retrieval_hits += 1


print(
    f"retrieval_hit_rate: {retrieval_hits}/{retrieval_total} = "
    f"{retrieval_hits/retrieval_total:.2f}"
)

print(
    f"refusal_accuracy:{refusal_correct}/{len(rows)}="
    f"{refusal_correct/len(rows):.2f}"
)