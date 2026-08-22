# LaunchGood Ops Copilot

Executive Human-in-the-Loop AI Operations Command Center for reviewing synthetic campaign compliance, risk signals, and policy grounding.

> **Core Principle:** *"AI prepares the decision; humans own the consequence."*

---

## Architecture Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                 Next.js 14 Frontend                         │
│   (Command Center Dashboard • Case Review • Evaluation)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST + CORS (JSON)
┌──────────────────────────────▼──────────────────────────────┐
│                    FastAPI Backend                          │
│   (CaseService • AnalysisService • DecisionService)         │
└──────┬───────────────────────┬───────────────────────┬──────┘
       │                       │                       │
┌──────▼──────┐         ┌──────▼──────┐         ┌──────▼──────┐
│  LangGraph  │         │  Local RAG  │         │   SQLite    │
│  Workflow   │         │ Cosine/FAISS│         │ Repository  │
└─────────────┘         └─────────────┘         └─────────────┘
```

> [!NOTE]
> **Prototype Provider Scope:** Only the deterministic mock provider (`LLM_PROVIDER=mock`) is currently active for zero-cost prototype verification. Reserved live provider names (`openai`, `anthropic`, `gemini`) validate `LLM_API_KEY` configuration and raise `NotImplementedError` until live SDK adapters are installed.

---

## Quickstart

### 1. Backend Service (FastAPI)
```bash
# Set up virtual environment
python -m venv .venv
.venv\Scripts\activate
pip install -e .[api,ui,dev]
copy .env.example .env

# Launch FastAPI server
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```
Verify:
```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### 2. Frontend Command Center (Next.js 14)
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Features & Review Workspace

1. **Operations Command Center (`/`):**
   - Real-time KPI metric tiles: *Needs Review*, *High Risk*, *Avg Confidence*, *Estimated Time Saved*.
   - Filter chips: *Needs Attention*, *Pending*, *Awaiting Decision*, *Resolved*.
   - Interactive 2-column Case Cards grid with one-click review navigation.

2. **3-Zone Case Review Workspace (`/cases/[id]`):**
   - **Zone 1: Executive Case Header:** Risk level, Priority, Category, and Confidence score + tier, with one-click "Run AI Assessment" trigger.
   - **Zone 2: Tabbed Evidence & Context Workspace:**
     - *Evidence Tab:* Specific supporting facts and source ID provenance.
     - *Retrieved Policies Tab:* Grounding status (`STRONG`/`WEAK`), similarity score, and excerpts.
     - *Source Timeline Tab:* Visual chronological feed of campaign creation, messages, updates, and risk signals.
     - *Uncertainty & Conflicts Tab:* High-contrast warning banners for `CONFLICTING_EVIDENCE` or zero policy matches.
   - **Zone 3: Persistent Human Decision Rail:**
     - Reviewer controls for `APPROVE`, `MODIFY`, `REJECT`, `ESCALATE`, optional overrides, and reviewer notes.
   - **Zone 4: Immutable Audit Trail:**
     - Chronological event timeline with an expandable raw JSON technical drawer.

3. **Evaluation & Quality Center (`/evaluation`):**
   - One-click execution of the 5-scenario synthetic benchmark.
   - Transparent reporting across Category, Action, Escalation, Risk, and Priority agreement.
   - Root-cause diagnostics explaining why the 80% risk score is a safety asset.

---

## 100% Free-Tier Deployment

- **Frontend:** Deploy `frontend/` to [Vercel](https://vercel.com) (100% free Next.js hosting, 1-click GitHub import). Set `NEXT_PUBLIC_API_URL` to your FastAPI backend URL.
- **Backend:** Deploy the root Docker container to [Render](https://render.com) or [Railway](https://railway.app) (Free Web Service).

---

## Documentation

Comprehensive engineering documentation is available under [`docs/`](docs/README.md):
- [`PRD.md`](docs/product/PRD.md) & [`requirements.md`](docs/product/requirements.md)
- [`decision-log.md`](docs/product/decision-log.md) (Decisions D-001 through D-009)
- [`architecture.md`](docs/architecture/architecture.md) & [`ADR-001`](docs/architecture/adr/ADR-001-architecture-style.md)
- [`ai-workflow.md`](docs/architecture/ai-workflow.md) & [`rag-design.md`](docs/architecture/rag-design.md)
- [`evaluation.md`](docs/ai/evaluation.md) & [`failure-cases.md`](docs/testing/failure-cases.md)
- [`demo-checklist.md`](docs/deployment/demo-checklist.md) (5-Minute video script)
