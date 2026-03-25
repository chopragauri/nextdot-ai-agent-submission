# THINKING.md

## Model Choice

I chose **Google Gemini 2.5 Flash** for three reasons: it's free-tier friendly (no billing required to get started), it natively supports **JSON output mode** (`response_mime_type="application/json"`), and it's fast enough for interactive use in a Streamlit UI. JSON mode was the deciding factor — it guarantees structurally valid JSON on every call, eliminating the need for regex parsing or retry logic that would add fragile complexity. I used the newer `google-genai` SDK instead of the deprecated `google-generativeai` package.

## Prompting Strategy

I used a **single structured prompt** rather than making four separate LLM calls (one per pipeline step). This keeps the context coherent — the model's classification directly informs its tone selection for the reply, and its reasoning references decisions made in earlier steps. The prompt explicitly defines the JSON schema, enumerates valid values for each field (e.g., intent must be one of complaint/query/feedback/request), and includes tone-matching rules tied to sentiment. I also added edge case instructions for empty inputs, very short messages, and non-English text so the model handles them gracefully rather than producing garbage output.

## What Broke and How I Fixed It

Early iterations had the model occasionally returning urgency levels like "Moderate" instead of the specified "Medium". Adding an explicit mapping with definitions (Low = casual inquiry, Medium = standard question, High = frustrated customer, Critical = threatening action) in the prompt fixed the consistency. I also had to handle the empty-input edge case in Python rather than relying on the LLM, since sending an empty string to the API would sometimes produce unpredictable results.

## What I Would Improve With More Time

I would add **input validation and error handling** around the API call (rate limits, network failures) with exponential backoff. I'd also build a **logging system** that saves every pipeline run with timestamps for auditability. Adding **unit tests** with mocked API responses would make the pipeline more robust. Finally, I'd explore **few-shot prompting** — embedding 2-3 example input/output pairs directly in the prompt to further improve consistency across edge cases.
