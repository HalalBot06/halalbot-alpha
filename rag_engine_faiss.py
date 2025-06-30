# rag_engine_faiss.py

import argparse
import json
import os
import faiss
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime
from feedback_utils import get_adjusted_score  # Feedback-aware score adjustments

# ----------------------------
# Load Model + FAISS Index
# ----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("halalbot_faiss.index")
with open("halalbot_faiss_metadata.json", "r") as f:
    metadata = json.load(f)

# ----------------------------
# Source Categorization
# ----------------------------
def source_category(source_path):
    path = source_path.lower()
    if "quran" in path or "surah" in path:
        return "quran"
    elif "hadith" in path or "bukhari" in path or "muslim" in path:
        return "hadith"
    elif "fatwa" in path or "askimam" in path:
        return "fatwa"
    elif "zakat" in path:
        return "zakat"
    return "other"

def passes_filter(source_path, filter_type):
    category = source_category(source_path)
    return (
        filter_type is None or
        (filter_type == "quran-only" and category == "quran") or
        (filter_type == "hadith-only" and category == "hadith") or
        (filter_type == "fatwa-only" and category == "fatwa") or
        (filter_type == "zakat-only" and category == "zakat") or
        (filter_type == "other-only" and category == "other")
    )

# ----------------------------
# Cleanup Utilities
# ----------------------------
def clean_text(text):
    text = re.sub(r"(ANSWER\s*:?)(\s*Share:)?", r"\1\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"\bShare:\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip()

# ----------------------------
# Main Search Function
# ----------------------------
def search_faiss(query, top_k=5, min_score=0.5, source_filter=None):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, top_k * 5)  # over-fetch to allow sorting
    results = []

    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        item = metadata[idx]
        raw_text = item.get("text", "").strip()
        source_path = item.get("source", "unknown.txt")
        base_score = float(score)

        if base_score < min_score:
            continue
        if source_filter and not passes_filter(source_path, source_filter):
            continue

        adjusted_score = get_adjusted_score(base_score, raw_text)

        results.append({
            "text": clean_text(raw_text),
            "source": source_path,
            "score": adjusted_score,
            "base_score": base_score,
            "category": source_category(source_path)
        })

    # Sort by source priority and adjusted score
    source_order = {"quran": 0, "hadith": 1, "fatwa": 2, "zakat": 3, "other": 4}
    results.sort(key=lambda x: (source_order.get(x["category"], 5), -x["score"]))

    return results[:top_k]

# ----------------------------
# Formatting Output
# ----------------------------
def format_markdown_response(query, results):
    output = f"\n**🔍 Query:** _{query}_\n\n"
    if not results:
        return output + "_No relevant answers found._"
    for i, result in enumerate(results, 1):
        output += f"**{i}.** {result['text']}\n"
        output += f"📘 **Source:** `{result['source']}`\n"
        output += f"🧠 **Score:** `{result['score']:.2f}`\n\n"
    return output

# ----------------------------
# Optional Search Logging
# ----------------------------
def log_query(query, results, log_path="search_log.jsonl"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "results": results
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# ----------------------------
# CLI Entry Point
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HalalBot RAG Search")
    parser.add_argument("query", type=str, help="Your query to search")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--min-score", type=float, default=0.5, help="Minimum cosine similarity score")
    parser.add_argument("--filter", choices=[
        "quran-only", "hadith-only", "fatwa-only", "zakat-only", "other-only"
    ], help="Filter results by source type")

    args = parser.parse_args()
    hits = search_faiss(args.query, top_k=args.top_k, min_score=args.min_score, source_filter=args.filter)
    print(format_markdown_response(args.query, hits))
    log_query(args.query, hits)




