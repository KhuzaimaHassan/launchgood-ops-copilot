# Coding Standards and 4D Practice

## 1. Code organization

- keep domain models independent of UI and provider SDKs
- use small functions with explicit inputs/outputs
- isolate side effects in repositories and adapters
- keep prompts versioned and testable
- avoid global mutable state

## 2. Type and error discipline

- type public functions and service boundaries
- validate external/provider output immediately
- use typed domain errors with safe user-facing messages
- never catch and silently ignore exceptions
- never treat a failed AI call as a successful empty result

## 3. 4D development

- **Delegation:** delegate bounded implementation tasks with explicit acceptance criteria
- **Discernment:** review generated architecture, prompts, and code decisions
- **Diligence:** run tests, evaluation, and failure-case checks
- **Documentation:** update the relevant Markdown and ADR when a decision changes

## 4. Definition of implementation quality

Code is not ready for demo when it merely works on the happy path. It must preserve provenance, handle uncertainty, distinguish AI from human output, and remain runnable with the documented configuration.
