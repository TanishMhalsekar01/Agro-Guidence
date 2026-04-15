import streamlit as st
import json
import os
import requests
import time
from ctransformers import AutoModelForCausalLM
from login_page import show_login_page

DATA_FILE = "agro_data.json"
MODEL_FILE = "tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf" 
REMOTE_URL = "https://gist.github.com/VedGaonkar/bcf7ee3371723125b372d636681e73ab/raw/9e22ccd22b6cc74ca7cc5c9beda4af4e35842eba/agro_data.json"

st.set_page_config(page_title="Agro Guidance", layout="wide", page_icon="🌱")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }

    .stat-box {
        background-color: #1c1f26; 
        color: white;
        padding: 20px; 
        border-radius: 15px;
        text-align: center; 
        border: 1px solid #2a2a2a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .stat-box h3 { color: #4caf50 !important; }
    .stat-box p { color: #e0e0e0 !important; }

    .crop-card {
        background-color: #1c1f26; 
        color: #ffffff;   /* 🔥 MAIN FIX */
        padding: 20px; 
        border-radius: 12px;
        border-left: 8px solid #4caf50; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.2); 
        margin-bottom: 15px;
    }

    .crop-card b {
        color: #ffcc00;  /* highlight title */
    }

    .ai-response {
        background-color: #1b2b1b; 
        color: #a5d6a7;   /* 🔥 FIX */
        padding: 20px; 
        border-radius: 12px;
        border: 1px dashed #4caf50;
        font-style: italic;
    }

    .stTextInput>div>div>input {
        background-color: #1c1f26;
        color: white;
    }

    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #4caf50; 
        color: white; 
        height: 3em; 
    }
    </style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_local_ai():
    if os.path.exists(MODEL_FILE):
        return AutoModelForCausalLM.from_pretrained(
            MODEL_FILE, 
            model_type="llama", 
            gpu_layers=0  
        )
    return None

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"General Symptoms": {"Yellowing": "Check nitrogen levels."}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# ── Authentication Gate ──────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ── Dashboard (only accessible after login) ───────────────────────────────────
if 'agro_db' not in st.session_state:
    st.session_state.agro_db = load_data()

user = st.session_state.get("current_user", {})
st.title(f"🌾 Agro Guidance: Offline Expert & AI Advisor")
st.markdown(
    f"<p style='color:#6b7280;font-size:0.9rem;margin-top:-0.8rem;'>Welcome back, "
    f"<b style='color:#4ade80'>{user.get('first_name', '')} {user.get('last_name', '')}</b> 👋</p>",
    unsafe_allow_html=True,
)

db = st.session_state.agro_db
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.markdown(f"<div class='stat-box'><h3>{len(db)}</h3><p>Crops Covered</p></div>", unsafe_allow_html=True)
with col_s2: st.markdown(f"<div class='stat-box'><h3>{sum(len(v) for v in db.values())}</h3><p>Solutions</p></div>", unsafe_allow_html=True)
with col_s3: st.markdown(f"<div class='stat-box'><h3>Active</h3><p>Offline AI Model</p></div>", unsafe_allow_html=True)

tab_search, tab_list, tab_ai = st.tabs(["🔍 Search", "📋 Browse Library", "🤖 AI Advisor (Offline)"])

with tab_search:
    query = st.text_input("Search Crop...", placeholder="e.g. Mango")
    if query:
        for crop, issues in db.items():
            if query.lower() in crop.lower():
                st.markdown(f"### 📍 {crop}")
                for p, s in issues.items():
                    st.markdown(f'<div class="crop-card"><b>⚠️ {p}</b><br>{s}</div>', unsafe_allow_html=True)

with tab_list:
    crops = sorted(db.keys())
    for c in crops:
        with st.expander(f"🌿 {c}"):
            for p, s in db[c].items():
                st.write(f"**{p}:** {s}")

with tab_ai:
    st.subheader("Personal AI Farming Consultant")
    st.write("Ask questions about soil, weather, or farming techniques.")
    
    user_prompt = st.text_input("Ask the Offline AI:", placeholder="How do I make organic fertilizer?")
    
    if user_prompt:
        ai_model = load_local_ai()
        if ai_model:
            with st.spinner("AI is generating advice on your CPU..."):
                full_prompt = f"<|system|>\nYou are a helpful Indian Agriculture Expert. Give a short, practical answer in 3 sentences.\n<|user|>\n{user_prompt}\n<|assistant|>\n"
                response = ai_model(full_prompt, max_new_tokens=100, temperature=0.7)
                st.markdown(f'<div class="ai-response"><b>AI Advisor:</b><br>{response}</div>', unsafe_allow_html=True)
        else:
            st.error(f"Model file '{MODEL_FILE}' not found in directory!")
            st.info("Make sure the downloaded .gguf file is in the same folder as this script.")

with st.sidebar:
    st.title("Settings")

    # ── User info card ──
    user = st.session_state.get("current_user", {})
    if user:
        st.markdown(
            f"""
            <div style='background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);
                        border-radius:12px;padding:12px 14px;margin-bottom:12px;'>
                <p style='margin:0;color:#4ade80;font-weight:600;font-size:0.95rem;'>
                    👤 {user.get('first_name','')} {user.get('last_name','')}
                </p>
                <p style='margin:2px 0 0;color:#6b7280;font-size:0.78rem;'>@{user.get('username','')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("🔄 Sync Global Data"):
        res = requests.get(REMOTE_URL)
        if res.status_code == 200:
            save_data(res.json())
            st.session_state.agro_db = res.json()
            st.success("Database Updated!")
            st.rerun()

    st.divider()
    if st.button("🚪 Log Out", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()