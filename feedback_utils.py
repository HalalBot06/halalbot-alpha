# feedback_utils.py
import json
import os
import hashlib
from datetime import datetime

FEEDBACK_LOG_FILE = "feedback_log.jsonl"
ADJUSTMENTS_FILE = "feedback_adjustments.json"

# -------------- Hashing Utility --------------
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

# -------------- Logging Utility --------------
def log_feedback(query, text, vote, user_email=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "text_hash": hash_text(text),
        "vote": vote,  # "up" or "down"
        "user": user_email or "anon"
    }
    with open(FEEDBACK_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    update_score_adjustments(entry["text_hash"], vote)

# -------------- Score Adjustment Logic --------------
def load_adjustments():
    if not os.path.exists(ADJUSTMENTS_FILE):
        return {}
    with open(ADJUSTMENTS_FILE, "r") as f:
        return json.load(f)

def save_adjustments(data):
    with open(ADJUSTMENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_score_adjustments(text_hash, vote):
    adj = load_adjustments()
    if text_hash not in adj:
        adj[text_hash] = {"thumbs_up": 0, "thumbs_down": 0}

    if vote == "up":
        adj[text_hash]["thumbs_up"] += 1
    elif vote == "down":
        adj[text_hash]["thumbs_down"] += 1

    save_adjustments(adj)

def get_score_penalty(text_hash):
    adj = load_adjustments()
    if text_hash not in adj:
        return 0.0
    downs = adj[text_hash].get("thumbs_down", 0)
    return min(0.02 * downs, 0.3)  # cap penalty at 0.3

def get_vote_summary(text_hash):
    adj = load_adjustments()
    if text_hash not in adj:
        return None
    return adj[text_hash]

def get_adjusted_score(base_score, text):
    text_hash = hash_text(text)
    penalty = get_score_penalty(text_hash)
    return max(0.0, base_score - penalty)
