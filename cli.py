"""
Interactive CLI for the AI Agent pipeline.
Type any customer message and see the structured analysis in real-time.
Usage: python cli.py
"""

import json
import sys

from agent import process_message
from config import DEFAULT_MODEL


def print_section(title: str, content: str):
    """Print a formatted section with a header."""
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")
    print(content)


def display_result(result: dict):
    """Pretty-print the pipeline output in the terminal."""
    c = result["classification"]
    e = result["extraction"]

    # Urgency indicators
    urgency_icons = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
    urgency_icon = urgency_icons.get(e["urgency_level"], "⚪")

    print_section(
        "CLASSIFICATION",
        f"  Intent:    {c['intent'].upper()}\n"
        f"  Sentiment: {c['sentiment'].upper()}"
    )

    print_section(
        "EXTRACTED FIELDS",
        f"  Customer:  {e['customer_name'] or 'Not provided'}\n"
        f"  Issue:     {e['issue_type']}\n"
        f"  Urgency:   {urgency_icon} {e['urgency_level']}\n"
        f"  Action:    {e['recommended_action']}"
    )

    print_section("GENERATED REPLY", f"  {result['reply']}")
    print_section("MODEL'S REASONING", f"  {result['reasoning']}")


def main():
    print("=" * 50)
    print("  🧠 Mini AI Agent — Interactive CLI")
    print(f"  Model: {DEFAULT_MODEL}")
    print("=" * 50)
    print("Type a customer message and press Enter.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            message = input("📩 Customer message: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if not message:
            print("⚠️  Empty message. Please type something.\n")
            continue

        print(f"\n⏳ Analyzing with {DEFAULT_MODEL}...")
        try:
            result = process_message(message)
            display_result(result)
        except RuntimeError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

        print()  # blank line before next input


if __name__ == "__main__":
    main()
