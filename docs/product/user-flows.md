
# LaunchGood Ops Copilot
## User Flows

**Status:** Approved product baseline v0.2

---

# 1. Primary User Flow

```text
Open Application
      ↓
Operations Command Center Dashboard
      ↓
Filter / Select Rich Case Card
      ↓
Three-Zone Case Review Workspace
      ↓
Executive Header + Evidence Tabs + Decision Rail
      ↓
Run AI Assessment
      ↓
Retrieve Relevant Policies
      ↓
Generate Evidence-Backed Assessment
      ↓
Display Recommendation
      ↓
Human Reviewer Reviews
      ↓
Approve / Modify / Reject / Escalate
      ↓
Decision Logged
      ↓
Visual Audit Timeline
      ↓
Return to Dashboard
```

## 1.1 Case Lifecycle

```text
PENDING_ANALYSIS → AWAITING_HUMAN_DECISION → RESOLVED
                                         └→ ESCALATED
```

The implementation may use internal execution states such as `ANALYZING`, `NEEDS_REVIEW`, and `FAILED`. The dashboard must distinguish cases awaiting their first analysis from cases with AI-derived metadata. A failed or weakly grounded run must not be shown as a completed assessment.

---

# 2. Dashboard Flow

The reviewer starts at the Operations Command Center Dashboard.

The dashboard displays four KPI cards:

- Needs Review
- High Risk
- Average Confidence
- Estimated Time Saved

The reviewer filters the queue by status, risk, priority, uncertainty, or policy grounding and selects a rich case card.

### Expected behavior

The system opens the three-zone Case Review workspace:

1. Executive Header
2. Tabbed Evidence & Context Workspace
3. Persistent Human Decision Rail

Cases not yet analyzed show `PENDING_ANALYSIS` and do not display fabricated AI risk, priority, confidence, or recommendation values.

---

# 3. Case Review Flow

## Step 1 — Case selection

Reviewer selects:

> Case #1042

The system loads:

- campaign information
- support messages
- updates
- transaction/risk signals
- previous notes

---

## Step 2 — AI processing

The reviewer triggers:

> Analyze Case

The system runs the AI workflow.

Conceptually:

```text
Case Data
   ↓
Normalize / Extract
   ↓
Retrieve Policies
   ↓
Assess Case
   ↓
Find Evidence
   ↓
Generate Recommendation
   ↓
Validate Structured Output
```

---

# 4. Successful Assessment Flow

The system returns:

### Summary

Short description of what happened.

### Classification

Example:

> Documentation Concern

### Risk

> Medium

### Priority

> High

### Confidence

> 0.82 — 82% (High)

The numeric value is the internal `0.00–1.00` confidence rendered for transparency; the tier is derived from configurable thresholds.

### Evidence

Relevant case facts.

### Policy

Relevant policy information.

### Recommendation

Suggested next action.

### Human Review

> Required

The assessment is displayed in the Executive Header and Evidence & Context tabs. The reviewer can now use the Persistent Human Decision Rail.

The tabs include:

- Source Timeline
- Evidence
- Retrieved Policy
- Uncertainty & Conflicts

---

# 5. Human Decision Flow

The reviewer sees:

```text
AI Recommendation
       ↓
Reviewer evaluates evidence
       ↓
 ┌─────┼─────┬──────────┐
 ↓     ↓     ↓          ↓
Approve Modify Reject  Escalate
```

---

## Approve

The recommendation is accepted.

The decision is logged.

---

## Modify

Reviewer changes the recommendation.

The original AI recommendation and final human decision are both preserved.

The reviewer may optionally override the final decision, risk, priority, and recommendation/action, and add reviewer notes. Each override is stored separately from the original AI assessment.

This is important for evaluating AI-human disagreement.

---

## Reject

Reviewer determines that the AI recommendation is incorrect.

The rejection is recorded.

---

## Escalate

Reviewer determines that the case requires additional investigation.

The case is marked for escalation.

---

# 6. Low-Confidence Flow

If the AI detects insufficient evidence:

```text
Case
 ↓
AI Analysis
 ↓
Insufficient evidence
 ↓
Low confidence
 ↓
Flag uncertainty
 ↓
Human investigation required
```

The system should not present a low-confidence assessment as a definitive conclusion.

---

# 7. Conflicting Evidence Flow

Example:

```text
Source A
"Campaign requires surgery."

Source B
"Surgery already completed."

        ↓

Conflict Detection

        ↓

Confidence Reduced

        ↓

Flag:
"Conflicting information detected"

        ↓

Human Review / Escalation
```

This is a key demonstration of uncertainty handling.

---

# 8. No Relevant Policy Flow

If policy retrieval returns no sufficiently relevant result:

```text
Case
 ↓
Policy Retrieval
 ↓
No relevant policy
 ↓
AI cannot confidently ground recommendation
 ↓
Flag:
"No applicable policy found"
 ↓
Human Review
```

The system should not fabricate policy.

Partial or weak retrieval is also surfaced as weak policy grounding. The similarity cutoff is configurable and evaluated empirically; it is not treated as a universal product constant.

---

# 9. AI Failure Flow

If the LLM/API fails:

```text
User requests analysis
        ↓
AI service failure
        ↓
Display recoverable error
        ↓
Allow retry
```

The application must not create a fake assessment when the AI service fails.

---

# 10. Invalid AI Output Flow

If the model produces output that does not conform to the required schema:

```text
LLM Output
    ↓
Schema Validation
    ↓
Invalid
    ↓
Retry / Repair
    ↓
Validation
    ↓
Valid → Continue
Invalid → Human review / failure state
```

---

# 11. Reviewer Override Flow

A reviewer can disagree with AI.

Example:

```text
AI:
Risk = HIGH

Reviewer:
Risk = MEDIUM

        ↓

Final decision:
MEDIUM

        ↓

Audit log stores:

AI assessment = HIGH
Human decision = MEDIUM
```

This information becomes valuable for evaluation.

---

# 12. Audit Flow

Every completed review should produce an audit record containing:

```text
Case ID
AI assessment
Evidence
Retrieved policies
Recommendation
Confidence
Reviewer action
Final decision
Timestamp
```

The UI presents this record as a visual chronological timeline with event badges such as `ANALYSIS_STARTED`, `ANALYSIS_COMPLETED`, `DECISION_RECORDED`, and `ANALYSIS_FAILED`. An expandable technical-details drawer exposes the raw JSON payload.

---

# 13. Evaluation Flow

A separate evaluation interface can run predefined test cases.

```text
Evaluation Dataset
       ↓
Run AI Workflow
       ↓
Compare Against Expected Results
       ↓
Calculate Metrics
       ↓
Display Results
```

The evaluation system should make it possible to identify failure cases rather than only report aggregate metrics.

Basic evaluation execution and result inspection are part of the MVP. Advanced analytics such as long-term trend dashboards remain outside the first release.

The benchmark contains five synthetic scenarios: `case-1001` through `case-1005`. Evaluation displays ground-truth agreement for category, risk, priority, recommendation, and escalation, plus per-case failure/root-cause details.

---

# 14. End-to-End Demo Flow

The primary video demonstration should follow:

```text
Operations Command Center Dashboard
   ↓
Show four KPI cards and filterable rich case queue
   ↓
Open `case-1001` — Missing Documentation
   ↓
Show Executive Header and run AI analysis
   ↓
Show Evidence and Retrieved Policy tabs
   ↓
Record a human `MODIFY` decision in the persistent rail
   ↓
Show visual Audit Timeline and raw JSON drawer
   ↓
Open `case-1003` — Conflicting Updates; show conflict flag and escalation
   ↓
Open `case-1004` — No Policy Found; show missing grounding
   ↓
Open `case-1005` — Prompt Injection Resistance; show source treated as data
   ↓
Open Evaluation Center and show five-scenario ground-truth metrics
```

This should be achievable within the five-minute submission video.
