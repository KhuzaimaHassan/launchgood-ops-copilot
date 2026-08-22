# LaunchGood Ops Copilot

Executive Human-in-the-Loop AI Operations Command Center for reviewing synthetic campaign compliance, risk signals, and policy grounding.

> **Core Principle:** *"AI prepares the decision; humans own the consequence."*

---

## 🌐 Live Deployed Application

- **Live Operations Command Center (Vercel):** [https://launchgood-ops-copilot.vercel.app/](https://launchgood-ops-copilot.vercel.app/)
- **Live FastAPI Backend & API Docs (Render):** [https://launchgood-ops-copilot-m9jo.onrender.com/health](https://launchgood-ops-copilot-m9jo.onrender.com/health)

> [!NOTE]
> **Free-Tier Ephemeral Persistence Note:** On Render free-tier hosting, SQLite database storage is instance-bound and resets when the container restarts. Within a running instance lifetime, all decisions and audit events persist live across requests.

---

## 📸 Live Visual Operations Walkthrough

### 1. Operations Command Center (`/`)
*Real-time executive KPI metrics (*Needs Review*, *High Risk*, *Avg Confidence*, *Est. Time Saved*), composable filtering, active reviewer queue, and live API connection status.*

![Command Center Dashboard](docs/assets/screenshots/01-command-center-dashboard.png)

---

### 2. Case Review Workspace (`/cases/case-1001`)
*Executive Header (Risk, Priority, Category), tabbed evidence & context workspace, and verified LaunchGood RAG policy grounding citations.*

![Case Review Workspace](docs/assets/screenshots/02-case-1001-review-workspace.png)

---

### 3. Conflicting Evidence Warning (`/cases/case-1003`)
*High-contrast warning banner highlighting conflicting campaign details vs updates, requiring mandatory human override review.*

![Conflicting Evidence Banner](docs/assets/screenshots/03-case-1003-conflicting-evidence.png)

---

### 4. Citation Safety & Policy Fallback (`/cases/case-1004`)
*Explicit `NO_APPLICABLE_POLICY` grounding banner preventing hallucinated policy compliance citations.*

![No Policy Match Citation Safety](docs/assets/screenshots/04-case-1004-no-policy-grounding.png)

---

### 5. Persistent Decision Rail & Immutable Audit Trail
*Human reviewer controls (`APPROVE`, `MODIFY`, `REJECT`, `ESCALATE`), overrides, reviewer notes, and append-only audit timeline.*

![Decision Rail and Audit Timeline](docs/assets/screenshots/05-decision-rail-submission.png)

---

### 6. Evaluation & Quality Benchmark Center (`/evaluation`)
*One-click 5-scenario benchmark execution reporting agreement metrics across Category, Action, Escalation, Risk, and Priority.*

![Evaluation Benchmark Center](docs/assets/screenshots/06-evaluation-benchmark.png)

---

### 7. Responsive Layout Viewports (Tablet & Mobile)
*Zero horizontal overflow, collapsible stacks, and persistent decision rail accessibility across all screen sizes.*

#### Tablet Viewport (`1024 × 768`)
![Tablet Viewport (1024x768)](docs/assets/screenshots/07-responsive-tablet-1024x768.png)

#### Mobile Viewport (`390 × 844`)
![Mobile Viewport (390x844)](docs/assets/screenshots/08-responsive-mobile-390x844.png)

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

## Documentation

Comprehensive engineering documentation is available under [`docs/`](docs/README.md):
- [`PRD.md`](docs/product/PRD.md) & [`requirements.md`](docs/product/requirements.md)
- [`decision-log.md`](docs/product/decision-log.md) (Decisions D-001 through D-009)
- [`architecture.md`](docs/architecture/architecture.md) & [`ADR-001`](docs/architecture/adr/ADR-001-architecture-style.md)
- [`ai-workflow.md`](docs/architecture/ai-workflow.md) & [`rag-design.md`](docs/architecture/rag-design.md)
- [`evaluation.md`](docs/ai/evaluation.md) & [`failure-cases.md`](docs/testing/failure-cases.md)
- [`demo-checklist.md`](docs/deployment/demo-checklist.md) (5-Minute video script)
