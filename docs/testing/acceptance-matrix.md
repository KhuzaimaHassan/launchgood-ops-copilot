# Acceptance evidence and limits

This matrix describes the current review branch, not proof of a production rollout. The deterministic provider and keyword-based conflict detector operate on five synthetic fixtures; they are not a live-LLM quality or prompt-injection evaluation.

| Capability | Automated evidence | Browser/deployment evidence |
| --- | --- | --- |
| Health, case listing/details, assessment and audit reads | API integration suite | Local branch queue/details, assessment and audit controls exercised on 10 November |
| Conflict case 1003 without intake risk signals | HIGH risk / HIGH priority, escalation, evidence retained, LOW demo confidence | Local case 1003 displayed HIGH/HIGH, 54% LOW, conflict/missing-policy flags and escalation on 10 November |
| Missing policy | Case 1004: NO_APPLICABLE_POLICY, LOW demo confidence without inventing high risk | Missing-policy flag displayed in the conflict case; standalone case 1004 behavior is API-tested |
| Confidence | Strong grounding preserves provider score; uncertainty caps never raise it; configured thresholds tested | Visible 54% LOW conflict and 79% MEDIUM weak-grounding scores/copy verified locally |
| Decisions | All four actions persist; GET case/assessment returns decision details; duplicate decisions rejected; original AI assessment retained | MODIFY submitted through phone UI; overrides, recommendation and long note survived reload; closed form absent |
| Benchmark isolation | Benchmark runs do not replace the saved case assessment or human decision | Button returned five 100% dimensions; three pending cases remained unassessed and recorded summaries remained intact |
| Five-fixture ground-truth agreement | Category, risk, priority, action and escalation asserted against unchanged expected labels | A passing fixture set does not establish general accuracy |
| Pending queue risk | Cards and case header now say Assessed risk: PENDING; assessed-risk filters distinguish pending | Pending-risk filter returned four unassessed cases; HIGH returned only the assessed conflict case before the second assessment |
| Responsive queue and decision rail | Production build/type check | Queue and long-note summary passed at 390×844, 1024×768 and 1440×900; no horizontal document/text overflow |
| Audit history | Stored SQLite events and retained decisions | Audit History label verified; raw JSON toggled and scrolled locally on phone; no cryptographic immutability claim |
| Provider failure/malformed output, physical-device behavior, real-LLM injection resistance | Not established by this repair | Not claimed verified |

The 6 November live benchmark had 80% risk/priority agreement because case 1003 was LOW rather than the expected HIGH. This branch fixes the rule, rather than changing the expected labels. The older blanket “100% accepted” claim has been removed. The 10 November browser audit used a matching isolated local API/SQLite fixture and production frontend build. No LaunchGood production deployment was made. Resized browser views are not physical-device tests.

See [review semantics](../product/review-semantics.md) for the confidence policy and historical-data limits.

Browser evidence: [conflict workspace](../assets/screenshots/08-verified-conflict-review.jpg), [mobile final decision](../assets/screenshots/09-verified-mobile-decision.jpg), [queue](../assets/screenshots/07-verified-queue.jpg). The benchmark starts empty before execution and after reload; offline examples remain separately labeled. Fault injection, offline/error UI and standalone no-policy browser execution were not tested in this pass.
