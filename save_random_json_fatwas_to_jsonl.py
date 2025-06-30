import json
import os
from tqdm import tqdm

INPUT_DIR = "./data/random/json"
OUTPUT_FILE = "random_fatwas_corpus.jsonl"

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def main():
    output = []
    filenames = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    
    for fname in tqdm(filenames, desc="Processing Random Fatwas"):
        with open(os.path.join(INPUT_DIR, fname), "r", encoding="utf-8") as f:
            data = json.load(f)

        question = clean_text(data.get("question", ""))
        answer = clean_text(data.get("answer", ""))

        if not question or not answer:
            continue  # Skip if either is missing

        output.append({
            "source": "fatwa",
            "type": "random",
            "question": question,
            "answer": answer
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in output:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Done. Random fatwas written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
