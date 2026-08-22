# ADR-002 — One Bounded LangGraph Workflow

**Status:** Accepted  
**Date:** 2026-08-18

## Context

The product needs explicit state, retries, validation, uncertainty handling, and an obvious human-review boundary. It does not need autonomous agents negotiating with each other.

## Decision

Use one LangGraph workflow with typed state and single-purpose nodes. Model calls are bounded and do not execute consequential tools.

## Consequences

The workflow is inspectable and testable. LangGraph adds a dependency, but its state and routing semantics support the required demonstration. Additional agents require a new ADR and evidence of meaningful benefit.

## Rejected alternatives

A plain sequential function pipeline may be sufficient for a later simplification, but autonomous multi-agent orchestration is rejected for MVP.
