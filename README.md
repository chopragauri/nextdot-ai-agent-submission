# Mini AI Agent That Thinks Out Loud

An AI-powered customer message analysis pipeline that classifies, extracts structured data, generates empathetic replies, and explains its own reasoning — all driven by an LLM with no hardcoded logic.

**Live Demo:** [Streamlit Cloud App](https://chopragauri-nextdot-ai-agent-submission-app-znyb14.streamlit.app/)

## Features

- **4-step pipeline**: Classify → Extract → Reply → Explain Reasoning
- **Structured JSON output** via Gemini's native JSON mode — no regex parsing
- **Streamlit web UI** with live message analysis
- **Interactive CLI** for terminal-based testing
- **Dual-model comparison** — run two Gemini models side-by-side on the same input
- **Edge case handling** — empty input, short messages, Hindi/Hinglish
- **Retry logic** with response validation for production reliability

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/chopragauri/nextdot-ai-agent-submission.git
cd nextdot-ai-agent-submission
```

### 2. Create a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

**macOS / Linux:**
```bash
cp .env.example .env
```

**Windows (Command Prompt):**
```bash
copy .env.example .env
```

Edit `.env` and add your [Google Gemini API key](https://aistudio.google.com/apikey) (free tier works):

```
GEMINI_API_KEY=your_actual_key_here
```

## Usage

### Run on the 3 sample inputs (generates output JSONs)

```bash
python3 run_samples.py        # macOS / Linux
python run_samples.py         # Windows
```

This processes all 3 sample customer messages and saves results to `outputs/output_A.json`, `output_B.json`, and `output_C.json`.

### Launch the Streamlit web UI

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

### Interactive CLI

```bash
python3 cli.py                # macOS / Linux
python cli.py                 # Windows
```

Type any customer message and see the structured analysis in real-time.

## Project Structure

```
├── agent.py           # Core pipeline — LLM call, retry logic, response validation
├── app.py             # Streamlit web interface with dual-model comparison
├── cli.py             # Interactive CLI for terminal-based testing
├── config.py          # Model configuration and constants
├── prompts.py         # Centralized LLM prompts (all prompt engineering lives here)
├── sample_inputs.py   # The 3 sample customer messages from the brief
├── run_samples.py     # Script to process all samples and save output JSONs
├── outputs/           # Generated JSON outputs for all 3 sample inputs
├── requirements.txt   # Python dependencies
├── THINKING.md        # Reflection on approach, decisions, and trade-offs
├── .env.example       # API key template
└── .gitignore         # Keeps .env and venv out of git
```

## Tech Stack

- **Python 3.9+**
- **Google Gemini API**  — free tier
- **Streamlit** — web UI + cloud deployment
- **python-dotenv** — environment variable management
