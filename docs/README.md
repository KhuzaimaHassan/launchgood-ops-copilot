# LaunchGood Ops Copilot Documentation

This directory is the source of truth for the deployed prototype.

## Current documentation layer

The product layer is complete enough to begin technical architecture:

- [`product/PRD.md`](product/PRD.md) — product vision, scope, workflow, roles, and definition of done
- [`product/requirements.md`](product/requirements.md) — functional, AI, data, RAG, UI, non-functional, and acceptance requirements
- [`product/user-flows.md`](product/user-flows.md) — primary, failure, human-review, audit, and evaluation flows
- [`product/decision-log.md`](product/decision-log.md) — approved product decisions and constraints

## Documentation layers

The approved product and architecture layers are now present. Later layers can be added as implementation begins:

```text
docs/
├── product/
├── architecture/
│   └── adr/
├── ai/
├── data/
├── development/
├── testing/
└── deployment/
```

Do not introduce technical choices that contradict the product documents. This is a deployed prototype using synthetic data and free-tier-conscious infrastructure; production-scale concerns remain explicitly out of scope.
