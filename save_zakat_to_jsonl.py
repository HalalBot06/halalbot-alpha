# save_zakat_to_jsonl.py

import json

input_path = "./data/zakat_rsb_chunks.json"
output_path = "zakat_corpus.jsonl"

with open(input_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open(output_path, "w", encoding="utf-8") as out:
    for entry in chunks:
        json.dump(entry, out)
        out.write("\n")

print("✅ Done. Zakat corpus written to zakat_corpus.jsonl")
