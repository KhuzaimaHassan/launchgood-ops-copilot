# Prototype Operations

## 1. Health and logs

The application exposes a health endpoint and emits structured logs containing request ID, case ID, analysis run ID, status, duration, and safe error category.

Do not log provider keys, raw secrets, or unnecessary source content.

## 2. Recovery

- provider failure: retry from the analysis request
- failed run: preserve failure/audit event and allow a new run
- corrupted index: rebuild from versioned synthetic policies
- database issue: restore from the documented local/hosted persistence mechanism
- bad deployment: roll back to the previous known configuration

## 3. Cost controls

- use local embeddings and FAISS
- cache the policy index
- bound retries and token counts
- keep evaluation runs manual/on-demand
- avoid always-on auxiliary services
- monitor provider usage through available provider logs

## 4. Human support boundary

There is no automated outbound message, refund, suspension, or financial action. Any real-world action remains outside the prototype and requires a human-controlled process.
