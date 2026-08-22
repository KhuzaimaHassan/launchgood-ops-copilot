
# LaunchGood Ops Copilot
## Product Requirements Specification

**Status:** Approved product baseline v0.2  
**Scope:** MVP deployed prototype

---

# 1. Functional Requirements

## FR-001 — Case Listing

The system shall display available synthetic cases.

Each case shall have:

- unique ID
- title
- category
- priority
- risk status
- review status
- lifecycle status: `PENDING_ANALYSIS`, `AWAITING_HUMAN_DECISION`, `RESOLVED`, or `ESCALATED`

Internal execution states may additionally include `ANALYZING`, `NEEDS_REVIEW`, and `FAILED`.

Cases in `PENDING_ANALYSIS` must not display AI-derived metadata as if it were already assessed.

---

## FR-002 — Case Details

The system shall display source information associated with a case.

Source information may include:

- campaign description
- campaign updates
- supporter messages
- transaction/risk signals
- previous reviewer notes

---

## FR-003 — Case Analysis

The system shall allow a reviewer to request an AI assessment.

The request shall transition the internal execution state to `ANALYZING`; successful completion shall expose the user-facing state `AWAITING_HUMAN_DECISION`. Invalid, incomplete, or weakly grounded results shall use `NEEDS_REVIEW` internally where appropriate.

---

## FR-004 — Structured AI Output

The AI assessment shall contain at minimum:

- summary
- category
- risk level
- priority
- confidence
- evidence
- recommendation
- human-review requirement
- uncertainty/conflict indicators
- `human_review_required`
- `escalation_recommended`

---

## FR-005 — Policy Retrieval

The system shall retrieve relevant policy information from a synthetic internal knowledge base.

The retrieved information shall be displayed to the reviewer.

---

## FR-006 — Evidence Grounding

The AI recommendation shall reference available case evidence.

Unsupported claims should be identified or avoided.

---

## FR-007 — Human Review

The reviewer shall be able to:

- approve
- modify
- reject
- escalate

the AI recommendation.

For a modification, the system shall support these optional reviewer overrides: final decision, overridden risk, overridden priority, overridden recommendation/action, and reviewer notes. The original AI assessment shall remain immutable and distinguishable from all reviewer overrides.

---

## FR-008 — Decision Logging

The system shall record the final reviewer decision.

The original AI assessment shall remain available for comparison.

---

## FR-009 — Uncertainty

The system shall identify:

- low confidence
- insufficient evidence
- conflicting evidence
- missing policy information

when applicable.

---

## FR-010 — Failure Handling

The system shall gracefully handle:

- LLM/API failure
- malformed AI output
- missing case information
- failed policy retrieval
- unexpected workflow errors

---

## FR-011 — Evaluation

The system shall support execution of a predefined synthetic evaluation dataset.

The evaluation shall compare model output against expected outcomes.

Basic evaluation execution and result inspection are P0 MVP capabilities.

---

## FR-012 — Evaluation Metrics

The system should report appropriate metrics such as:

- classification performance
- risk assessment performance
- retrieval performance
- recommendation quality
- human override rate

Exact metrics may be refined during technical design.

---

# 2. User Interface Requirements

## UI-001 — Command Center Dashboard

The Dashboard shall use the approved visual system: Dark Navy `#0F172A`, Slate `#1E293B`, and LaunchGood Teal `#0D9488`.

The first viewport shall display four KPI cards:

- Needs Review
- High Risk
- Average Confidence
- Estimated Time Saved

The Dashboard shall provide queue filtering by lifecycle status, risk, priority, uncertainty, and policy grounding. The primary queue shall use rich case cards rather than a plain table. Each card shall show case title, risk, priority, status, confidence, evidence count, policy-grounding status, and a clear review action.

---

## UI-002 — Three-Zone Review Workspace

The Case Review page shall use three distinct zones:

1. **Executive Header:** case identity, lifecycle status, risk, priority, confidence, and recommended action.
2. **Tabbed Evidence & Context Workspace:** organized source timeline, evidence, retrieved policy, and uncertainty/conflict views.
3. **Persistent Human Decision Rail:** approve, modify, reject, and escalate controls with optional overrides and reviewer notes.

The interface shall clearly distinguish source information, AI-generated information, and human-authored decisions.

---

## UI-003 — Tabbed Evidence Visibility

Evidence supporting the AI assessment shall be visible without requiring application logs. The workspace shall organize source timeline, supporting evidence items, and uncertainty/conflict context into labeled tabs or equivalent progressive-disclosure sections.

---

## UI-004 — Tabbed Policy Grounding

Retrieved policy passages shall be visible in the Evidence & Context workspace alongside policy ID, chunk ID, grounding status, score, excerpt, and the recommendation they support.

---

## UI-005 — Confidence

Confidence shall be presented as an uncertainty signal, not as proof that the AI is correct.

Confidence shall be stored internally as `0.00–1.00` and displayed as a percentage plus a tier, such as `82% (High)`. Tier thresholds shall be configurable.

---

## UI-006 — Human Control

Consequential actions shall require explicit reviewer interaction.

## UI-007 — Visual Audit Timeline

Audit history shall be presented as a chronological visual timeline with formatted event badges for analysis started, analysis completed, failures, decisions, and state changes. Raw event payloads shall remain available through an expandable technical JSON drawer.

---

# 3. AI Requirements

## AI-001 — Structured Generation

LLM responses shall use a validated structured schema.

---

## AI-002 — Evidence-Based Reasoning

The model shall use retrieved case information rather than relying solely on general model knowledge.

---

## AI-003 — Policy Grounding

Policy-related recommendations shall be grounded in retrieved policy content.

---

## AI-004 — Uncertainty Detection

The workflow shall provide a mechanism for identifying insufficient or conflicting information.

The workflow shall set explicit uncertainty/conflict flags and shall be able to require human review or recommend escalation.

---

## AI-005 — Recommendation Boundaries

The AI shall recommend actions rather than execute consequential actions.

---

## AI-006 — Retry / Recovery

The workflow shall have defined behavior for failed or invalid model responses.

After bounded retry/repair attempts, the workflow shall return a typed failure or `NEEDS_REVIEW` result rather than fabricate an assessment.

---

# 4. Data Requirements

The prototype dataset shall contain synthetic data.

Each case should contain sufficient information to simulate a realistic operational review.

Potential entities:

- Campaign
- Case
- Support Message
- Campaign Update
- Risk Signal
- Policy
- AI Assessment
- Reviewer Decision

No real personally identifiable information should be required.

---

# 5. RAG Requirements

The knowledge base shall contain synthetic operational policies.

The retrieval system shall:

- index policy content
- retrieve relevant sections
- return source metadata
- handle no-result cases
- expose retrieved context to the AI workflow

Retrieval queries shall be generated from the normalized case category, key entities, detected issue terms, and missing-information questions. The workflow shall retain the query and retrieval metadata for audit/evaluation.

Similarity thresholds are configurable evaluation parameters; the product shall not assume a universal cutoff such as `0.65`. Weak or partial retrieval must be labeled as such and must not be presented as sufficient policy grounding.

The prototype should avoid unnecessarily complex vector infrastructure.

---

# 6. Audit Requirements

The system shall preserve:

- case ID
- assessment timestamp
- AI output
- evidence
- retrieved policies
- recommendation
- confidence
- reviewer action
- final decision

---

# 7. Non-Functional Requirements

## NFR-001 — Deployability

The application must run as a deployed web application.

---

## NFR-002 — Free-Tier Compatibility

The MVP should be deployable using free-tier or no-cost infrastructure wherever reasonably possible.

The architecture should minimize:

- persistent compute
- external API usage
- storage requirements
- unnecessary managed services

---

## NFR-003 — Performance

A normal case should produce an assessment within a reasonable interactive waiting period for a prototype.

Exact latency targets will be established after implementation testing.

---

## NFR-004 — Reliability

The system should fail gracefully rather than silently producing invalid results.

---

## NFR-005 — Maintainability

The implementation should use:

- typed interfaces
- modular components
- environment-based configuration
- clear separation of concerns
- automated tests for important behavior

---

## NFR-006 — Security

The prototype should:

- avoid real sensitive data
- keep credentials outside source code
- use environment variables for secrets
- avoid exposing API keys to the frontend
- clearly separate mock data from real-world assumptions

---

## NFR-007 — Reproducibility

A developer should be able to understand how the application works from the repository documentation and run the core workflow with the documented configuration.

---

# 8. Evaluation Requirements

The evaluation dataset should include both:

### Straightforward cases

Where evidence is clear and expected decisions are relatively obvious.

### Difficult cases

Including:

- ambiguous evidence
- conflicting information
- missing information
- misleading signals
- irrelevant policy retrieval
- cases requiring escalation

The system should be evaluated on its ability to **recognize uncertainty**, not merely classify obvious examples.

---

# 9. Prototype Acceptance Criteria

The MVP passes product acceptance when:

### Case workflow

- [ ] Reviewer can view cases.
- [ ] Unanalyzed cases are visibly marked `PENDING_ANALYSIS`.
- [ ] Reviewer can open a case.
- [ ] Reviewer can trigger analysis.
- [ ] AI generates structured output.
- [ ] Policy retrieval works.
- [ ] Evidence is displayed.
- [ ] Recommendation is displayed.
- [ ] Confidence is displayed.
- [ ] Confidence includes a numeric value, percentage, and configurable tier.
- [ ] Uncertainty and conflict flags are displayed when applicable.
- [ ] Human review is required.

### Human-in-loop

- [ ] Reviewer can approve.
- [ ] Reviewer can modify.
- [ ] Reviewer can reject.
- [ ] Reviewer can escalate.
- [ ] Human decision is recorded.
- [ ] AI and human decisions remain distinguishable.
- [ ] Reviewer modifications preserve optional decision, risk, priority, recommendation, and notes fields.

### Reliability

- [ ] Invalid AI output is handled.
- [ ] AI/API failure is handled.
- [ ] Missing information is handled.
- [ ] No-policy results are handled.
- [ ] Conflicting evidence is handled.

### Evaluation

- [ ] Synthetic evaluation dataset exists.
- [ ] Evaluation can be executed.
- [ ] Metrics are calculated.
- [ ] Failure cases can be inspected.

### Deployment

- [ ] Application is publicly accessible.
- [ ] Core workflow works on the deployed environment.
- [ ] No secrets are exposed.
- [ ] Prototype operates within intended free-tier constraints.

---

# 10. Explicit Out-of-Scope Requirements

The following must not enter MVP scope unless a later decision explicitly approves them:

- real LaunchGood integrations
- real payment processing
- real user accounts
- real campaign moderation
- autonomous campaign suspension
- autonomous refunds
- autonomous external messaging
- complex multi-agent systems
- Kubernetes
- microservice decomposition
- enterprise-scale infrastructure
- unnecessary paid services

---

# 11. Requirement Priority

### P0 — Must Have

- Case management
- AI assessment
- Structured output
- RAG
- Evidence
- Recommendation
- Human review
- Decision logging
- Basic evaluation
- Deployment

### P1 — Important

- Evaluation dashboard
- Audit trail visualization
- Reviewer override analytics

### P0 — Required Trust Capabilities

- Uncertainty detection
- Conflict detection

### P2 — Nice to Have

- Advanced analytics
- richer dashboards
- additional case types
- optimization experiments
- production-style integrations

P2 features must not delay the core deployed prototype.

---

# 12. Definition of Done

The product is ready for submission when a reviewer can open the public URL, select a realistic case, observe the AI independently perform meaningful analysis and policy retrieval, inspect evidence and uncertainty, make a human decision, and observe the resulting audit/evaluation information.

The complete workflow must be demonstrable in a short video without requiring access to source code.
