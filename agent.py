"""
Core AI Agent Pipeline
Processes customer messages through 4 steps: Classify, Extract, Generate Reply, Explain Reasoning.
All steps are handled by the LLM in a single structured call — no hardcoded logic.
"""

import json
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import DEFAULT_MODEL
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Load API key from .env file
load_dotenv()


def get_client() -> genai.Client:
    """Create a Gemini API client using the key from .env or Streamlit secrets."""
    api_key = os.getenv("GEMINI_API_KEY")

    # Fallback: check Streamlit secrets (for Streamlit Cloud deployment)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Copy .env.example to .env and add your key."
        )
    return genai.Client(api_key=api_key)


def process_message(message: str, model_name: str = DEFAULT_MODEL) -> dict:
    """
    Run the full AI agent pipeline on a customer message.

    Args:
        message: Raw customer message text.
        model_name: Gemini model to use (default: gemini-2.0-flash).

    Returns:
        dict with keys: classification, extraction, reply, reasoning.
    """
    # Handle edge case: empty or whitespace-only input
    if not message or not message.strip():
        return {
            "classification": {"intent": "unknown", "sentiment": "neutral"},
            "extraction": {
                "customer_name": None,
                "issue_type": "empty message",
                "urgency_level": "Low",
                "recommended_action": "Request the customer to provide more details",
            },
            "reply": "Hello! It seems your message was empty. Could you please share more details so we can assist you?",
            "reasoning": "The input message was empty or contained only whitespace. No classification or extraction could be performed. A polite prompt for more information was generated.",
        }

    # Build the user prompt with the customer message
    user_prompt = USER_PROMPT_TEMPLATE.format(message=message)

    # Create client and send request with JSON output mode
    client = get_client()
    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )

    # Parse and return the structured JSON response
    result = json.loads(response.text)
    return result


if __name__ == "__main__":
    # Quick test with a sample message
    test_msg = "Hi, I have a question about your pricing plans. Can you help?"
    print("Testing pipeline with:", test_msg)
    print(json.dumps(process_message(test_msg), indent=2))
