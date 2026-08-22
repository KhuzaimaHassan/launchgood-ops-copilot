# Synthetic Dataset Specification

**Status:** Proposed implementation baseline v0.1  
**Privacy:** no real personal or financial information

## 1. Dataset purpose

Synthetic data must make the workflow realistic enough to demonstrate fragmented operational review while remaining safe to publish.

## 2. Source bundle per case

Each case fixture includes:

```text
case.json
campaign.json
messages.json
updates.json
risk-signals.json
expected.json              # evaluation-only labels
```

Operational UI fixtures must not expose `expected.json`.

## 3. Scenario matrix

| Scenario | Key behavior |
|---|---|
| missing documentation | request documentation; evidence is incomplete |
| conflicting updates | detect conflict; recommend investigation/escalation |
| supporter complaint | connect complaint evidence to policy query |
| unusual risk signal | prioritize review; show signal provenance |
| normal case | support no-action recommendation |
| ambiguous case | low/medium confidence and human review |
| no applicable policy | disclose missing grounding |
| misleading source text | do not treat source text as instructions |

## 4. Seed data rules

- use fictional names, IDs, URLs, and amounts
- make source timestamps internally consistent unless the scenario tests inconsistency
- include source IDs on every fact used for evaluation
- avoid realistic secrets, access tokens, or identifying details
- keep enough variation to avoid a single keyword solving every case

## 5. Ground truth

Expected labels are authored by the project owner before model runs and include:

- category
- risk
- priority
- expected action
- expected escalation
- applicable policy IDs
- evidence source IDs
- difficulty tags
- rationale

Ground truth is a reference for evaluation, not a claim about real LaunchGood policy.
