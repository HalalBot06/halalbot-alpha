import streamlit as st
from rag_engine_faiss import search_faiss, format_markdown_response
from feedback_utils import log_feedback
import json
import os
import hashlib
from datetime import datetime

# ----------------------------
# Custom CSS and Styling Functions
# ----------------------------
def apply_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Amiri:wght@400;700&display=swap');
    
    /* Root Variables - Islamic Color Palette */
    :root {
        --primary-green: #2E7D4A;
        --light-green: #4A9B6B;
        --accent-gold: #D4AF37;
        --warm-white: #FAFAFA;
        --soft-gray: #F5F7FA;
        --text-dark: #2C3E50;
        --text-medium: #5A6C7D;
        --border-light: #E1E8ED;
        --shadow-subtle: 0 2px 8px rgba(46, 125, 74, 0.08);
        --shadow-card: 0 4px 16px rgba(46, 125, 74, 0.12);
        --gradient-primary: linear-gradient(135deg, #2E7D4A 0%, #4A9B6B 100%);
        --gradient-gold: linear-gradient(135deg, #D4AF37 0%, #F4D03F 100%);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--warm-white);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
        background: white;
        border-radius: 16px;
        box-shadow: var(--shadow-card);
        margin: 1rem auto;
        border: 1px solid var(--border-light);
    }
    
    /* Logo Styling */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .stImage > div {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-subtle);
        border: 2px solid var(--border-light);
    }
    
    /* Typography */
    h1 {
        font-family: 'Amiri', serif !important;
        color: var(--primary-green) !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Subtitle */
    .stCaption {
        text-align: center !important;
        color: var(--text-medium) !important;
        font-size: 1rem !important;
        margin-bottom: 2rem !important;
        font-style: italic;
    }
    
    /* Disclaimer Section */
    .disclaimer-container {
        background: linear-gradient(135deg, #FFF8E1 0%, #F5F5F5 100%);
        border: 2px solid var(--accent-gold);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .disclaimer-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-gold);
    }
    
    .disclaimer-container h3 {
        color: var(--primary-green) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .disclaimer-container p {
        color: var(--text-dark) !important;
        line-height: 1.6 !important;
        font-size: 0.95rem !important;
        margin: 0 !important;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border: 2px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: var(--soft-gray) !important;
        color: var(--text-dark) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 3px rgba(46, 125, 74, 0.1) !important;
        background: white !important;
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background: var(--gradient-primary) !important;
    }
    
    .stSlider > div > div > div > div {
        background: white !important;
        border: 3px solid var(--primary-green) !important;
        box-shadow: var(--shadow-subtle) !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border: 2px solid var(--border-light) !important;
        border-radius: 12px !important;
        background: var(--soft-gray) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 3px rgba(46, 125, 74, 0.1) !important;
    }
    
    /* Query Display */
    .query-header {
        background: var(--gradient-primary);
        color: white !important;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 2rem 0 1.5rem 0;
        font-weight: 500;
        box-shadow: var(--shadow-card);
        position: relative;
        overflow: hidden;
    }
    
    .query-header::before {
        content: '🔍';
        margin-right: 0.5rem;
        font-size: 1.2em;
    }
    
    /* Results Container */
    .results-container {
        margin-top: 2rem;
    }
    
    /* Individual Result Cards */
    .result-card {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-subtle);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .result-card:hover {
        box-shadow: var(--shadow-card);
        transform: translateY(-2px);
        border-color: var(--light-green);
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }
    
    /* Source Type Indicators */
    .source-quran::before {
        background: var(--gradient-primary);
    }
    
    .source-hadith::before {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
    }
    
    .source-fatwa::before {
        background: var(--gradient-gold);
    }
    
    /* Result Text */
    .result-text {
        color: var(--text-dark);
        line-height: 1.7;
        font-size: 1rem;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Source Info */
    .source-info {
        display: flex;
        gap: 1rem;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid var(--border-light);
        font-size: 0.9rem;
    }
    
    .source-badge {
        background: var(--soft-gray);
        color: var(--primary-green);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 500;
        border: 1px solid var(--border-light);
    }
    
    .score-badge {
        background: var(--gradient-gold);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: var(--shadow-subtle);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-subtle) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-card) !important;
        background: linear-gradient(135deg, #1e5d36 0%, #2d7a4f 100%) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: var(--soft-gray) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-light) !important;
        color: var(--primary-green) !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        border: 1px solid var(--border-light) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        background: white !important;
    }
    
    /* Warning/Error Messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: var(--shadow-subtle) !important;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: linear-gradient(135deg, #FFF3CD 0%, #FFF8E1 100%) !important;
        border-left: 4px solid var(--accent-gold) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #F8D7DA 0%, #FCE4EC 100%) !important;
        border-left: 4px solid #DC3545 !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #D4EDDA 0%, #E8F5E8 100%) !important;
        border-left: 4px solid var(--primary-green) !important;
    }
    
    /* Admin Section */
    .admin-section {
        background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
        border: 2px solid var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    /* Login Form Styling */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: var(--shadow-card);
        border: 1px solid var(--border-light);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: var(--soft-gray);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: var(--text-medium) !important;
        font-weight: 500 !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .result-card {
            padding: 1rem;
        }
        
        .source-info {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--soft-gray);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-green);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--light-green);
    }
    
    /* Loading States */
    .stSpinner {
        color: var(--primary-green) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def format_conversational_response_with_styling(response_text):
    """Add custom styling to conversational responses"""
    return f"""
    <div class="conversational-response">
        <div style="
            background: linear-gradient(135deg, #f8fffe 0%, #f0f9f6 100%);
            border-left: 4px solid #2E7D4A;
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(46, 125, 74, 0.08);
            font-family: 'Inter', sans-serif;
            line-height: 1.7;
            color: #2C3E50;
        ">
            {response_text}
        </div>
    </div>
    """

def create_styled_result_card(result, index):
    """Create a beautifully styled result card"""
    source_type = result.get('category', 'other')
    
    # Icons for different source types
    source_icons = {
        'quran': '📖',
        'hadith': '📜', 
        'fatwa': '⚖️',
        'zakat': '💰',
        'other': '📚'
    }
    
    icon = source_icons.get(source_type, '📚')
    
    return f"""
    <div class="result-card source-{source_type}">
        <div class="result-text">
            <strong>{index}.</strong> {result['text']}
        </div>
        <div class="source-info">
            <span class="source-badge">
                {icon} {result['source'].replace('.txt', '').replace('_', ' ').title()}
            </span>
            <span class="score-badge">
                Score: {result['score']:.2f}
            </span>
        </div>
    </div>
    """

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(
    page_title="HalalBot",
    page_icon="static/halalbot_favicon.ico",
    layout="centered"
)

# Apply the custom CSS immediately after page config
apply_custom_css()

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
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
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
    
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.caption("Qur'an & Hadith AI Assistant (Local RAG) — *Alpha v0.2*")
    
    # Enhanced disclaimer with custom styling
    st.markdown("""
    <div class="disclaimer-container">
        <h3>ℹ️ Important Disclaimer</h3>
        <p>🧠 <em>Note: I am an AI assistant trained on the Qur'an, Hadith, and select scholarly sources.</em><br>
        Please consult your local Imam or a qualified scholar for specific religious rulings.</p>
    </div>
    """, unsafe_allow_html=True)

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
            st.error("⛔ This question is inappropriate and will not be processed. Please respect the sacred nature of this service.")
            log_blocked_query(st.session_state.email, query)
            return

        # Styled query header
        st.markdown(f"""
        <div class="query-header">
            Query: <em>{query}</em>
        </div>
        """, unsafe_allow_html=True)
        
        results = search_faiss(query, top_k=top_k, min_score=min_score, source_filter=filter_map[filter_choice])
        
        if results:
            log_query_for_user(st.session_state.email, query, results)
            
            # Display results with enhanced styling
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            for i, result in enumerate(results, 1):
                # Use the styled card instead of basic markdown
                st.markdown(create_styled_result_card(result, i), unsafe_allow_html=True)
                
                # Enhanced feedback section
                result_id = hash_text(result["text"])
                with st.expander("💭 Was this helpful?"):
                    col1, col2 = st.columns(2)
                    if col1.button("👍 Yes", key=f"yes_{i}"):
                        log_feedback(query, result["text"], "up", st.session_state.email)
                        st.success("Thank you for your feedback!")
                    if col2.button("👎 No", key=f"no_{i}"):
                        log_feedback(query, result["text"], "down", st.session_state.email)
                        st.warning("We'll use your feedback to improve.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No relevant answers found.")

    # Admin section with enhanced styling
    if st.session_state.is_admin:
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        with st.expander("🛠 Admin Tools"):
            show_admin_dashboard()
        st.markdown('</div>', unsafe_allow_html=True)

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






