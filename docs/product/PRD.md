
# LaunchGood Ops Copilot
## Product Requirements Document (PRD)

**Status:** Approved product baseline v0.2  
**Product Type:** Deployed AI-assisted operations prototype  
**Primary Purpose:** Demonstrate Applied AI engineering capability through a realistic human-in-the-loop workflow  
**Development Methodology:** 4D — Delegation, Discernment, Diligence, Documentation

---

## 1. Product Overview

LaunchGood Ops Copilot is a prototype AI-assisted operations system designed to reduce the manual effort involved in reviewing crowdfunding campaign-related cases.

The system aggregates case information from multiple sources, uses an AI workflow to summarize and assess the case, retrieves relevant internal policy information, identifies supporting evidence, and produces an evidence-backed recommendation for a human reviewer.

The system intentionally keeps consequential decisions under human control.

The prototype is not intended to represent LaunchGood's actual internal systems, policies, data, or production architecture. It uses realistic synthetic/mock data to demonstrate how such a workflow could operate.

---

## 2. Problem Statement

Small operations, support, finance, and trust & safety teams can spend substantial time manually reviewing fragmented information.

A typical case may require a reviewer to:

1. Read campaign information.
2. Review support or donor messages.
3. Inspect campaign updates.
4. Examine available risk or transaction signals.
5. Search internal policies.
6. Determine the nature and urgency of the issue.
7. Gather supporting evidence.
8. Decide on the appropriate next step.
9. Record the decision.

As case volume grows, this process creates repetitive cognitive work and increases the risk of inconsistent review.

The opportunity is not to remove humans from the process.

The opportunity is to allow AI to perform the repetitive analysis and preparation work while keeping consequential decisions with humans.

---

## 3. Product Vision

> Turn fragmented operational information into an evidence-backed case assessment that allows a human reviewer to make a faster, better-informed decision.

The system should behave as a **decision-support copilot**, not an autonomous decision-maker.

---

## 4. Target User

### Primary User

Operations / Trust & Safety reviewer.

The reviewer is responsible for investigating cases and making the final decision.

### Secondary Stakeholder

Team lead or operations manager.

The team lead needs visibility into:

- case volume
- priority
- risk distribution
- reviewer decisions
- AI performance
- human override patterns
- potential time savings

---

## 5. Core User Problem

The reviewer should not have to manually answer:

> "What happened, what evidence supports it, what policy applies, how serious is it, and what should I investigate next?"

The Copilot should prepare those answers.

The reviewer should then decide:

> "Do I agree with this assessment and recommendation?"

---

## 6. Product Goals

### Goal 1 — Reduce repetitive analysis

Automatically summarize and structure fragmented case information.

### Goal 2 — Surface useful insight

Identify risk, priority, issue category, relevant evidence, and recommended next action.

### Goal 3 — Make AI output trustworthy

Every important recommendation should be accompanied by evidence and relevant policy context.

### Goal 4 — Preserve human control

The AI must not independently execute consequential actions.

### Goal 5 — Demonstrate production-oriented AI engineering

The prototype should demonstrate:

- structured LLM outputs
- agentic workflow
- RAG
- evaluation
- failure handling
- auditability
- human-in-the-loop design

---

## 7. Non-Goals

The prototype will NOT:

- connect to real LaunchGood systems
- process real user/customer data
- automatically suspend campaigns
- automatically issue refunds
- automatically contact campaign organizers
- automatically modify financial records
- replace human reviewers
- implement a complete enterprise trust & safety platform
- implement complex multi-agent orchestration without a demonstrated need
- build production-scale infrastructure

---

## 8. Key Product Principle

> AI prepares the decision. Humans own the consequence.

The AI may analyze, classify, retrieve evidence, and recommend.

The human makes the final consequential decision.

---

## 9. Prototype Workflow

The core workflow is:

**Case ingestion → information extraction → policy retrieval → AI assessment → evidence generation → recommendation → human review → decision logging → evaluation**

The user-facing case lifecycle is explicit:

```text
PENDING_ANALYSIS → AWAITING_HUMAN_DECISION → RESOLVED
                                         └→ ESCALATED
```

The implementation may use granular internal execution states such as `ANALYZING`, `NEEDS_REVIEW`, and `FAILED`. `PENDING_ANALYSIS` is the initial dashboard state. Cases that have not been analyzed must not display invented risk, priority, confidence, or recommendation values.

---

## 10. AI Responsibilities

The AI is responsible for:

- summarizing the case
- extracting important information
- classifying the issue
- estimating risk
- assigning priority
- retrieving relevant policies
- identifying supporting evidence
- generating a recommended next action
- indicating confidence
- identifying ambiguity or conflicting evidence
- recommending escalation when appropriate

---

## 11. Human Responsibilities

The human reviewer is responsible for:

- validating AI output
- interpreting ambiguous cases
- accepting or modifying recommendations
- rejecting incorrect assessments
- escalating cases
- taking consequential actions outside the prototype
- providing reviewer feedback

---

## 12. Human/AI Boundary

### AI can:

- analyze
- summarize
- retrieve
- classify
- recommend
- flag uncertainty

### AI cannot:

- suspend a campaign
- approve a refund
- reject a campaign
- contact an external party
- modify financial/account records
- make irreversible decisions

All consequential actions require human approval.

---

## 13. Core Case Types

The prototype should support realistic operational scenarios such as:

1. Missing documentation
2. Conflicting campaign information
3. Donor/supporter complaint
4. Suspicious campaign activity
5. Unusual transaction/risk signal
6. Campaign information inconsistency
7. Normal/no-action-required case
8. Ambiguous case requiring escalation

These are synthetic scenarios created for demonstration.

---

## 14. Case Assessment

Every case should produce a structured assessment containing:

- case summary
- issue category
- priority
- risk level
- confidence
- evidence
- relevant policies
- recommendation
- human-review requirement
- ambiguity/conflict flags

Confidence is stored internally as a number from `0.00` to `1.00`. The interface displays both a percentage and a tier, for example `0.82 — 82% (High)`. Tier boundaries are configurable.

---

## 15. Evidence-Backed Recommendations

The system must avoid producing unsupported recommendations.

A recommendation should reference:

1. Case evidence
2. Relevant policy information
3. Reasoning summary

Example:

**Recommendation**

> Request supporting documentation and escalate for human review.

**Evidence**

- Campaign description contains an unsupported medical claim.
- Three donor complaints reference missing documentation.
- Recent campaign update provides no supporting evidence.

**Policy**

Relevant documentation policy retrieved from the internal knowledge base.

---

## 16. Uncertainty Handling

The system should explicitly recognize uncertainty.

Examples:

### High confidence

Evidence is consistent and sufficient.

### Medium confidence

Some information is incomplete or conflicting.

### Low confidence

The case is ambiguous or evidence is insufficient.

Low-confidence or conflicting cases should result in:

> Human investigation required.

The system must not compensate for uncertainty by producing a more confident-sounding recommendation.

Uncertainty is a first-class assessment result. The workflow must distinguish insufficient case evidence, conflicting case evidence, missing or weak policy retrieval, and invalid or incomplete model output. Any of these may lower confidence and may set `human_review_required` or `escalation_recommended` to true.

---

## 17. Product Dashboard

The dashboard should provide:

- total open cases
- high-risk cases
- pending reviews
- cases by priority
- cases by category
- recent reviewer activity

Each case also has a visible lifecycle status. Before analysis, a case is shown as `PENDING_ANALYSIS`; after a successful run it is shown as `AWAITING_HUMAN_DECISION`. Dashboard metrics must not treat pending cases as analyzed cases.

The dashboard is intended for demonstration and basic operational visibility.

---

## 18. Case Review Interface

A reviewer should be able to open a case and see:

### Case Information

Original case data and source information.

### AI Summary

Concise explanation of what happened.

### Assessment

- category
- risk
- priority
- confidence

### Evidence

Relevant source information supporting the assessment.

### Policy

Retrieved policy passages.

### Recommendation

Suggested next action.

### Human Decision

- Approve
- Modify
- Reject
- Escalate

For `Modify`, the reviewer can record an optional overridden decision, risk, priority, and recommendation/action, together with reviewer notes. Unchanged fields remain linked to the original AI assessment. The system preserves both the AI values and the final human values.

---

## 19. Auditability

The system should record:

- case ID
- AI assessment
- retrieved evidence
- recommendation
- confidence
- reviewer decision
- reviewer modification
- timestamp

This allows the prototype to demonstrate how AI decisions could be reviewed retrospectively.

---

## 20. Evaluation

The system will include a predefined evaluation dataset containing synthetic cases with expected outcomes.

Evaluation should measure:

- classification performance
- risk assessment performance
- policy retrieval quality
- recommendation quality
- evidence grounding
- human override rate
- escalation behavior

Basic evaluation execution is part of the MVP. Advanced trend analysis and reviewer analytics are not required for the first release.

The purpose is not to manufacture an impressive accuracy number.

The purpose is to demonstrate that the system has a measurable quality bar and that known failure modes are intentionally tested.

---

## 21. Success Metrics

The prototype will be considered successful if it demonstrates:

### Product

- reviewer can process a case end-to-end
- AI provides useful analysis
- recommendations are evidence-backed
- human approval is required for consequential decisions

### AI

- structured outputs are valid
- relevant policies are retrieved
- recommendations correspond to available evidence
- uncertainty is surfaced
- difficult cases can be escalated

### Engineering

- application is deployed
- workflow is reproducible
- failures are handled gracefully
- important actions are auditable
- evaluation can be repeated

---

## 22. Prototype Constraints

The project is intentionally designed for free-tier deployment.

Therefore:

- use synthetic data
- minimize external API calls
- use small/efficient models where practical
- prefer local embeddings
- use lightweight storage
- avoid unnecessary infrastructure
- avoid always-on expensive services
- keep the architecture simple enough for a single developer
- avoid premature scalability work

The prototype should optimize for:

**demonstration quality > infrastructure complexity**

---

## 23. Prototype vs Production

### Prototype

- synthetic data
- lightweight deployment
- limited users
- limited dataset
- simplified integrations
- free/low-cost infrastructure

### Production

A real implementation would require:

- authenticated internal access
- real LaunchGood data integrations
- stronger privacy controls
- role-based access
- secure secrets management
- production database
- robust observability
- model monitoring
- comprehensive evaluation
- human-review policies
- access auditing
- stronger reliability guarantees

The prototype should clearly communicate this distinction.

---

## 24. Product Philosophy

The system should not attempt to maximize AI autonomy.

Instead, it should maximize:

> **Useful automation while preserving appropriate human judgment.**

A smaller, well-controlled AI workflow is preferable to an unnecessarily autonomous system.

---

## 25. 4D Development Principle

All AI-assisted development will follow:

### Delegation

Use AI to accelerate implementation of bounded tasks.

### Discernment

Human reviews architectural and product decisions rather than blindly accepting AI output.

### Diligence

Generated code and AI behavior are verified through tests, evaluation, review, and failure analysis.

### Documentation

Important technical and product decisions are recorded so that the reasoning behind the system remains understandable.

The developer retains ownership of the final architecture, code, decisions, and deployed system.

---

## 26. Definition of Done — Product MVP

The MVP is complete when:

- a user can open the deployed application
- synthetic cases are available
- a reviewer can select a case
- the system processes the case through the AI workflow
- AI produces structured assessment
- relevant policy information is retrieved
- evidence is shown
- recommendation is generated
- uncertainty is surfaced
- human decision is required
- reviewer decision is recorded
- evaluation results are available
- uncertainty and conflict detection work on representative difficult cases
- basic evaluation can be run against the synthetic dataset
- the system handles representative failure cases
- the application is publicly deployable
- the complete workflow can be demonstrated within five minutes

---

## 27. Final Product Statement

> LaunchGood Ops Copilot is a human-in-the-loop AI operations prototype that transforms fragmented campaign and support information into evidence-backed case assessments, enabling reviewers to investigate cases faster while retaining human control over consequential decisions.
