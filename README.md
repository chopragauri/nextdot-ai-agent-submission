# Mini AI Agent That Thinks Out Loud

An AI-powered customer message analysis pipeline that classifies, extracts structured data, generates empathetic replies, and explains its own reasoning — all driven by an LLM with no hardcoded logic.

Built for the **Nextdot AI Engineering Internship** assignment.

## Features

- **4-step pipeline**: Classify → Extract → Reply → Explain
- **Structured JSON output** via Gemini's native JSON mode
- **Streamlit web UI** with live message analysis
- **Dual-model comparison** (Gemini 2.0 Flash vs 2.5 Flash)
- **Edge case handling**: empty input, short messages, Hindi/Hinglish

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nextdot-ai-agent.git
cd nextdot-ai-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

```bash
cp .env.example .env
```

Edit `.env` and add your [Google Gemini API key](https://aistudio.google.com/apikey):

```
GEMINI_API_KEY=your_actual_key_here
```

## Usage

### Run on the 3 sample inputs (generates output JSONs)

```bash
python run_samples.py
```

This creates `outputs/output_A.json`, `output_B.json`, and `output_C.json`.

### Launch the Streamlit web UI

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

### Test with a custom message (CLI)

```bash
python agent.py
```

## Project Structure

```
├── agent.py           # Core pipeline — LLM call + JSON parsing
├── app.py             # Streamlit web interface
├── config.py          # Model configuration
├── prompts.py         # Centralized LLM prompts
├── sample_inputs.py   # The 3 sample customer messages
├── run_samples.py     # Script to run samples and save outputs
├── outputs/           # Generated JSON outputs
├── requirements.txt   # Python dependencies
├── THINKING.md        # Reflection on approach and decisions
├── .env.example       # API key template
└── .gitignore         # Keeps .env out of git
```

## Tech Stack

- **Python 3.10+**
- **Google Gemini API** (gemini-2.0-flash) — free tier
- **Streamlit** — web UI
- **python-dotenv** — environment variable management
