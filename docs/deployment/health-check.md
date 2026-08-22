# Health Check Verification

## API check

Start the API with:

```text
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

Then request:

```text
GET /health
```

Expected response:

```json
{"status":"ok"}
```

## Smoke sequence

1. Open the public or local UI URL.
2. Confirm the dashboard loads synthetic cases.
3. Open a `PENDING_ANALYSIS` case.
4. Run analysis and confirm evidence/policy/uncertainty sections render.
5. Record a reviewer decision.
6. Confirm audit events are visible.
7. Run evaluation and confirm metrics are displayed.

## Failure interpretation

- health failure: deployment/process/configuration issue
- dashboard failure: UI dependency or storage issue
- analysis failure: provider, retrieval, or workflow issue
- missing policy: expected behavior only when grounding is genuinely unavailable
