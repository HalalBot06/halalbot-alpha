import streamlit as st
from rag_engine_faiss import search_faiss, format_markdown_response
from feedback_utils import log_feedback
import json
import os
import hashlib
from datetime import datetime

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(
    page_title="HalalBot",
    page_icon="static/halalbot_favicon.ico",
    layout="centered"
)

# ----------------------------
# File Paths
# ----------------------------
USERS_FILE = "users.json"
INVITE_CODES_FILE = "invite_codes.json"
HISTORY_DIR = "data/history"
BLOCKED_FILE = "blocked_queries.txt"
BLOCKED_LOG = "blocked_queries_log.jsonl"
os.makedirs(HISTORY_DIR, exist_ok=True)

# ----------------------------
# Utility Functions
# ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# ----------------------------
# Blocked Query Handling
# ----------------------------
def load_blocked_phrases():
    if not os.path.exists(BLOCKED_FILE):
        return []
    with open(BLOCKED_FILE, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

BLOCKED_PHRASES = load_blocked_phrases()

def is_blocked_query(query):
    lowered = query.lower()
    return any(phrase in lowered for phrase in BLOCKED_PHRASES)

def log_blocked_query(email, query):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "email": email,
        "query": query
    }
    with open(BLOCKED_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ----------------------------
# User Management
# ----------------------------
def load_users():
    return load_json(USERS_FILE)

def save_users(users):
    save_json(USERS_FILE, users)

def authenticate_user(email, password):
    users = load_users()
    hashed = hash_password(password)
    return email in users and users[email]["password"] == hashed

def register_user(email, password, invite_code):
    users = load_users()
    if email in users:
        return False, "User already exists."
    if not validate_invite_code(invite_code):
        return False, "Invalid or used invite code."
    users[email] = {
        "password": hash_password(password),
        "invite_code": invite_code,
        "is_admin": False
    }
    save_users(users)
    use_invite_code(invite_code, email)
    return True, None

def is_admin(email):
    users = load_users()
    return users.get(email, {}).get("is_admin", False)

# ----------------------------
# Invite Code Management
# ----------------------------
def validate_invite_code(code):
    codes = load_json(INVITE_CODES_FILE)
    return code in codes and not codes[code].get("used", False)

def use_invite_code(code, email):
    codes = load_json(INVITE_CODES_FILE)
    if code in codes:
        codes[code]["used"] = True
        codes[code]["email"] = email
        save_json(INVITE_CODES_FILE, codes)

# ----------------------------
# History Logging
# ----------------------------
def log_query_for_user(email, query, results):
    file = os.path.join(HISTORY_DIR, f"{hash_email(email)}.jsonl")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "results": results
    }
    with open(file, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ----------------------------
# Session Initialization
# ----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ----------------------------
# Login/Register UI
# ----------------------------
def show_login():
    st.title("🔐 HalalBot Login")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In"):
            if authenticate_user(email, password):
                st.session_state.authenticated = True
                st.session_state.email = email
                st.session_state.is_admin = is_admin(email)
                st.rerun()
            else:
                st.error("Invalid credentials")
    with tab2:
        new_email = st.text_input("New Email", key="register_email")
        new_password = st.text_input("New Password", type="password", key="register_password")
        invite_code = st.text_input("Invite Code", key="invite_code")
        if st.button("Register"):
            success, msg = register_user(new_email, new_password, invite_code)
            if success:
                st.success("Registered! Please log in.")
            else:
                st.error(msg)

# ----------------------------
# Admin Dashboard
# ----------------------------
def show_admin_dashboard():
    st.subheader("🛠 Admin Dashboard")
    users = load_users()
    codes = load_json(INVITE_CODES_FILE)
    st.markdown(f"**Total users:** `{len(users)}`")
    st.markdown(f"**Total invite codes:** `{len(codes)}`")
    used = len([c for c in codes.values() if c.get("used")])
    st.markdown(f"**Used codes:** `{used}`")
    st.markdown("---")

# ----------------------------
# Main UI
# ----------------------------
def show_main():
    st.image("static/halalbot_logo.png", width=200)
    st.title("HalalBot Alpha")
    st.caption("Qur’an & Hadith AI Assistant (Local RAG) – *Alpha v0.2*")
    st.markdown("""
    ### ℹ️ Disclaimer
    > 🧠 *Note: I am an AI assistant trained on the Qur’an, Hadith, and select scholarly sources.*  
    > Please consult your local Imam or a qualified scholar for specific religious rulings.
    """)

    query = st.text_input("Ask a question:")
    top_k = st.slider("Number of responses", 1, 10, 5)
    min_score = st.slider("Minimum score", 0.0, 1.0, 0.5)
    filter_choice = st.selectbox("Source filter", [
        "All Sources", "Quran only", "Hadith only", "Fatwa only", "Zakat only", "Other only"
    ])
    filter_map = {
        "Quran only": "quran-only",
        "Hadith only": "hadith-only",
        "Fatwa only": "fatwa-only",
        "Zakat only": "zakat-only",
        "Other only": "other-only",
        "All Sources": None
    }

    if query:
        if is_blocked_query(query):
            st.error("❌ This question is inappropriate and will not be processed. Please respect the sacred nature of this service.")
            log_blocked_query(st.session_state.email, query)
            return

        st.markdown(f"#### 🔍 **Query:** _{query}_")
        results = search_faiss(query, top_k=top_k, min_score=min_score, source_filter=filter_map[filter_choice])
        if results:
            log_query_for_user(st.session_state.email, query, results)
            for i, result in enumerate(results, 1):
                st.markdown(f"""
**{i}.** {result['text']}

📘 **Source:** `{result['source']}`  
🧠 **Score:** `{result['score']:.2f}`
""")
                result_id = hash_text(result["text"])
                with st.expander("Was this helpful?"):
                    col1, col2 = st.columns(2)
                    if col1.button("👍 Yes", key=f"yes_{i}"):
                        log_feedback(query, result["text"], "up", st.session_state.email)
                        st.success("Thank you for your feedback!")
                    if col2.button("👎 No", key=f"no_{i}"):
                        log_feedback(query, result["text"], "down", st.session_state.email)
                        st.warning("We’ll use your feedback to improve.")
        else:
            st.warning("No relevant answers found.")

    if st.session_state.is_admin:
        with st.expander("🔐 Admin Tools"):
            show_admin_dashboard()

    st.markdown("---")
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.session_state.email = ""
        st.session_state.is_admin = False
        st.rerun()

# ----------------------------
# Launch App
# ----------------------------
if not st.session_state.authenticated:
    show_login()
else:
    show_main()






