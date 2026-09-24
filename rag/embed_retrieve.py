from sentence_transformers import SentenceTransformer
from retrieve import load_chunks,cosine

if __name__ == "__main__":
    tests = [
        ("How do I block a lost debit card?", "debit_card_block.md"),
        ("How many days to dispute a charge?", "dispute_window.md"),
        ("Why is there a monthly account fee on my statement?", "statement_charges.md"),
        ("What documents do I need for KYC?", "kyc_documents.md"),
        ("How do I reset my password?", "password_reset.md"),
        ("How long do international transfers take?", "international_transfers.md"),
        ("Where can I find the savings interest rate?", "savings_interest.md"),
        ("How do I book a branch appointment?", "branch_appointments.md"),
        ("Can I use another bank ATM for free?", "statement_charges.md"),
        ("What ID is accepted for identity verification?", "kyc_documents.md"),
    ]

    chunks = load_chunks()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_texts = [c["text"]for c in chunks]
    chunk_vecs = model.encode(chunk_texts)
hits = 0
for question, expected in tests:
    q_vec = model.encode(question)
    ranked = sorted(
        zip(chunks,chunk_vecs),
        key = lambda pair: cosine(q_vec,pair[1]),
        reverse= True
    )

    top3_files = [c["source"] for c, _ in ranked[:3]]
    ok = expected in top3_files
    if ok:
        hits+=1
    print("HIT" if ok else "MISS","|", expected,"|",top3_files,"|",question)
print("hits:",hits,"of",len(tests))