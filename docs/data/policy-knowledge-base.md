# Synthetic Policy Knowledge Base

**Status:** Proposed implementation baseline v0.1

## 1. Policy corpus goals

The corpus should demonstrate retrieval and grounding, not imitate confidential LaunchGood policy. Every document is synthetic and labeled as such.

## 2. Initial policy families

- campaign documentation and verification
- medical or emergency fundraising evidence
- prohibited or restricted campaign content
- supporter complaint handling
- campaign update and consistency review
- escalation and additional investigation
- no-action/insufficient-concern guidance

## 3. Required document metadata

```json
{
  "policy_id": "POL-DOC-001",
  "title": "Synthetic Documentation Review Policy",
  "version": "1.0",
  "effective_date": "2026-01-01",
  "category": "DOCUMENTATION",
  "source_path": "data/policies/POL-DOC-001.md",
  "synthetic": true
}
```

## 4. Corpus test cases

The corpus must include near-matches and exceptions so evaluation can test irrelevant retrieval, weak grounding, and no-policy behavior. Each policy family should have at least one positive case and one confusing near-match.

## 5. Change process

Changing policy content, chunking, embedding model, or metadata increments the knowledge-base/index version and triggers a new retrieval evaluation run.
