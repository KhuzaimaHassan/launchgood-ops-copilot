# LaunchGood Ops Copilot — System Design

**Status:** Proposed architecture baseline v0.1

## 1. Runtime request flow

```text
Reviewer
   ↓
Next.js 14 Operations Command Center
   ↓ REST + JSON
FastAPI REST route
   ↓
Application service
   ↓
Repository / workflow / evaluation service
```

## 2. Application modules

```text
frontend/
└── src/
    ├── app/           # Next.js App Router pages (Command Center, Case Review, Evaluation)
    ├── components/    # Executive Dashboard, Review Workspace, Decision Rail, Timelines
    ├── lib/           # REST API client
    └── types/         # Frontend API contracts

app/
├── api/               # FastAPI routes and dependency wiring
├── domain/            # Pydantic models, enums, state transitions
├── services/          # case, assessment, decision, evaluation services
├── workflow/          # LangGraph state and nodes
├── rag/               # indexing, retrieval, relevance grading
├── providers/         # LLM and embedding adapters
├── repositories/      # SQLite/file repositories and interfaces
├── ui/                # Optional Streamlit developer/data exploration script
└── config/            # environment-backed settings
```

The exact source tree may vary, but responsibilities should remain separated.

## 3. API surface

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | liveness/readiness check |
| GET | `/cases` | list cases with intake/status metadata |
| GET | `/cases/{case_id}` | retrieve source data and latest assessment |
| POST | `/cases/{case_id}/analysis` | start or rerun bounded analysis |
| GET | `/cases/{case_id}/assessment` | retrieve latest assessment and provenance |
| POST | `/cases/{case_id}/decision` | save explicit human decision/overrides |
| GET | `/cases/{case_id}/audit` | retrieve audit events |
| POST | `/evaluation/runs` | run the synthetic evaluation dataset |
| GET | `/evaluation/runs/{run_id}` | retrieve metrics and failure cases |

Routes return typed JSON models and a correlation/request ID. Hosted execution may return a run ID and be polled; local development may return the completed result directly.

## 4. Case state transitions

### Product-facing states

```text
PENDING_ANALYSIS → AWAITING_HUMAN_DECISION → RESOLVED
                                         └→ ESCALATED
```

### Internal execution states

```text
PENDING_ANALYSIS → ANALYZING
ANALYZING → AWAITING_HUMAN_DECISION
ANALYZING → NEEDS_REVIEW
ANALYZING → FAILED
AWAITING_HUMAN_DECISION → RESOLVED | ESCALATED
```

State transition rules belong in one domain service. UI code must not mutate status directly.

## 5. Analysis idempotency

Each analysis request gets an `analysis_run_id`. A rerun creates a new assessment version and audit event; it does not overwrite the prior AI assessment. The latest successful assessment is shown by default, while previous runs remain inspectable.

If an identical completed run is reused, the service may return the cached result to control cost, but the UI must label it as cached.

## 6. Error handling

| Error | System behavior | Reviewer-visible result |
|---|---|---|
| Missing case fields | stop before LLM call | missing-information flags |
| LLM timeout/rate limit | bounded retry with backoff | retryable failure |
| Invalid structured output | repair/retry, then stop | `NEEDS_REVIEW` or `FAILED` |
| RAG index unavailable | do not claim policy grounding | policy retrieval unavailable |
| Weak policy match | continue with explicit flag | weak/partial grounding |
| Database write failure | do not report success | save failure and retry option |
| Unexpected exception | log correlation ID, safe error | recoverable application error |

## 7. Persistence strategy

The repository layer supports SQLite for operational prototype records, JSON/CSV for seed/evaluation fixtures, and FAISS plus JSON metadata for policy retrieval. No component should depend directly on SQL statements or filesystem paths outside its repository/adapter.

A PostgreSQL repository can be added later without changing API or workflow contracts.

## 8. Security and privacy posture

- synthetic data is mandatory for the prototype
- provider keys are server-side environment variables
- secrets are never committed or returned through API responses
- logs redact tokens, keys, and message contents where practical
- authentication and authorization are explicit future seams, not hidden assumptions
- the product clearly labels all data as synthetic/mock

## 9. Observability for the prototype

Structured application logs should include timestamp, request ID, case ID, analysis run ID, workflow node/status, duration, and provider error category. Do not add a paid tracing platform; local logs and persisted audit events are sufficient for the demonstration.
