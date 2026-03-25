"""
Run the AI agent pipeline on all three sample inputs and save outputs as JSON files.
Usage: python run_samples.py
"""

import json
import os

from agent import process_message
from sample_inputs import SAMPLES


def main():
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    for key, sample in SAMPLES.items():
        print(f"\n{'='*60}")
        print(f"Processing Input {key}: {sample['label']}")
        print(f"{'='*60}")
        print(f"Message: {sample['message'][:80]}...")

        # Run the pipeline
        result = process_message(sample["message"])

        # Save to JSON file
        output_path = os.path.join(output_dir, f"output_{key}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Saved to: {output_path}")
        print(f"Intent: {result['classification']['intent']}")
        print(f"Sentiment: {result['classification']['sentiment']}")
        print(f"Urgency: {result['extraction']['urgency_level']}")

    print(f"\n{'='*60}")
    print("All outputs saved to the outputs/ directory.")


if __name__ == "__main__":
    main()
