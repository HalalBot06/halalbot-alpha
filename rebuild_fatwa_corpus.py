import json
from pathlib import Path
from tqdm import tqdm

INPUT_FILE = "fatwa_corpus.jsonl"
OUTPUT_FILE = "fatwa_corpus_rebuilt.jsonl"

def clean_text(text: str) -> str:
    return text.replace("\n", " ").replace("  ", " ").strip()

def rebuild_fatwa_corpus():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    valid_records = []

    for line in tqdm(lines, desc="Rebuilding fatwa corpus"):
        try:
            record = json.loads(line)
            question = clean_text(record.get("question", ""))
            answer = clean_text(record.get("answer", ""))

            if question and answer:
                text = f"Question: {question} Answer: {answer}"
                valid_records.append({
                    "text": text,
                    "source": "fatwa"
                })
        except Exception as e:
            continue

    with output_path.open("w", encoding="utf-8") as f:
        for record in valid_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ Rebuilt fatwa corpus written to {OUTPUT_FILE} with {len(valid_records)} valid entries.")

if __name__ == "__main__":
    rebuild_fatwa_corpus()
