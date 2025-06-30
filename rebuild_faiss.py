import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data
with open("corpus.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line.strip()) for line in f]

texts = [r["text"] for r in records]
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, "halalbot_faiss.index")
with open("halalbot_faiss_metadata.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("✅ Index built and saved.")
