# Acceptance evidence and limits

This matrix describes the current review branch, not proof of a production rollout. The deterministic provider and keyword-based conflict detector operate on five synthetic fixtures; they are not a live-LLM quality or prompt-injection evaluation.

| Capability | Automated evidence | Browser/deployment evidence |
| --- | --- | --- |
| Health, case listing/details, assessment and audit reads | API integration suite | Previously exercised live on 6 November; new branch still needs browser verification |
| Conflict case 1003 without intake risk signals | HIGH risk / HIGH priority, escalation, evidence retained, LOW demo confidence | New branch browser check pending |
| Missing policy | NO_APPLICABLE_POLICY, LOW demo confidence without inventing high risk | New branch browser check pending |
| Confidence | Strong grounding preserves provider score; uncertainty caps never raise it; configured thresholds tested | Visible demo-score copy and flag explanations require visual review |
| Decisions | All four actions persist; GET case/assessment returns decision details; duplicate decisions rejected; original AI assessment retained | Summary, overrides and notes after browser reload still need verification |
| Benchmark isolation | Benchmark runs do not replace the saved case assessment or human decision | Actual benchmark button still needs branch UI check |
| Five-fixture ground-truth agreement | Category, risk, priority, action and escalation asserted against unchanged expected labels | A passing fixture set does not establish general accuracy |
| Pending queue risk | Cards and case header now say Assessed risk: PENDING; assessed-risk filters distinguish pending | Browser check pending |
| Responsive queue and decision rail | Production build/type check | Recheck 390×844, 1024×768 and 1440×900 for this branch; older screenshots do not verify the new summary |
| Audit history | Stored SQLite events and retained decisions | No cryptographic immutability claim |
| Provider failure/malformed output, physical-device behavior, real-LLM injection resistance | Not established by this repair | Not claimed verified |

The 6 November live benchmark had 80% risk/priority agreement because case 1003 was LOW rather than the expected HIGH. This branch fixes the rule, rather than changing the expected labels. The older blanket “100% accepted” claim has been removed. Deployment and a fresh browser audit must be reported separately from unit/API tests.

See [review semantics](../product/review-semantics.md) for the confidence policy and historical-data limits.
