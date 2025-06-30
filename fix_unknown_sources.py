import json
from tqdm import tqdm

input_file = "corpus.jsonl"
output_file = "corpus_cleaned.jsonl"

def detect_fatwa_text(text):
    return "mufti" in text.lower() or "question" in text.lower()

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in tqdm(infile, desc="🔍 Scanning entries"):
        try:
            entry = json.loads(line)
            source = entry.get("source", "").lower()

            # Case: missing or bad source
            if not source or source.endswith(".txt") or "unknown" in source:
                if detect_fatwa_text(entry.get("text", "")):
                    entry["source"] = "fatwa"
                else:
                    entry["source"] = "misc"

            # Normalize source (e.g., fix file-based names)
            if source.endswith(".txt"):
                entry["source"] = source.replace(".txt", "").lower()

            outfile.write(json.dumps(entry) + "\n")
        except json.JSONDecodeError:
            continue  # skip bad lines

print(f"\n✅ Cleaned corpus written to {output_file}")
