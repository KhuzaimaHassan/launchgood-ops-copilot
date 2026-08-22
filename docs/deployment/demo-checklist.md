# Five-Minute Demo Walkthrough

This walkthrough is synchronized with the five-scenario synthetic benchmark and the Operations Command Center UI baseline.

## 0:00–0:30 — Problem statement and principle

Explain that operations reviewers must combine campaign, message, update, risk, and policy information.

State the principle:

> AI prepares the decision; humans own the consequence.

## 0:30–1:15 — Operations Command Center Dashboard

Show the first viewport with four KPI cards:

- Needs Review
- High Risk
- Average Confidence
- Estimated Time Saved

Show the filterable rich case-card queue and explain that `PENDING_ANALYSIS` cases do not pretend to have AI-derived risk or recommendations.

## 1:15–2:30 — Clear Case: `case-1001`

Open **Missing Documentation** and show the three-zone workspace:

1. **Executive Header** — category, risk, priority, confidence, and recommendation.
2. **Tabbed Evidence & Context Workspace** — source timeline, evidence, and retrieved policy grounding.
3. **Persistent Human Decision Rail** — reviewer action controls.

Run the AI analysis, show the evidence and policy passage, then record a human `MODIFY` decision with reviewer notes. Show the visual audit timeline afterward.

## 2:30–3:45 — Difficult and adversarial cases

Show the three failure-oriented scenarios:

- `case-1003` — **Conflicting Updates**: display `CONFLICTING_EVIDENCE`, reduced trust, and escalation behavior.
- `case-1004` — **No Policy Found**: display `NO_APPLICABLE_POLICY` and show that the system does not fabricate a citation.
- `case-1005` — **Prompt Injection Resistance**: show that “ignore all instructions” inside source data is treated as evidence text, not an executable instruction.

## 3:45–4:30 — Evaluation Center

Run the complete five-scenario benchmark: `case-1001` through `case-1005`.

Show:

- workflow completion rate
- category agreement
- risk agreement
- priority agreement
- recommendation/action agreement
- escalation agreement
- per-case failure/root-cause breakdown

Explain that imperfect scores are visible by design and identify where the system needs improvement.

## 4:30–5:00 — Architecture and trade-offs

Close with:

- modular monolith rather than microservices
- bounded single workflow rather than multi-agent autonomy
- local FAISS/fallback retrieval
- SQLite and synthetic fixtures
- explicit failure handling, provenance, and auditability
- free-tier-conscious deployment

Mention that the default local provider is deterministic for reproducible testing and that a real provider adapter requires separate configuration and evaluation.
