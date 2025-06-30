import json
from pathlib import Path
from tqdm import tqdm

# Path to your original fatwa_corpus.jsonl
INPUT_FILE = Path("fatwa_corpus.jsonl")
OUTPUT_FILE = Path("fatwa_corpus_patched.jsonl")

def patch_fatwa_source():
    with INPUT_FILE.open("r", encoding="utf-8") as infile, OUTPUT_FILE.open("w", encoding="utf-8") as outfile:
        for line in tqdm(infile, desc="Patching fatwa corpus"):
            entry = json.loads(line)
            # Set source if missing or blank
            if "source" not in entry or not entry["source"].strip():
                entry["source"] = "fatwa"
            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print("✅ Patched corpus written to", OUTPUT_FILE)

if __name__ == "__main__":
    patch_fatwa_source()
