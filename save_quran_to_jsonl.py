import os
import json

# Path to folder containing surah_1.txt to surah_114.txt
INPUT_DIR = "data/quran_txt"
OUTPUT_FILE = "quran_corpus.jsonl"

def build_quran_jsonl(input_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as out_file:
        for i in range(1, 115):  # Surahs 1 to 114
            filename = f"surah_{i}.txt"
            path = os.path.join(input_dir, filename)

            if not os.path.exists(path):
                print(f"⚠️ Missing file: {filename}")
                continue

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for j, line in enumerate(lines, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue

                doc = {
                    "id": f"quran-surah_{i}-ayah_{j}",
                    "source": "quran",
                    "text": clean_line
                }
                out_file.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"✅ Done. Quran corpus written to {output_file}")

if __name__ == "__main__":
    build_quran_jsonl(INPUT_DIR, OUTPUT_FILE)
