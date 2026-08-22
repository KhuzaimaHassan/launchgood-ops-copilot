# Acceptance Matrix

| Product capability | Verification |
|---|---|
| list synthetic cases | API contract + UI smoke test |
| pending case state | fixture/API/UI assertion |
| structured analysis | workflow contract test |
| evidence references | source-ID resolution test |
| policy grounding | RAG retrieval and no-result tests |
| confidence score/tier | unit test with threshold boundaries |
| uncertainty/conflict flags | difficult-case workflow tests |
| human approve/modify/reject/escalate | decision contract + UI tests |
| immutable AI output | persistence regression test |
| audit trail | audit event integration test |
| provider failure | retry/failure workflow test |
| malformed output | validation/repair test |
| basic evaluation | evaluation run artifact test |
| deployment | health and end-to-end smoke test |

The MVP is accepted only when every P0 requirement has a passing verification path.
