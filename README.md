# AI-Powered Health Management System

An AI-driven Streamlit app that:
1. Generates personalized meal plans from a user profile.
2. Analyzes food images to provide nutrition estimates.
3. Answers health queries using Gemini 1.5 Flash.

## Repo structure
```
ai-health-manager/
├─ .github/
│  └─ workflows/ci.yml
├─ .env.example
├─ README.md
├─ requirements.txt
├─ app.py
├─ gemini_client.py
├─ utils.py
├─ .gitignore
├─ assets/
└─ models/
```

## Quickstart (local)
1. Clone the repo
2. Create a virtualenv and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set your `GEMINI_API_KEY`:
   ```
   cp .env.example .env
   # edit .env and add your key
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Deployment
- Add `GEMINI_API_KEY` to your deployment platform's secrets (Streamlit Cloud, Render, Heroku, etc.).
- For production, add persistent storage (Postgres / S3) and authentication.

## Notes
- This project uses `gemini-1.5-flash` (multimodal) via the Google Generative AI Python SDK.
- Gemini outputs are estimates and should not be used as clinical medical advice.
