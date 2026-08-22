# Test Strategy

## 1. Test layers

### Unit tests

Test state transitions, confidence-tier derivation, schema validation, query formulation, grounding labels, redaction, and metric calculations without network calls.

### Contract tests

Test API request/response models, repository contracts, provider interfaces, and fixture compatibility.

### Workflow tests

Run the graph with deterministic fake LLM, embedding, and retrieval providers. Cover success, retry, invalid output, conflict, weak retrieval, and missing data.

### Integration tests

Test SQLite persistence, FAISS retrieval, seed loading, and API-service wiring locally.

### UI smoke tests

Verify a reviewer can list a case, run analysis, inspect evidence/policy, submit each decision type, and view audit output.

### Evaluation tests

Run the versioned synthetic dataset and store metrics/failures as artifacts.

## 2. Test principles

- tests must be repeatable
- live provider tests are separate and opt-in
- difficult cases are first-class fixtures
- failed tests should identify case ID and workflow node
- no test may include real sensitive data
