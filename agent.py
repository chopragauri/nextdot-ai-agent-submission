"""
Core AI Agent Pipeline
Processes customer messages through 4 steps: Classify, Extract, Generate Reply, Explain Reasoning.
All steps are handled by the LLM in a single structured call — no hardcoded logic.
"""

import json
import os
import time

from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import DEFAULT_MODEL
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Load API key from .env file
load_dotenv()

# Expected keys in the pipeline output — used for validation
EXPECTED_KEYS = {"classification", "extraction", "reply", "reasoning"}
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 3


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


def validate_response(result: dict) -> bool:
    """Check that the LLM response has all required keys and valid values."""
    if not isinstance(result, dict):
        return False
    if not EXPECTED_KEYS.issubset(result.keys()):
        return False

    # Validate classification values
    classification = result.get("classification", {})
    valid_intents = {"complaint", "query", "feedback", "request", "unknown"}
    valid_sentiments = {"positive", "neutral", "negative", "urgent"}
    if classification.get("intent") not in valid_intents:
        return False
    if classification.get("sentiment") not in valid_sentiments:
        return False

    # Validate extraction fields exist
    extraction = result.get("extraction", {})
    if "urgency_level" not in extraction or "recommended_action" not in extraction:
        return False

    return True


def process_message(message: str, model_name: str = DEFAULT_MODEL) -> dict:
    """
    Run the full AI agent pipeline on a customer message.

    Sends the message to the LLM with a structured prompt and returns
    the classified, extracted, and generated response as a dict.

    Args:
        message: Raw customer message text.
        model_name: Gemini model to use (default: gemini-2.5-flash).

    Returns:
        dict with keys: classification, extraction, reply, reasoning.

    Raises:
        RuntimeError: If the LLM fails after all retries.
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
    client = get_client()

    # Retry loop — handles transient API errors and malformed responses
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.7,
                ),
            )

            result = json.loads(response.text)

            # Validate the response structure before returning
            if validate_response(result):
                return result
            else:
                last_error = "Response missing required fields or has invalid values"
                print(f"[Attempt {attempt + 1}] Validation failed: {last_error}")

        except json.JSONDecodeError as e:
            last_error = f"JSON parse error: {e}"
            print(f"[Attempt {attempt + 1}] {last_error}")
        except Exception as e:
            last_error = str(e)
            print(f"[Attempt {attempt + 1}] API error: {last_error}")

        # Wait before retrying (skip delay on last attempt)
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError(
        f"Pipeline failed after {MAX_RETRIES + 1} attempts. Last error: {last_error}"
    )


if __name__ == "__main__":
    # Quick test with a sample message
    test_msg = "Hi, I have a question about your pricing plans. Can you help?"
    print("Testing pipeline with:", test_msg)
    print(json.dumps(process_message(test_msg), indent=2))
