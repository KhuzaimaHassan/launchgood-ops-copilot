# Required Failure Cases

| Case | Expected behavior |
|---|---|
| case ID does not exist | typed not-found response; no LLM call |
| required source data missing | incomplete-data flag; human review |
| conflicting campaign and update | conflict flag; reduced confidence; escalation may be recommended |
| no policy match | no fabricated policy; `NO_APPLICABLE_POLICY` |
| weak policy match | weak-grounding warning; recommendation remains reviewable |
| LLM timeout | bounded retry; recoverable failure |
| malformed JSON/schema | repair attempt; then `NEEDS_REVIEW`/failure |
| prohibited action generated | validation failure; no action execution |
| database write error | no false success; retry/error state |
| duplicate decision submission | idempotency or explicit conflict response |
| prompt-injection-like source text | treat source as data, not instruction |
| empty evaluation dataset | clear validation error; no misleading metrics |
