# ADR-003 — Local FAISS Policy Index

**Status:** Accepted  
**Date:** 2026-08-18

## Context

The knowledge base is small, synthetic, and primarily used to demonstrate grounding. A hosted vector database would add cost and configuration burden.

## Decision

Use local Sentence Transformers embeddings where practical, a persisted FAISS index, and JSON metadata. Version the corpus, chunking configuration, embedding model, and index.

## Consequences

Retrieval is inexpensive and reproducible for the prototype. It is not a multi-tenant or horizontally scalable vector architecture. Thresholds remain configurable and are calibrated through evaluation.

## Rejected alternatives

Hosted vector databases and external rerankers are deferred until retrieval quality or scale demonstrates a need.
