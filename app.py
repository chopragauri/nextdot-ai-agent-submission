"""
Streamlit UI for the AI Agent pipeline.
Run with: streamlit run app.py
"""

import streamlit as st

from agent import process_message
from config import AVAILABLE_MODELS, DEFAULT_MODEL
from sample_inputs import SAMPLES

# --- Page Config ---
st.set_page_config(
    page_title="AI Agent - Thinks Out Loud",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Mini AI Agent That Thinks Out Loud")
st.markdown(
    "Analyzes customer messages through a 4-step pipeline: "
    "**Classify** → **Extract** → **Reply** → **Explain Reasoning**"
)
st.divider()

# --- Sidebar: Model Selection & Info ---
st.sidebar.header("⚙️ Settings")
selected_model = st.sidebar.selectbox(
    "Select Model",
    options=list(AVAILABLE_MODELS.keys()),
    index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL),
    format_func=lambda m: f"{m}",
    help="Choose the Gemini model to use for analysis",
)
st.sidebar.caption(f"_{AVAILABLE_MODELS[selected_model]}_")

compare_mode = st.sidebar.checkbox(
    "🔀 Compare two models side-by-side",
    help="Run the same message through two different models and compare outputs",
)
if compare_mode:
    second_model = st.sidebar.selectbox(
        "Second Model",
        options=[m for m in AVAILABLE_MODELS if m != selected_model],
    )

st.sidebar.divider()
st.sidebar.markdown(
    "**How it works:**\n"
    "1. Paste any customer message\n"
    "2. The AI classifies intent & sentiment\n"
    "3. Extracts structured data (name, urgency, etc.)\n"
    "4. Writes a tone-matched reply\n"
    "5. Explains its own reasoning"
)

# --- Sample Input Buttons ---
st.subheader("📋 Try a Sample Input")
cols = st.columns(3)
for i, (key, sample) in enumerate(SAMPLES.items()):
    with cols[i]:
        if st.button(f"Input {key}: {sample['label']}", use_container_width=True):
            st.session_state["input_message"] = sample["message"]

# --- Message Input ---
st.subheader("✍️ Enter Customer Message")
message = st.text_area(
    "Paste or type a customer message below:",
    value=st.session_state.get("input_message", ""),
    height=120,
    placeholder="e.g., I ordered the premium plan 3 weeks ago and STILL haven't received access...",
)


# --- Urgency badge with color ---
def urgency_badge(level: str) -> str:
    """Return a colored markdown badge for the urgency level."""
    colors = {
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🟠",
        "Critical": "🔴",
    }
    return f"{colors.get(level, '⚪')} {level}"


def display_result(result: dict, title: str = ""):
    """Render the pipeline output in organized, readable sections."""
    if title:
        st.markdown(f"### 🤖 {title}")

    st.markdown("---")

    # --- Step 1: Classification ---
    st.markdown("#### Step 1: Classification")
    col1, col2 = st.columns(2)
    with col1:
        intent = result["classification"]["intent"]
        intent_icons = {
            "complaint": "🔴 COMPLAINT",
            "query": "🔵 QUERY",
            "feedback": "🟢 FEEDBACK",
            "request": "🟠 REQUEST",
        }
        st.markdown(f"**Intent:** {intent_icons.get(intent, intent.upper())}")
    with col2:
        sentiment = result["classification"]["sentiment"]
        sentiment_icons = {
            "positive": "😊 Positive",
            "neutral": "😐 Neutral",
            "negative": "😞 Negative",
            "urgent": "🚨 Urgent",
        }
        st.markdown(f"**Sentiment:** {sentiment_icons.get(sentiment, sentiment.upper())}")

    # --- Step 2: Extraction ---
    st.markdown("#### Step 2: Extracted Fields")
    ext = result["extraction"]
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("👤 Customer Name", ext["customer_name"] or "Not provided")
    col_b.metric("📂 Issue Type", ext["issue_type"])
    col_c.markdown(f"**⚡ Urgency**\n\n{urgency_badge(ext['urgency_level'])}")
    col_d.metric("🎯 Action", ext["recommended_action"][:35] + ("..." if len(ext["recommended_action"]) > 35 else ""))
    if len(ext["recommended_action"]) > 35:
        st.caption(f"**Full recommended action:** {ext['recommended_action']}")

    # --- Step 3: Generated Reply ---
    st.markdown("#### Step 3: Generated Reply")
    st.success(result["reply"])

    # --- Step 4: Reasoning ---
    st.markdown("#### Step 4: Model's Reasoning")
    st.info(result["reasoning"])

    # Raw JSON output (collapsible)
    with st.expander("📄 View Raw JSON Output"):
        st.json(result)


# --- Run Pipeline ---
if st.button("🚀 Analyze Message", type="primary", use_container_width=True):
    if not message or not message.strip():
        st.error("⚠️ Please enter a customer message to analyze.")
    else:
        try:
            if compare_mode:
                # Side-by-side model comparison
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
                # Single model analysis
                with st.spinner(f"Analyzing with {selected_model}..."):
                    result = process_message(message, model_name=selected_model)
                display_result(result)
        except RuntimeError as e:
            st.error(f"❌ Pipeline error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
