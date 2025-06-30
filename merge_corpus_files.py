import json
from pathlib import Path
from tqdm import tqdm

# List of input files in desired order
input_files = [
    "quran_corpus.jsonl",
    "hadith_corpus.jsonl",
    "fatwa_corpus.jsonl",
    "misc_fatwas_corpus.jsonl",
    "random_fatwas_corpus.jsonl",
    "zakat_corpus.jsonl"
]

# Output file
output_path = Path("corpus.jsonl")

# Merge all entries
merged = []
for file_name in input_files:
    file_path = Path(file_name)
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line.strip())
                    merged.append(item)
                except json.JSONDecodeError:
                    print(f"❌ Skipped invalid line in {file_name}")
    else:
        print(f"⚠️ File not found: {file_name}")

# Write to output
with output_path.open("w", encoding="utf-8") as f:
    for item in tqdm(merged, desc="Writing corpus"):
        json.dump(item, f)
        f.write("\n")

print("✅ All corpus files merged into corpus.jsonl")
