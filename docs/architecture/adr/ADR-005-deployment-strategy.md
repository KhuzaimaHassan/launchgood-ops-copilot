# ADR-005 — Free-Tier-Conscious Deployment

**Status:** Accepted  
**Date:** 2026-08-18

## Context

The deliverable is a publicly accessible prototype. It must be demonstrable without introducing paid infrastructure or production-scale operations.

## Decision

Deploy the smallest supported web-service shape with synthetic fixtures, SQLite or the selected free database option, a local FAISS artifact, environment-based secrets, a health endpoint, and manual/on-demand evaluation.

## Consequences

The system is affordable and simple to explain. It has limited durability, concurrency, authentication, and observability. Those limitations are documented and must not be hidden.

## Rejected alternatives

Kubernetes, Redis, Kafka, hosted vector infrastructure, paid observability, and multi-region deployment are out of scope.
