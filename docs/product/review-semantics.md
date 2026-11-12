# Review semantics

## Deterministic review rules

The mock provider considers normalized intake risk indicators **and detected source conflicts**. Either produces HIGH assessed risk and HIGH review priority. A conflict also recommends escalation; the documentation recommendation and source evidence remain intact. These values represent a demo review rule, not proof of fraud or a real campaign decision. The existing keyword-based conflict detector remains limited and is not a general contradiction engine.

Confidence is a rule-derived demo score, **not a calibrated probability**. The workflow never increases the provider score:

- A CONFLICTING_EVIDENCE, NO_APPLICABLE_POLICY or INSUFFICIENT_EVIDENCE flag caps it 0.01 below the configured MEDIUM threshold (0.54 with defaults).
- WEAK_POLICY_GROUNDING alone caps it 0.01 below the configured HIGH threshold (0.79 with defaults).
- Strong grounding without these flags preserves the provider score. Human review remains required for every assessment.

Thresholds have a zero floor; if the MEDIUM threshold itself is configured as zero, no nonnegative score can fall below it. The normal default thresholds are HIGH 0.80 and MEDIUM 0.55. This policy affects new runs only. Existing saved assessments and decisions are not rewritten or retroactively relabeled.

## Pending and final states

Unassessed cards and case headers show Assessed risk: PENDING, independently of intake priority. High-risk KPI/filter values use assessed risk only; PENDING has its own risk filter. Intake priority remains visible and continues to prioritize the existing needs-review count.

Case and assessment GET responses include persisted reviewer decisions. The rail displays the recorded action, risk/priority overrides, effective recommendation, notes, reviewer and timestamp. New decisions reference the saved assessment. The original AI values remain visible separately; no AI assessment is overwritten by a human override.

Resolved or escalated cases do not show a new submission form. If an older API does not supply decision details, the rail reports that they are unavailable and still prevents another submission. Existing backend lifecycle rejection remains in place. Offline examples cannot record decisions.

Benchmark runs use non-persisting assessment execution so they cannot become the case's latest assessment or replace the basis of a final decision. The benchmark starts with no result; users must run it. Offline examples remain labeled as static examples, not execution results.

## Deployment

Deploy the matching backend and frontend after review; no schema migration is required. The API response adds an optional/default-empty decisions list. An older backend will not provide the final-summary details. Older previously benchmarked cases may already have historical extra assessments; this repair does not delete them or reconstruct missing legacy decision/assessment links. No database reset is required or authorized.
