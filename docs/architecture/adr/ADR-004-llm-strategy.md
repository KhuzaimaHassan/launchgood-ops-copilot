# ADR-004 — Configurable LLM Provider Adapter

**Status:** Accepted  
**Date:** 2026-08-18

## Context

Provider cost, availability, structured-output support, and free-tier limits may change during development. Product logic should not be coupled to one SDK.

## Decision

Define an `LLMProvider` interface with structured generation, timeout, retry, model metadata, and safe error behavior. Select the provider and model through environment configuration. Include a deterministic fake provider for tests.

## Consequences

The prototype can switch providers without changing workflow contracts. Provider-specific capabilities must be handled inside adapters and verified through evaluation.

> [!NOTE]
> **Prototype Execution Scope:** Only the deterministic mock provider (`LLM_PROVIDER=mock`) is currently active for zero-cost prototype verification. Reserved live provider names (`openai`, `anthropic`, `gemini`) validate `LLM_API_KEY` environment configuration and raise `NotImplementedError` until live SDK adapters are installed.

## Rejected alternatives

Embedding provider SDK calls directly in workflow nodes would be faster initially but would increase coupling and make tests/network failures harder to control.
