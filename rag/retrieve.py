from pathlib import Path


POLICIES_DIR = Path(__file__).resolve().parent.parent /"policies"

def split_on_headings(text:str,source:str) -> list[dict]:
    chunks =[]
    current_heading = source
    current_lines =[]
    for line in text.splitlines():
        if line.startswith('#'):
            if current_lines:
                chunks.append(
                    {"source":source,"heading":current_heading,"text":"\n".join(current_lines).strip()}
                )
                current_heading = line.lstrip('#').strip()
                current_lines=[line]

        else:
            current_lines.append(line)
    if current_lines:
        chunks.append(
            {"source":source, "heading":current_heading, "text":"\n".join(current_lines).strip()}
        )
    return chunks

def load_chunks()->list[dict]:
    all_chunks = []
    for path in sorted(POLICIES_DIR.glob("*.md")):
        all_chunks.extend(split_on_headings(path.read_text(encoding="utf-8"),path.name))
    return all_chunks


def tokenize(text:str)-> set[str]:
    words =[]
    for raw in text.lower().split():
        word = "".join(ch for ch in raw if ch.isalnum())
        if word:
            words.append(word)
    return set(words)

def score_chunk(question:str, chunk:dict)-> int:
    q=tokenize(question)
    c=tokenize(chunk["text"])
    return len(q&c)

if __name__ == "__main__":
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
    hits = 0
    for question, expected in tests:
        ranked = sorted(chunks, key=lambda c: score_chunk(question, c), reverse=True)
        top3_files = [c["source"] for c in ranked[:3]]
        ok = expected in top3_files
        if ok:
            hits += 1
        print("HIT" if ok else "MISS", "|", expected, "|", top3_files, "|", question)
    print("hits:", hits, "of", len(tests)) 
