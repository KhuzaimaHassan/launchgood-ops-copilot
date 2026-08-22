# Product Decision Log

**Status:** Approved product baseline v0.2

## D-001 — Prototype boundary

The system is a deployed demonstration prototype, not a replacement for LaunchGood's production platform. It uses synthetic data and must remain compatible with free-tier or no-cost infrastructure wherever reasonably possible.

## D-002 — Human ownership of consequences

AI may summarize, classify, retrieve, identify evidence, flag uncertainty, and recommend. It may not execute consequential actions. A human reviewer owns the final decision.

## D-003 — Trust capabilities are MVP requirements

Uncertainty detection, conflict detection, and basic evaluation execution are P0 because the demonstration would be misleading without them. Advanced analytics remain P1/P2.

## D-004 — Explicit lifecycle states

Cases expose the user-facing states `PENDING_ANALYSIS`, `AWAITING_HUMAN_DECISION`, `RESOLVED`, and `ESCALATED`. The implementation may use `ANALYZING`, `NEEDS_REVIEW`, and `FAILED` internally. Pending cases cannot display AI-derived metadata as completed analysis.

## D-005 — Confidence representation

Confidence is stored internally as `0.00–1.00` and rendered in the UI as a percentage plus a tier. Tier thresholds are configurable and must be treated as uncertainty signals, not correctness probabilities.

## D-006 — Immutable AI assessment plus explicit overrides

The original AI assessment is preserved. A reviewer modification records optional final decision, risk, priority, recommendation/action, and notes as separate human-authored fields.

## D-007 — RAG query and weak retrieval behavior

Retrieval queries are generated from normalized case information, issue terms, entities, and missing-information questions. Query and retrieval metadata are retained for evaluation. Similarity thresholds are configurable; weak or partial retrieval is surfaced and cannot silently become policy grounding.

## D-008 — Evaluation scope

The MVP must run a predefined synthetic evaluation dataset, calculate basic metrics, and expose failure cases. Long-term analytics, reviewer trend dashboards, and production monitoring are later concerns.

## D-009 — Operations Command Center UI & Decision Ergonomics

The reviewer interface shall use an intentional visual system:

- Dark Navy: `#0F172A`
- Slate: `#1E293B`
- LaunchGood Teal: `#0D9488`

The Dashboard shall use KPI cards and rich case cards instead of a plain case table as its primary scanning surface. The Case Review workspace shall use three persistent zones:

1. **Executive Header** — case identity, lifecycle, risk, priority, confidence, and recommended action.
2. **Tabbed Evidence & Context Workspace** — source timeline, evidence, retrieved policy, and uncertainty/conflict context.
3. **Persistent Human Decision Rail** — approve, modify, reject, or escalate controls with optional overrides and reviewer notes.

Audit History shall be presented as a visual chronological timeline with formatted event badges. Raw event JSON remains available through an expandable technical-details drawer.
