# Prompts and Schemas

**Status:** Proposed implementation baseline v0.1

## 1. Prompt construction

Prompts are composed from stable templates plus structured runtime context. Raw case content is delimited and labeled as source material.

Required context sections:

```text
SYSTEM RULES
NORMALIZED CASE SIGNALS
SOURCE FACTS WITH SOURCE IDS
RETRIEVED POLICY CHUNKS WITH CHUNK IDS
OUTPUT SCHEMA
```

The prompt must state that absent or weak policy context cannot be replaced with general model knowledge.

## 2. Normalized signals contract

```json
{
  "issue_category_candidates": ["DOCUMENTATION_CONCERN"],
  "entities": ["campaign", "organizer"],
  "key_facts": [
    {"fact": "string", "source_id": "update-1"}
  ],
  "risk_indicators": [
    {"indicator": "string", "severity": "MEDIUM", "source_id": "signal-1"}
  ],
  "missing_information_questions": ["string"]
}
```

## 3. Assessment contract

```json
{
  "summary": "string",
  "category": "DOCUMENTATION_CONCERN",
  "risk_level": "LOW|MEDIUM|HIGH",
  "priority": "LOW|MEDIUM|HIGH|URGENT",
  "confidence_score": 0.0,
  "evidence": [
    {
      "source_type": "CAMPAIGN|MESSAGE|UPDATE|RISK_SIGNAL",
      "source_id": "string",
      "fact": "string",
      "supports": "CATEGORY|RISK|PRIORITY|RECOMMENDATION"
    }
  ],
  "recommendation_action": "REQUEST_DOCUMENTATION|INVESTIGATE|NO_ACTION|ESCALATE",
  "recommendation_rationale": "string",
  "uncertainty_flags": [],
  "human_review_required": true,
  "escalation_recommended": false
}
```

The application validates enum values, source references, score range, non-empty rationale, and action boundaries. It derives `confidence_tier` from configuration after validation.

## 4. Reviewer decision contract

```json
{
  "decision_type": "APPROVE|MODIFY|REJECT|ESCALATE",
  "overridden_risk": "LOW|MEDIUM|HIGH|null",
  "overridden_priority": "LOW|MEDIUM|HIGH|URGENT|null",
  "overridden_recommendation": "string|null",
  "reviewer_notes": "string|null"
}
```

All override fields are optional. The original AI assessment is immutable.

## 5. Prompt test cases

Prompt tests must cover:

- clear evidence and strong policy match
- missing evidence
- conflicting source facts
- weak or absent policy retrieval
- prompt-injection-like text inside source content
- prohibited action request
- malformed/partial model output
