# Development Setup

**Status:** Proposed implementation baseline v0.1

## 1. Expected local prerequisites

- Python 3.11 or the version selected by deployment
- Git
- a virtual environment tool
- access to the configured LLM provider only when running live analysis

The application must also support a no-network test mode using fixtures and a fake provider.

## 2. Configuration categories

Configuration belongs in environment variables or a local untracked `.env` file. Never commit secrets.

```text
APP_ENV=development
DATABASE_URL=sqlite:///./data/app.db
LLM_PROVIDER=mock|configured_provider
LLM_MODEL=...
LLM_API_KEY=...
EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=...
RAG_INDEX_PATH=...
CONFIDENCE_HIGH_THRESHOLD=...
CONFIDENCE_MEDIUM_THRESHOLD=...
MAX_ANALYSIS_RETRIES=...
```

The exact provider names are implementation choices; the configuration contract should remain stable.

## 3. Local workflow

### Backend (FastAPI + LangGraph + SQLite)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[api,ui,dev]
copy .env.example .env
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

### Frontend (Next.js 14 App Router)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to access the Operations Command Center.

### Running Tests
```bash
pytest
```
