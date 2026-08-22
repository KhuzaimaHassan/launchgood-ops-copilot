# LaunchGood Ops Copilot — Data Model

**Status:** Proposed architecture baseline v0.1  
**Storage default:** SQLite plus local FAISS/JSON artifacts  
**Data policy:** synthetic data only

## 1. Modeling rules

- source facts, AI-derived fields, and human-authored fields are separate
- AI assessments are append-only versions for auditability
- reviewer decisions never mutate the original AI output
- all records have stable IDs and timestamps
- enum values are explicit and validated
- raw source content is retained only as synthetic fixture data

## 2. Entity relationship overview

```text
Campaign 1 ──────── * Case
Case 1 ──────────── * SupportMessage
Case 1 ──────────── * CampaignUpdate
Case 1 ──────────── * RiskSignal
Case 1 ──────────── * AssessmentRun
AssessmentRun 1 ─── 1 AIAssessment
AssessmentRun 1 ─── * EvidenceItem
AssessmentRun 1 ─── * PolicyReference
Case 1 ──────────── * ReviewerDecision
Case 1 ──────────── * AuditEvent
Policy 1 ────────── * PolicyChunk
```

## 3. Core entities

### Campaign

| Field | Type | Notes |
|---|---|---|
| `campaign_id` | string | stable synthetic identifier |
| `title` | string | campaign title |
| `description` | text | source content |
| `organizer_summary` | text/null | synthetic organizer context |
| `created_at` | datetime | source timestamp |
| `updated_at` | datetime | source timestamp |

### Case

| Field | Type | Notes |
|---|---|---|
| `case_id` | string | primary identifier |
| `campaign_id` | string | related campaign |
| `title` | string | review case title |
| `intake_category` | enum/string | non-AI initial category |
| `initial_priority` | enum | intake priority, not AI priority |
| `status` | enum | lifecycle state |
| `source_refs` | JSON/list | source record IDs |
| `created_at` | datetime | intake timestamp |
| `updated_at` | datetime | latest state change |

User-facing status values are `PENDING_ANALYSIS`, `AWAITING_HUMAN_DECISION`, `RESOLVED`, and `ESCALATED`. Internal execution records may additionally use `ANALYZING`, `NEEDS_REVIEW`, and `FAILED`.

### SupportMessage

| Field | Type | Notes |
|---|---|---|
| `message_id` | string | stable identifier |
| `case_id` | string | parent case |
| `channel` | enum/string | synthetic support/donor channel |
| `author_role` | enum/string | supporter, organizer, staff |
| `content` | text | synthetic content |
| `created_at` | datetime | source timestamp |

### CampaignUpdate

| Field | Type | Notes |
|---|---|---|
| `update_id` | string | stable identifier |
| `campaign_id` | string | parent campaign |
| `content` | text | synthetic update |
| `created_at` | datetime | source timestamp |

### RiskSignal

| Field | Type | Notes |
|---|---|---|
| `signal_id` | string | stable identifier |
| `case_id` | string | parent case |
| `signal_type` | enum/string | transaction, complaint, consistency, documentation |
| `value` | JSON | synthetic structured signal |
| `severity` | enum | low, medium, high |
| `source_ref` | string/null | provenance |

## 4. AI and evidence entities

### AssessmentRun

| Field | Type | Notes |
|---|---|---|
| `analysis_run_id` | string | unique execution |
| `case_id` | string | parent case |
| `workflow_version` | string | reproducibility marker |
| `model_provider` | string | provider name, not secret |
| `model_name` | string | model identifier |
| `status` | enum | running, succeeded, failed, needs_review |
| `started_at` | datetime | execution time |
| `completed_at` | datetime/null | completion time |
| `error_code` | string/null | typed failure category |

### AIAssessment

| Field | Type | Notes |
|---|---|---|
| `assessment_id` | string | immutable assessment ID |
| `analysis_run_id` | string | parent run |
| `summary` | text | concise case summary |
| `category` | enum/string | AI-derived issue category |
| `risk_level` | enum | low, medium, high |
| `priority` | enum | low, medium, high, urgent |
| `confidence_score` | float | canonical `0.0–1.0` value |
| `confidence_tier` | enum | derived high, medium, low |
| `human_review_required` | boolean | explicit boundary |
| `escalation_recommended` | boolean | explicit uncertainty response |
| `uncertainty_flags` | JSON/list | missing, conflict, weak_policy, etc. |
| `recommendation_action` | enum/string | bounded recommended action |
| `recommendation_rationale` | text | evidence-backed explanation |
| `created_at` | datetime | immutable creation time |

The confidence tier is derived by application code from configurable thresholds. It is not independently trusted from an LLM categorical value.

### EvidenceItem

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | string | stable identifier |
| `assessment_id` | string | parent assessment |
| `source_type` | enum | campaign, message, update, risk_signal |
| `source_id` | string | source record |
| `quote_or_fact` | text | concise supporting fact |
| `supports` | enum | risk, category, priority, recommendation |
| `confidence` | float/null | optional evidence confidence |

### PolicyReference

| Field | Type | Notes |
|---|---|---|
| `policy_reference_id` | string | stable identifier |
| `assessment_id` | string | parent assessment |
| `policy_id` | string | source policy |
| `chunk_id` | string | retrieved chunk |
| `retrieval_score` | float | provider/index score |
| `grounding_status` | enum | strong, weak, none |
| `excerpt` | text | displayed policy passage |

## 5. Human and audit entities

### ReviewerDecision

| Field | Type | Notes |
|---|---|---|
| `decision_id` | string | stable identifier |
| `case_id` | string | parent case |
| `assessment_id` | string/null | AI assessment reviewed |
| `decision_type` | enum | approve, modify, reject, escalate |
| `overridden_risk` | enum/null | optional human override |
| `overridden_priority` | enum/null | optional human override |
| `overridden_recommendation` | string/null | optional human override |
| `reviewer_notes` | text/null | reviewer reasoning |
| `reviewer_id` | string | prototype reviewer identifier |
| `created_at` | datetime | decision time |

### AuditEvent

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | stable identifier |
| `case_id` | string | related case |
| `analysis_run_id` | string/null | related execution |
| `event_type` | enum/string | state_changed, analysis_completed, decision_recorded, failure |
| `actor_type` | enum | system, AI, reviewer |
| `payload` | JSON | redacted event details |
| `created_at` | datetime | event time |

## 6. Evaluation entities

Evaluation fixtures should be versioned JSON/CSV rather than mixed into operational case rows.

```text
EvaluationExample
├── example_id
├── case_fixture
├── expected_category
├── expected_risk
├── expected_priority
├── expected_action
├── expected_escalation
├── expected_policy_ids
└── difficulty / tags
```

An evaluation run stores the dataset version, workflow/model configuration, aggregate metrics, and per-example failures.
