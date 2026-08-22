# Acceptance Matrix

| Product Capability | Verification Method | Status | Deployed Live Result |
| :--- | :--- | :--- | :--- |
| **Backend Health Check** | `GET /health` | **PASSED** | `200 OK` `{"status":"ok"}` on Render |
| **List Synthetic Cases** | `GET /cases` | **PASSED** | `200 OK` Returns 5 synthetic cases |
| **Case Details Retrieval** | `GET /cases/{id}` | **PASSED** | `200 OK` Retrieves intake details & status |
| **Structured AI Analysis** | `POST /cases/{id}/analysis` | **PASSED** | `200 OK` (or `409` if already analyzed) |
| **Assessment Retrieval** | `GET /cases/{id}/assessment` | **PASSED** | `200 OK` Returns assessment payload |
| **Human Decision Recording** | `POST /cases/{id}/decision` | **PASSED** | `200 OK` Persists `APPROVE`/`MODIFY`/`REJECT`/`ESCALATE` |
| **Immutable Audit Timeline** | `GET /cases/{id}/audit` | **PASSED** | `200 OK` Timeline events payload |
| **Evaluation Benchmark Run** | `POST /evaluation/runs` | **PASSED** | `200 OK` Executes 5-scenario benchmark |
| **Evaluation Lookup** | `GET /evaluation/runs/{id}` | **PASSED** | `200 OK` Retrieves completed run metrics |
| **Desktop Layout (`1440x900`)** | Playwright UI Audit | **PASSED** | 4 KPI tiles, filter chips, 2-column queue |
| **Tablet Layout (`1024x768`)** | Playwright UI Audit | **PASSED** | Responsive stacking, zero horizontal overflow |
| **Mobile Layout (`390x844`)** | Playwright UI Audit | **PASSED** | Touch-friendly cards, scrollable decision rail |
| **Policy Citation Safety** | RAG Policy Grounding | **PASSED** | Explicit `NO_APPLICABLE_POLICY` banner |
| **Conflicting Evidence** | Uncertainty Handler | **PASSED** | High-contrast `CONFLICTING_EVIDENCE` banner |
| **Prompt Injection Protection**| LangGraph Workflow | **PASSED** | Treats instruction text as evidence data |

The MVP is 100% accepted with all P0 capabilities verified on live deployed infrastructure.
