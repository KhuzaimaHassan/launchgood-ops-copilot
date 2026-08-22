# Deployment Configuration

## 1. Required configuration

```text
APP_ENV
DATABASE_URL
LLM_PROVIDER
LLM_MODEL
LLM_API_KEY
EMBEDDING_PROVIDER
EMBEDDING_MODEL
RAG_INDEX_PATH
RAG_INDEX_VERSION
CONFIDENCE_HIGH_THRESHOLD
CONFIDENCE_MEDIUM_THRESHOLD
MAX_ANALYSIS_RETRIES
REQUEST_TIMEOUT_SECONDS
```

## 2. Secret handling

- set secrets only through the deployment platform or local untracked environment file
- never place secrets in Markdown, fixtures, screenshots, or client-side configuration
- rotate a credential if it is exposed
- use a mock provider for tests and screenshots when possible

## 3. Configuration validation

Startup should fail clearly when required production settings are missing. Non-secret defaults may be used for local development, but production must not silently fall back to a mock provider unless explicitly configured.
