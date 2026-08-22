# Deployment Guide

**Target:** free-tier-compatible hosted prototype

## 1. Deployment shape

Prefer one lightweight deployable service or the smallest provider-supported split. The service must expose the API/UI entry point and persist synthetic data and index artifacts in the selected supported manner.

## 1.1 Frontend and backend responsibilities

The deployed application consists of two lightweight services:

- `frontend/`: Next.js 14 App Router production frontend (e.g., hosted on Vercel)
- root application: FastAPI backend, workflow, RAG, repositories, and API routes (e.g., hosted on Render, Railway, or Fly.io)

The Streamlit script (`app/ui/streamlit_app.py`) is an optional developer exploration tool and is not required for the deployed reviewer experience.

## 2. Release checklist

- install from pinned dependencies
- seed only synthetic cases/policies
- build/load the versioned FAISS index
- set provider secrets in the hosting platform
- set production configuration values
- verify `/health`
- run one clear case and one difficult case
- verify reviewer decision and audit event
- run basic evaluation
- confirm no secret appears in logs or UI

## 3. Smoke test

1. open public URL
2. confirm dashboard loads
3. open a `PENDING_ANALYSIS` case
4. run analysis
5. inspect evidence, policy, confidence, and flags
6. submit `MODIFY` with reviewer notes
7. confirm AI and human values remain distinct
8. inspect audit record
9. run evaluation and inspect a failure case

## 4. Prototype limitations

The deployment is not production-ready for real user data, real financial operations, or unattended high-volume use. These limitations must be visible in submission/demo documentation.
