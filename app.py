"""
Streamlit UI for the AI Agent pipeline.
Features dark neon and clean light themes with custom CSS styling.
Run with: streamlit run app.py
"""

import os
import streamlit as st

from agent import process_message
from config import AVAILABLE_MODELS, DEFAULT_MODEL
from sample_inputs import SAMPLES

# --- Page Config ---
st.set_page_config(
    page_title="AI Agent - Thinks Out Loud",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar: Theme Toggle + Model Selection ---
st.sidebar.markdown("## ⚙️ Settings")
theme_choice = st.sidebar.radio(
    "Theme",
    options=["🌙 Dark", "☀️ Light"],
    horizontal=True,
    index=0,
)
theme = theme_choice == "🌙 Dark"

selected_model = st.sidebar.selectbox(
    "Model",
    options=list(AVAILABLE_MODELS.keys()),
    index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL),
    help="Choose the Gemini model for analysis",
)
st.sidebar.caption(f"_{AVAILABLE_MODELS[selected_model]}_")

compare_mode = st.sidebar.checkbox(
    "🔀 Compare two models",
    help="Run the same message through two models and compare",
)
if compare_mode:
    second_model = st.sidebar.selectbox(
        "Second Model",
        options=[m for m in AVAILABLE_MODELS if m != selected_model],
    )

st.sidebar.divider()
st.sidebar.markdown(
    "**Pipeline Steps:**\n"
    "1. 🏷️ Classify intent & sentiment\n"
    "2. 📋 Extract structured fields\n"
    "3. ✉️ Generate tone-matched reply\n"
    "4. 🧠 Explain reasoning"
)

# --- Theme CSS ---
if theme:
    # ===== DARK NEON THEME =====
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 50%, #0a0a1a 100%);
        color: #e0e0e0;
    }
    .neon-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7c3aed, #00d4ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
        margin-bottom: 0;
    }
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .neon-subtitle {
        text-align: center;
        color: #8892a0;
        font-size: 1.05rem;
        margin-top: 0;
        letter-spacing: 2px;
    }
    .glow-card {
        background: rgba(15, 20, 35, 0.85);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.08), inset 0 0 15px rgba(0, 212, 255, 0.03);
        transition: box-shadow 0.3s ease;
    }
    .glow-card:hover {
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.15), inset 0 0 20px rgba(0, 212, 255, 0.05);
    }
    .glow-card h4 {
        color: #00d4ff;
        margin-top: 0;
        font-size: 1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 1px;
        margin: 4px;
    }
    .badge-complaint { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-query { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    .badge-feedback { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }
    .badge-request { background: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.4); }
    .badge-positive { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }
    .badge-neutral { background: rgba(148, 163, 184, 0.2); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.4); }
    .badge-negative { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-urgent { background: rgba(220, 38, 38, 0.3); color: #ff4444; border: 1px solid rgba(220, 38, 38, 0.5); animation: pulse-urgent 1.5s infinite; }
    @keyframes pulse-urgent {
        0%, 100% { box-shadow: 0 0 5px rgba(220, 38, 38, 0.3); }
        50% { box-shadow: 0 0 20px rgba(220, 38, 38, 0.6); }
    }
    .urgency-low { color: #4ade80; }
    .urgency-medium { color: #facc15; }
    .urgency-high { color: #fb923c; }
    .urgency-critical { color: #ff4444; font-weight: 700; }
    .metric-card {
        background: rgba(15, 20, 35, 0.7);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #8892a0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.05rem;
        color: #e0e0e0;
        font-weight: 600;
    }
    .reply-box {
        background: rgba(0, 212, 255, 0.06);
        border-left: 3px solid #00d4ff;
        border-radius: 0 10px 10px 0;
        padding: 18px 20px;
        margin: 10px 0;
        color: #d0d0d0;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    .reasoning-box {
        background: rgba(124, 58, 237, 0.06);
        border-left: 3px solid #7c3aed;
        border-radius: 0 10px 10px 0;
        padding: 18px 20px;
        margin: 10px 0;
        color: #b0b0b0;
        line-height: 1.7;
        font-size: 0.9rem;
        font-style: italic;
    }
    .step-label {
        display: inline-block;
        background: rgba(0, 212, 255, 0.12);
        color: #00d4ff;
        padding: 3px 10px;
        border-radius: 5px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .stButton > button {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #e0e0e0 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #00d4ff, #7c3aed) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        padding: 12px !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.4) !important;
    }
    .stTextArea textarea {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.15) !important;
    }
    section[data-testid="stSidebar"] {
        background: rgba(8, 10, 25, 0.95) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.1);
    }
    hr { border-color: rgba(0, 212, 255, 0.15) !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    # ===== LIGHT CLEAN THEME =====
    st.markdown("""
    <style>
    .stApp {
        background: #f8f9fc;
        color: #1a1a2e;
    }
    .neon-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .neon-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.05rem;
        margin-top: 0;
        letter-spacing: 2px;
    }
    .glow-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
        transition: box-shadow 0.3s ease;
    }
    .glow-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .glow-card h4 {
        color: #2563eb;
        margin-top: 0;
        font-size: 1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 1px;
        margin: 4px;
    }
    .badge-complaint { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .badge-query { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
    .badge-feedback { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    .badge-request { background: #fff7ed; color: #ea580c; border: 1px solid #fed7aa; }
    .badge-positive { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    .badge-neutral { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
    .badge-negative { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .badge-urgent { background: #fef2f2; color: #dc2626; border: 1px solid #f87171; font-weight: 800; }
    .urgency-low { color: #16a34a; }
    .urgency-medium { color: #ca8a04; }
    .urgency-high { color: #ea580c; }
    .urgency-critical { color: #dc2626; font-weight: 700; }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.05rem;
        color: #1e293b;
        font-weight: 600;
    }
    .reply-box {
        background: #eff6ff;
        border-left: 3px solid #2563eb;
        border-radius: 0 10px 10px 0;
        padding: 18px 20px;
        margin: 10px 0;
        color: #1e293b;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    .reasoning-box {
        background: #f5f3ff;
        border-left: 3px solid #7c3aed;
        border-radius: 0 10px 10px 0;
        padding: 18px 20px;
        margin: 10px 0;
        color: #374151;
        line-height: 1.7;
        font-size: 0.9rem;
        font-style: italic;
    }
    .step-label {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb;
        padding: 3px 10px;
        border-radius: 5px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .stButton > button {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        color: #374151 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.12) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        padding: 12px !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    }
    .stTextArea textarea {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        color: #1e293b !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    hr { border-color: #e2e8f0 !important; }

    /* ===== Force dark text on all Streamlit elements in light mode ===== */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
    .stApp .stMarkdown, .stApp .stMarkdown p {
        color: #1e293b !important;
    }
    /* Sidebar text */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #1e293b !important;
    }
    /* Sidebar header */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    /* Sidebar caption */
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {
        color: #64748b !important;
    }
    /* ===== Selectbox — force white background everywhere ===== */
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #1e293b !important;
    }
    .stSelectbox [data-baseweb="select"] span {
        color: #1e293b !important;
    }
    .stSelectbox [data-baseweb="select"] {
        border: 1.5px solid #2563eb !important;
        border-radius: 8px !important;
    }
    .stSelectbox svg { fill: #2563eb !important; }
    /* Dropdown popover menu */
    [data-baseweb="popover"], [data-baseweb="popover"] > div,
    [data-baseweb="menu"], [data-baseweb="menu"] > div,
    ul[role="listbox"], ul[role="listbox"] > li {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #1e293b !important;
    }
    ul[role="listbox"] > li:hover,
    ul[role="listbox"] > li[aria-selected="true"] {
        background-color: #eff6ff !important;
    }
    /* Checkbox and toggle labels */
    .stCheckbox label span,
    .stCheckbox label p {
        color: #1e293b !important;
    }
    /* ===== Toggle switch — visible track and thumb ===== */
    div[data-testid="stToggle"] label span,
    div[data-testid="stToggle"] label p {
        color: #1e293b !important;
    }
    /* Toggle track (off state = gray, on state = blue) */
    div[data-testid="stToggle"] [role="checkbox"] {
        background-color: #cbd5e1 !important;
    }
    div[data-testid="stToggle"] [role="checkbox"][aria-checked="true"] {
        background-color: #2563eb !important;
    }
    /* Toggle thumb */
    div[data-testid="stToggle"] [role="checkbox"] > div {
        background-color: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }
    /* Text area placeholder */
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    /* Text area proper styling */
    .stTextArea textarea {
        background: #ffffff !important;
        border: 1.5px solid #d1d5db !important;
        color: #1e293b !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    /* Label text */
    .stTextArea label p, .stSelectbox label p {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    /* Headings */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        color: #0f172a !important;
    }
    /* Keep neon-title gradient */
    .neon-title { -webkit-text-fill-color: transparent !important; }
    /* Keep badge colors */
    .badge { color: inherit !important; }
    .badge-complaint { color: #dc2626 !important; }
    .badge-query { color: #2563eb !important; }
    .badge-feedback { color: #16a34a !important; }
    .badge-request { color: #ea580c !important; }
    .badge-positive { color: #16a34a !important; }
    .badge-neutral { color: #475569 !important; }
    .badge-negative { color: #dc2626 !important; }
    .badge-urgent { color: #dc2626 !important; }
    /* Keep card heading colors */
    .glow-card h4 { color: #2563eb !important; }
    .step-label { color: #2563eb !important; }
    /* Keep metric colors */
    .metric-label { color: #64748b !important; }
    .metric-value { color: #1e293b !important; }
    /* Keep urgency colors */
    .urgency-low { color: #16a34a !important; }
    .urgency-medium { color: #ca8a04 !important; }
    .urgency-high { color: #ea580c !important; }
    .urgency-critical { color: #dc2626 !important; }
    /* Reply and reasoning boxes */
    .reply-box { color: #1e293b !important; }
    .reasoning-box { color: #374151 !important; }
    /* Subtitle */
    .neon-subtitle { color: #64748b !important; -webkit-text-fill-color: #64748b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
banner_name = "banner_dark.png" if theme else "banner_light.png"
banner_path = os.path.join(os.path.dirname(__file__), "assets", banner_name)
fallback_banner = os.path.join(os.path.dirname(__file__), "assets", "banner.png")

if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
elif os.path.exists(fallback_banner):
    st.image(fallback_banner, use_container_width=True)
else:
    # Fallback: styled text header (only when no banner images exist)
    st.markdown('<h1 class="neon-title">🧠 Mini AI Agent That Thinks Out Loud</h1>', unsafe_allow_html=True)
    st.markdown('<p class="neon-subtitle">CLASSIFY  •  EXTRACT  •  REPLY  •  EXPLAIN</p>', unsafe_allow_html=True)
st.divider()

# --- Sample Input Buttons ---
st.markdown("### 📋 Try a Sample Input")
cols = st.columns(3)
for i, (key, sample) in enumerate(SAMPLES.items()):
    with cols[i]:
        if st.button(f"Input {key}: {sample['label']}", use_container_width=True):
            st.session_state["input_message"] = sample["message"]

# --- Message Input ---
st.markdown("### ✍️ Enter Customer Message")
message = st.text_area(
    "Paste or type a customer message below:",
    value=st.session_state.get("input_message", ""),
    height=120,
    placeholder="e.g., I ordered the premium plan 3 weeks ago and STILL haven't received access...",
)


def display_result(result: dict, title: str = ""):
    """Render the pipeline output with themed styling."""
    if title:
        st.markdown(f"### 🤖 {title}")

    # --- Step 1: Classification ---
    intent = result["classification"]["intent"]
    sentiment = result["classification"]["sentiment"]

    st.markdown(f"""
    <div class="glow-card">
        <span class="step-label">Step 1</span>
        <h4>Classification</h4>
        <span class="badge badge-{intent}">{intent.upper()}</span>
        <span class="badge badge-{sentiment}">{sentiment.upper()}</span>
    </div>
    """, unsafe_allow_html=True)

    # --- Step 2: Extraction ---
    ext = result["extraction"]
    urgency = ext["urgency_level"]
    urgency_class = f"urgency-{urgency.lower()}"

    st.markdown(f"""
    <div class="glow-card">
        <span class="step-label">Step 2</span>
        <h4>Extracted Fields</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; margin-top: 10px;">
            <div class="metric-card">
                <div class="metric-label">👤 Customer</div>
                <div class="metric-value">{ext["customer_name"] or "Not provided"}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">📂 Issue Type</div>
                <div class="metric-value">{ext["issue_type"]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">⚡ Urgency</div>
                <div class="metric-value {urgency_class}">{urgency}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">🎯 Action</div>
                <div class="metric-value" style="font-size: 0.85rem;">{ext["recommended_action"]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Step 3: Reply ---
    reply_text = result["reply"].replace("\n", "<br>")
    st.markdown(f"""
    <div class="glow-card">
        <span class="step-label">Step 3</span>
        <h4>Generated Reply</h4>
        <div class="reply-box">{reply_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Step 4: Reasoning ---
    reasoning_text = result["reasoning"].replace("\n", "<br>")
    st.markdown(f"""
    <div class="glow-card">
        <span class="step-label">Step 4</span>
        <h4>Model's Reasoning</h4>
        <div class="reasoning-box">{reasoning_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # Raw JSON
    with st.expander("📄 View Raw JSON Output"):
        st.json(result)


# --- Run Pipeline ---
if st.button("⚡ Analyze Message", type="primary", use_container_width=True):
    if not message or not message.strip():
        st.error("⚠️ Please enter a customer message to analyze.")
    else:
        try:
            if compare_mode:
                col_left, col_right = st.columns(2)
                with col_left:
                    with st.spinner(f"Running {selected_model}..."):
                        result1 = process_message(message, model_name=selected_model)
                    display_result(result1, title=selected_model)
                with col_right:
                    with st.spinner(f"Running {second_model}..."):
                        result2 = process_message(message, model_name=second_model)
                    display_result(result2, title=second_model)
            else:
                with st.spinner(f"Analyzing with {selected_model}..."):
                    result = process_message(message, model_name=selected_model)
                display_result(result)
        except RuntimeError as e:
            st.error(f"❌ Pipeline error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
