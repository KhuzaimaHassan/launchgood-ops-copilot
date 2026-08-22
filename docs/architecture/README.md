# Architecture Documentation

This layer translates the approved product baseline into an implementation-ready technical design.

## Documents

- [`architecture.md`](architecture.md) — architecture principles, components, boundaries, and quality attributes
- [`system-design.md`](system-design.md) — runtime flow, API surface, state transitions, persistence, and failure handling
- [`data-model.md`](data-model.md) — entities, fields, relationships, auditability, and evaluation fixtures
- [`ai-workflow.md`](ai-workflow.md) — bounded LangGraph workflow, state, structured output, and uncertainty behavior
- [`rag-design.md`](rag-design.md) — policy ingestion, indexing, query formulation, retrieval, grounding, and evaluation

### Decision records

The [`adr/`](adr/) directory contains ADR-001 through ADR-005, all approved and accepted as the active architecture baseline.

## Approved implementation direction

```text
Next.js Operations Command Center → FastAPI
                                  → application services
                                  → one LangGraph workflow
                                       ├→ LLM provider adapter
                                       ├→ FAISS RAG adapter
                                       └→ SQLite/file repositories
```

Streamlit is retained under `app/ui/` only as an optional developer/data-exploration script. The design is intentionally a modular monolith split into a Next.js 14 frontend and FastAPI backend for the deployed prototype. ADR-001 through ADR-005 are the active accepted decisions for architecture style, orchestration, RAG storage, LLM strategy, and deployment.
