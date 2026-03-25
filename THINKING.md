# THINKING.md

## Model Choice

I went with **Google Gemini 2.5 Flash** because it's free (no credit card needed), fast enough for real-time use, and supports **native JSON output mode**. The JSON mode was the biggest factor — I just set `response_mime_type="application/json"` in the API call and the model always returns clean, valid JSON. No regex parsing, no hoping the output is formatted correctly. I initially used `gemini-2.0-flash` but hit the free-tier rate limit quickly during testing, so I moved to `2.5-flash` which had a separate quota. I also used the newer `google-genai` SDK since the older `google-generativeai` package has been deprecated by Google.

## Prompting Strategy

The assignment has four steps — classify, extract, generate a reply, and explain the reasoning. I used a **single prompt** that handles all four steps at once and returns one JSON object, instead of making four separate API calls.

This made more sense for a few reasons. First, the steps are connected — the classification directly affects the tone of the reply, and the reasoning needs to reference the classification. If I split them into separate calls, each step would lose context from the others. Second, one call is faster and uses less API quota than four. And third, it kept the code simpler — one function call, one response, one validation step.

The prompt itself took the most iteration. Early versions were too vague, so I kept refining it — adding explicit definitions for every allowed value, including a few-shot example to anchor the format, and writing specific instructions for edge cases like empty messages, short inputs, and Hindi/Hinglish text.

## What Broke and How I Fixed It

**The model kept returning wrong urgency values.** Instead of sticking to Low, Medium, High, and Critical, it would make up its own labels like "Moderate" or "Urgent." I fixed this by adding concrete definitions in the prompt — for example, "Low = general question, no time pressure" and "Critical = threatening to leave, requesting a refund, or mentioning legal action." Once the model understood what each level actually meant, it picked the right one consistently.

**Empty messages caused errors.** Sending an empty string to the API gave unpredictable results, so I added a check in Python that catches empty input before it ever reaches the API.

**API rate limits during testing.** I burned through the `gemini-2.0-flash` quota while iterating on the prompt. Switching to `2.5-flash` gave me a fresh quota to work with.

**Generic replies.** The model kept writing bland, template-sounding responses — things like "we value your feedback." I fixed this by explicitly telling it to avoid generic phrases and to reference specific details from the customer's message instead.

**API key not found on Streamlit Cloud.** The `.env` file is in `.gitignore` so the key doesn't get pushed to GitHub, which means it's not available when deployed. I added a fallback — the code checks `.env` first, and if that's missing, it reads from `st.secrets` (Streamlit's built-in secrets manager).

## What I'd Improve With More Time

- **Caching** — store results so repeated messages don't waste API quota
- **Unit tests** — test the validation and error handling with mocked API responses instead of making real calls
- **History feature** in the Streamlit UI — let users save past analyses and compare them side by side
- **More few-shot examples** in the prompt — giving the model 2-3 real examples instead of just one would improve consistency
- **Broader language support** — right now it handles English and Hindi/Hinglish, but extending it to other regional languages like Tamil, Bengali, or Marathi would make it more useful in a real Indian customer support setting
- **Multi-turn conversation** — let the agent ask follow-up questions instead of treating each message in isolation
