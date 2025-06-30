import os
import json
import re
from tqdm import tqdm

FOLDER = "./data/random/txt"
OUTPUT_FILE = "misc_fatwas_corpus.jsonl"

def fix_spacing(text):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text.replace("\n", " ")).replace("  ", " ")

def extract_fatwa_from_text(text):
    question_match = re.search(r"(?:^|\n)Question:\s*(.+)", text, re.IGNORECASE)
    question = question_match.group(1).strip() if question_match else "Unknown question"
    answer_start = question_match.end() if question_match else 0
    answer = text[answer_start:].strip()
    answer = fix_spacing(answer)
    return {
        "question": question,
        "answer": answer,
        "source": "misc_fatwa"
    }

def main():
    fatwa_files = [f for f in os.listdir(FOLDER) if f.endswith(".txt")]
    results = []

    for filename in tqdm(fatwa_files, desc="Processing Misc Fatwas"):
        with open(os.path.join(FOLDER, filename), "r", encoding="utf-8") as f:
            raw = f.read()
            entry = extract_fatwa_from_text(raw)
            results.append(entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for item in results:
            json.dump(item, out, ensure_ascii=False)
            out.write("\n")

    print(f"✅ Done. Misc fatwas written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
