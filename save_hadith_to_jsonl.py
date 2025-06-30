import os
import json
from pathlib import Path
from tqdm import tqdm

# Directory containing hadith .txt files
HADITH_DIR = Path("data/hadith_txt")
OUTPUT_FILE = "hadith_corpus.jsonl"

def process_hadith_file(filepath):
    """Splits Hadith entries by line and formats them into JSONL entries."""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        raw_entries = text.split("Bukhari:")
        for raw in raw_entries:
            if not raw.strip():
                continue
            number, _, content = raw.partition(" ")
            entry = {
                "source": "hadith",
                "title": f"Sahih Bukhari {number.strip()}",
                "text": content.strip()
            }
            entries.append(entry)
    return entries

def main():
    all_entries = []
    for file in tqdm(sorted(HADITH_DIR.glob("*.txt")), desc="Processing Hadith Files"):
        entries = process_hadith_file(file)
        all_entries.extend(entries)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for entry in all_entries:
            out_f.write(json.dumps(entry) + "\n")

    print("✅ Done. Hadith corpus written to hadith_corpus.jsonl")

if __name__ == "__main__":
    main()
