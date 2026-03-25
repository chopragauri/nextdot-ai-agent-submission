"""
Streamlit UI for the AI Agent pipeline.
Run with: streamlit run app.py
"""

import json

import streamlit as st

from agent import process_message
from config import AVAILABLE_MODELS, DEFAULT_MODEL
from sample_inputs import SAMPLES

# --- Page Config ---
st.set_page_config(page_title="AI Agent - Thinks Out Loud", layout="wide")
st.title("Mini AI Agent That Thinks Out Loud")
st.caption("Analyzes customer messages: classifies, extracts, replies, and explains its reasoning.")

# --- Sidebar: Model Selection ---
st.sidebar.header("Settings")
selected_model = st.sidebar.selectbox(
    "Select Model",
    options=list(AVAILABLE_MODELS.keys()),
    index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL),
    format_func=lambda m: f"{m} — {AVAILABLE_MODELS[m]}",
)
compare_mode = st.sidebar.checkbox("Compare two models side-by-side")
if compare_mode:
    second_model = st.sidebar.selectbox(
        "Second Model",
        options=[m for m in AVAILABLE_MODELS if m != selected_model],
    )

# --- Sample Input Buttons ---
st.subheader("Try a Sample Input")
cols = st.columns(3)
for i, (key, sample) in enumerate(SAMPLES.items()):
    with cols[i]:
        if st.button(f"Input {key}: {sample['label']}", use_container_width=True):
            st.session_state["input_message"] = sample["message"]

# --- Message Input ---
st.subheader("Enter Customer Message")
message = st.text_area(
    "Paste or type a customer message below:",
    value=st.session_state.get("input_message", ""),
    height=120,
    placeholder="e.g., I ordered the premium plan 3 weeks ago and STILL haven't received access...",
)


def display_result(result: dict, title: str = ""):
    """Render the pipeline output in organized sections."""
    if title:
        st.markdown(f"### {title}")

    # Classification
    col1, col2 = st.columns(2)
    with col1:
        intent = result["classification"]["intent"]
        intent_colors = {"complaint": "red", "query": "blue", "feedback": "green", "request": "orange"}
        st.markdown(f"**Intent:** :{intent_colors.get(intent, 'gray')}[{intent.upper()}]")
    with col2:
        sentiment = result["classification"]["sentiment"]
        sentiment_colors = {"positive": "green", "neutral": "blue", "negative": "red", "urgent": "red"}
        st.markdown(f"**Sentiment:** :{sentiment_colors.get(sentiment, 'gray')}[{sentiment.upper()}]")

    # Extraction
    st.markdown("#### Extracted Fields")
    ext = result["extraction"]
    extract_cols = st.columns(4)
    extract_cols[0].metric("Customer Name", ext["customer_name"] or "Not provided")
    extract_cols[1].metric("Issue Type", ext["issue_type"])
    extract_cols[2].metric("Urgency", ext["urgency_level"])
    extract_cols[3].metric("Action", ext["recommended_action"][:30])
    if len(ext["recommended_action"]) > 30:
        st.caption(f"Full action: {ext['recommended_action']}")

    # Reply
    st.markdown("#### Generated Reply")
    st.info(result["reply"])

    # Reasoning
    st.markdown("#### Model's Reasoning")
    st.warning(result["reasoning"])

    # Raw JSON (collapsible)
    with st.expander("View Raw JSON"):
        st.json(result)


# --- Run Pipeline ---
if st.button("Analyze Message", type="primary", use_container_width=True):
    if not message or not message.strip():
        st.error("Please enter a customer message to analyze.")
    else:
        if compare_mode:
            # Side-by-side comparison
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
            # Single model
            with st.spinner(f"Analyzing with {selected_model}..."):
                result = process_message(message, model_name=selected_model)
            display_result(result)
