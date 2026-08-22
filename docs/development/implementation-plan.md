# Implementation Plan

**Status:** Approved sequencing plan v0.1

## Phase 0 — Contracts

- create typed domain enums/models
- create synthetic fixture format
- add configuration model
- add fake provider interfaces

## Phase 1 — Data and repositories

- seed cases, source records, and policies
- implement SQLite/file repositories
- implement provenance and audit persistence

## Phase 2 — RAG

- parse policy fixtures
- chunk and embed policies
- build FAISS index
- implement retrieval and grounding labels

## Phase 3 — AI workflow

- implement LangGraph nodes
- add structured output validation
- add retry/repair and uncertainty rules
- persist assessment versions

## Phase 4 — API and review flow

- implement case, analysis, assessment, decision, audit, and evaluation routes
- enforce state transitions in services
- add API contract tests

## Phase 5 — Next.js Operations Command Center

- build the primary deployed Next.js 14 App Router frontend
- implement the executive dashboard with KPI cards and composable filters
- implement the three-zone case review workspace
- display evidence, policy grounding, source timeline, and uncertainty warnings
- implement the persistent human decision rail
- implement evaluation metrics and structured failure reporting
- integrate the frontend with FastAPI through typed REST contracts
- retain `app/ui/streamlit_app.py` as an optional developer/data-exploration tool

## Phase 6 — Evaluation and hardening

- execute baseline dataset
- inspect difficult cases
- fix grounding and validation failures
- document known limitations

## Phase 7 — Deployment and demo

- deploy the Next.js frontend to a free-tier frontend host
- deploy the FastAPI backend using the root application container
- configure `NEXT_PUBLIC_API_URL`, CORS, database, provider, and RAG settings
- verify frontend-to-backend health and workflow behavior
- run the deployed smoke test
- record the five-minute walkthrough

Each phase should leave the application runnable and should not introduce unrelated infrastructure.
