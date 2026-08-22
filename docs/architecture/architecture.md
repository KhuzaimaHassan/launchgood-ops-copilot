# LaunchGood Ops Copilot — Technical Architecture

**Status:** Proposed architecture baseline v0.1  
**Scope:** Deployed prototype  
**Related product baseline:** `docs/product/PRD.md`, `docs/product/requirements.md`, `docs/product/user-flows.md`

## 1. Architectural intent

LaunchGood Ops Copilot is a small, deployable, human-in-the-loop application. It prepares an evidence-backed case assessment for a reviewer; it does not execute consequential operational actions.

The architecture optimizes for:

- a convincing end-to-end prototype
- explicit AI and human boundaries
- inspectable state and failure handling
- repeatable evaluation
- free-tier compatibility
- a clean path to a stronger production system later

It deliberately avoids microservices, autonomous multi-agent behavior, event streaming, Kubernetes, and paid infrastructure that does not materially improve the demonstration.

## 2. Architectural principles

1. **Human ownership of consequences.** AI can recommend; only the reviewer can finalize a decision.
2. **Structured data at boundaries.** Services exchange typed Pydantic models rather than unvalidated dictionaries or free-form text.
3. **Evidence before recommendation.** The workflow extracts and retrieves supporting information before producing a recommendation.
4. **Uncertainty is explicit.** Missing evidence, conflicts, weak policy retrieval, and invalid model output become visible states.
5. **One workflow, bounded autonomy.** LangGraph provides state, validation, retry, and checkpoint-friendly flow control; it does not orchestrate independent autonomous agents.
6. **Provider replaceability.** LLM and embedding providers are configured behind interfaces.
7. **Prototype-sized infrastructure.** Local files, FAISS, SQLite, and a single web service are acceptable defaults for synthetic data.

## 3. Logical components

```text
┌──────────────────────────────────┐
│ Next.js Operations Command Center│
│ Primary deployed reviewer UI     │
└───────────────┬──────────────────┘
                │ REST/JSON
┌───────────────▼──────────────────┐
│ FastAPI application              │
│ API, validation, case/review     │
│ and evaluation routes            │
└───────┬──────────┬───────────────┘
        │          │
┌───────▼────────┐ └──────────────────────┐
│ Application     │                        │
│ services        │              ┌─────────▼─────────┐
│ case + review   │              │ Persistence       │
└───────┬────────┘              │ SQLite / file     │
        │                       │ audit + eval data │
┌───────▼────────┐              └───────────────────┘
│ LangGraph      │
│ assessment     │
│ workflow       │
└───┬────────┬───┘
    │        │
┌───▼───┐ ┌──▼────────────┐
│ LLM   │ │ RAG service    │
│ adapter│ │ FAISS + policy│
└───────┘ └───────────────┘
```

## 4. Component responsibilities

### Next.js frontend

- renders the production dashboard, case review workspace, and evaluation center
- calls FastAPI through typed REST contracts
- displays source data, AI output, human decisions, and audit history
- never receives provider secrets
- shows explicit offline-demo state when fallback data is used

### Optional Streamlit developer interface

The Streamlit application in `app/ui/streamlit_app.py` is retained for local experimentation, data exploration, and fallback developer workflows. It is not the primary deployed reviewer interface and is not part of the production frontend deployment path.

### FastAPI application

- exposes the stable application boundary
- validates request and response models
- coordinates application services
- translates domain errors into safe API errors
- owns request-level logging and correlation IDs

### Application services

- load and normalize cases
- start and resume analysis
- persist assessments and reviewer decisions
- run evaluation datasets
- keep domain logic independent of frontend frameworks and provider SDKs

### LangGraph workflow

- executes the bounded assessment state machine
- normalizes case signals
- formulates a policy query
- retrieves and grades policy context
- generates and validates structured assessment output
- detects uncertainty/conflicts
- retries bounded failures
- returns a typed failure or review-required result when it cannot produce a safe assessment

### RAG service

- builds or loads the policy index
- retrieves policy chunks and metadata
- labels strong, weak, and no-match retrieval
- never invents policy content

### Persistence

- SQLite is the default prototype database
- JSON/CSV fixtures provide synthetic seed data
- FAISS index and policy metadata are stored as deployable artifacts
- repository interfaces leave a path to PostgreSQL without requiring it for the prototype

## 5. Trust boundaries

| Boundary | Required control |
|---|---|
| Browser → API | request validation; no secrets in client |
| API → workflow | typed case input; correlation ID |
| Workflow → LLM | structured schema; bounded request limits |
| Workflow → RAG | normalized query; retrieval metadata retained |
| AI output → reviewer | schema validation; evidence and uncertainty visible |
| Reviewer → persistence | explicit decision payload; immutable AI output |
| Application → logs | redact secrets and avoid real PII |

## 6. Deployment shape

The deployed prototype uses a lightweight split:

- Next.js frontend hosted on a free-tier frontend platform (e.g. Vercel)
- FastAPI backend hosted as the root application service

Streamlit remains an optional local developer/data-exploration interface and is not required for the production deployment.

The system must work with synthetic data, environment-based configuration, a configurable LLM provider, a local policy index, and bounded request volume.

## 7. Quality attributes

### Reliability

Invalid model output, provider failure, missing input, and retrieval failure produce visible recoverable states. The system never saves an unvalidated assessment as successful.

### Explainability

The reviewer sees evidence references, retrieved policy sources, confidence, uncertainty flags, and the distinction between AI and human decisions.

### Maintainability

Domain models, repositories, provider adapters, workflow nodes, and API routes remain independently testable.

### Cost control

Use local embeddings, cached policy indexes, small synthetic fixtures, bounded LLM calls, and no always-on supporting services beyond the application database.

## 8. Out of scope

- real LaunchGood integrations
- autonomous campaign or account actions
- real financial operations
- production authentication and organization-wide authorization
- multi-region availability
- enterprise observability platforms
- online model training
