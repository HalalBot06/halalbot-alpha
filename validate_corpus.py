import json
from tqdm import tqdm

with open("corpus.jsonl", "r") as infile:
    records = [json.loads(line) for line in infile]

valid = []
invalid = []

for i, r in enumerate(tqdm(records, desc="Validating corpus")):
    if "text" in r and isinstance(r["text"], str) and r["text"].strip():
        valid.append(r)
    else:
        invalid.append((i, r))

with open("corpus_validated.jsonl", "w") as out:
    for r in valid:
        out.write(json.dumps(r) + "\n")

print(f"\n✅ Cleaned corpus written to corpus_validated.jsonl")
print(f"🟢 Valid entries: {len(valid)}")
print(f"🔴 Invalid/missing text entries: {len(invalid)}")
