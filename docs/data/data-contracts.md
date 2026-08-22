# Data Contracts and Provenance

**Status:** Proposed implementation baseline v0.1

## 1. Contract rules

- IDs are stable strings within a dataset version
- timestamps use UTC ISO-8601
- enum values are uppercase in API/storage contracts
- nullable fields are explicit
- numeric confidence is always within `0.0–1.0`
- source references must resolve before an assessment is persisted

## 2. Provenance requirements

Every assessment must be traceable to:

- case and source record IDs
- analysis run ID
- workflow version
- model/provider name
- policy query
- retrieved policy chunk IDs and scores
- reviewer decision, if present

## 3. Retention for prototype

Synthetic fixtures and audit data may remain in the repository/local database for demonstration. No real user content should be imported. A production system would require a documented retention and deletion policy; that is out of scope for this prototype.

## 4. Contract compatibility

Schema changes require:

1. update to the relevant documentation
2. migration or fixture update
3. contract tests
4. an evaluation rerun if AI or retrieval output changes
