# save as patch_misc_and_random.py
import json
from pathlib import Path
from tqdm import tqdm

def patch_file(file_in, file_out):
    with open(file_in) as f_in, open(file_out, "w") as f_out:
        for line in tqdm(f_in, desc=f"Patching {file_in}"):
            obj = json.loads(line)
            if "text" not in obj:
                if "question" in obj and "answer" in obj:
                    obj["text"] = f"Question: {obj['question']}\nAnswer: {obj['answer']}"
                    obj["source"] = "fatwa"
            f_out.write(json.dumps(obj) + "\n")

patch_file("misc_fatwas_corpus.jsonl", "misc_fatwas_corpus_patched.jsonl")
patch_file("random_fatwas_corpus.jsonl", "random_fatwas_corpus_patched.jsonl")
