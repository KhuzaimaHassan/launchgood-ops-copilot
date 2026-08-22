# ADR-001 — Modular Monolith Architecture

**Status:** Accepted  
**Date:** 2026-08-18

## Context

The prototype needs a real API, UI, workflow, persistence, RAG, auditability, and evaluation while remaining deployable on free-tier infrastructure.

## Decision

Use a clean service-oriented architecture with a modern Next.js (React + Tailwind CSS + TypeScript) frontend, a typed FastAPI backend service, one bounded LangGraph workflow, provider adapters, and repository interfaces. The frontend communicates with FastAPI over REST with full CORS support. Streamlit is preserved as an optional developer/data exploration script.

## Consequences

- Next.js delivers a responsive, high-contrast, executive-ready Operations Command Center with zero page-rerun layout glitches.
- FastAPI backend serves as the single source of truth for business logic, RAG retrieval, LangGraph orchestration, and SQLite persistence.
- Free-tier deployment is straightforward: Next.js on Vercel (100% free), FastAPI on Render/Railway/Fly.io.
- Local development is simple: `uvicorn app.api.main:app` + `npm run dev` in `frontend/`.

## Rejected alternatives

Microservices, Kubernetes, event streaming, and multiple always-on workers add operational cost without improving the prototype enough.
