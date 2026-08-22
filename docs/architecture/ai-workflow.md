# LaunchGood Ops Copilot — AI Workflow Design

**Status:** Proposed architecture baseline v0.1  
**Orchestration:** one bounded LangGraph workflow  
**Primary rule:** AI prepares the decision; humans own the consequence

## 1. Workflow graph

```text
START → load_case → normalize_case → formulate_policy_query
      → retrieve_policy → grade_policy_grounding
      → extract_evidence_and_conflicts → generate_assessment
      → validate_assessment
          ├─ invalid + retries available → repair_assessment → validate
          ├─ invalid + retries exhausted → NEEDS_REVIEW / FAILED
          └─ valid → derive_confidence_and_flags
                         → persist_assessment → END
```

The graph is a stateful workflow, not a collection of independent autonomous agents. Each node has one responsibility and typed inputs/outputs.

## 2. Workflow state

```python
WorkflowState = {
    "case_id": str,
    "analysis_run_id": str,
    "case": CaseInput,
    "normalized_signals": NormalizedSignals | None,
    "policy_query": PolicyQuery | None,
    "policy_matches": list[PolicyMatch],
    "policy_grounding": GroundingStatus,
    "evidence_items": list[EvidenceItemDraft],
    "conflict_flags": list[ConflictFlag],
    "assessment_draft": AssessmentDraft | None,
    "assessment": AIAssessment | None,
    "retry_count": int,
    "errors": list[WorkflowError],
}
```

The implementation should use Pydantic models for these structures rather than leaving them as untyped dictionaries.

## 3. Node responsibilities

### `load_case`

Loads the case and related source records. Fails early when the case does not exist.

### `normalize_case`

Converts heterogeneous source records into structured signals: issue/category clues, named entities, key facts, risk indicators, missing-information questions, and source references. Provenance is preserved for later evidence linking.

### `formulate_policy_query`

Builds a concise retrieval query from normalized signals. It must not blindly concatenate the entire raw case. Query fields include issue category, relevant entities, concern terms, and missing-information questions.

### `retrieve_policy`

Calls the RAG adapter and stores matches, scores, source metadata, and the exact query used.

### `grade_policy_grounding`

Labels retrieval as `STRONG`, `WEAK`, or `NONE` using configurable evaluation parameters and policy metadata. The label is visible in assessment provenance.

### `extract_evidence_and_conflicts`

Identifies source facts that support or contradict a potential assessment. Conflicting facts become explicit flags rather than being averaged away.

### `generate_assessment`

Produces a strict structured draft containing summary, category, risk, priority, evidence references, recommendation, uncertainty flags, and human-review requirements. The prompt instructs the model to abstain from unsupported policy claims.

### `validate_assessment`

Validates enums, required fields, evidence references, score bounds, and action boundaries. It rejects recommendations that imply autonomous consequential actions.

### `repair_assessment`

Performs at most a configured number of repair attempts. It receives validation errors, not an instruction to freely regenerate the entire case. Exhaustion returns a typed failure/review-required result.

### `derive_confidence_and_flags`

Normalizes the canonical numeric score to `0.0–1.0`, derives the UI tier from configuration, and adds deterministic flags for missing evidence, conflicts, and weak policy grounding. The LLM cannot provide contradictory authoritative score/tier values.

### `persist_assessment`

Stores the immutable assessment, provenance, audit event, and resulting case status in one application-level operation.

## 4. Structured assessment contract

```json
{
  "summary": "string",
  "category": "DOCUMENTATION_CONCERN",
  "risk_level": "MEDIUM",
  "priority": "HIGH",
  "confidence_score": 0.82,
  "evidence": [
    {
      "source_type": "SUPPORT_MESSAGE",
      "source_id": "msg-1042-01",
      "fact": "string",
      "supports": "RECOMMENDATION"
    }
  ],
  "recommendation_action": "REQUEST_DOCUMENTATION",
  "recommendation_rationale": "string",
  "uncertainty_flags": ["WEAK_POLICY_GROUNDING"],
  "human_review_required": true,
  "escalation_recommended": false
}
```

The application derives `confidence_tier` after validation. A recommendation is a bounded enum/action, not an instruction to call an external system.

## 5. Uncertainty rules

| Condition | Deterministic response |
|---|---|
| missing key case facts | add `INSUFFICIENT_EVIDENCE`; require review |
| contradictory source facts | add `CONFLICTING_EVIDENCE`; lower confidence; consider escalation |
| weak policy grounding | add `WEAK_POLICY_GROUNDING`; require review |
| no applicable policy | add `NO_APPLICABLE_POLICY`; never invent policy |
| malformed model output | retry/repair, then typed failure |
| prohibited autonomous action | validation failure |

The workflow may generate a useful recommendation under uncertainty, but the UI must make uncertainty prominent and preserve human review.

## 6. Provider abstraction

The workflow depends on interfaces such as:

```text
LLMProvider.generate_structured(prompt, schema) -> model output
EmbeddingProvider.embed(texts) -> vectors
PolicyRetriever.search(query, filters, top_k) -> policy matches
```

Provider implementations may target a hosted model or a local/mock provider for tests. Unit tests must not require network access.

## 7. Cost and latency controls

- one primary generation call plus bounded repair calls
- one retrieval call against a local index
- cached normalized case/query data where safe
- small context windows containing only relevant source excerpts
- configurable maximum tokens and timeout
- deterministic fixture provider for evaluation and CI
