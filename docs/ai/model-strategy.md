# Model Strategy

**Status:** Proposed implementation baseline v0.1

## 1. Provider policy

The application uses an `LLMProvider` interface. A provider is selected through environment configuration and never imported directly by domain code.

Required adapter behavior:

- structured generation against a supplied schema
- timeout and retry support
- model/provider metadata returned for auditability
- safe error categories
- deterministic fake provider for tests

## 2. Model responsibilities

The model may:

- normalize fragmented case information
- summarize source facts
- classify issue category
- propose risk and priority
- identify evidence and conflicts
- formulate a policy query
- recommend a bounded next action
- indicate uncertainty

The model may not:

- call external consequential systems
- claim a policy was retrieved when it was not
- invent evidence, policy, or source references
- make the final reviewer decision

## 3. Default call budget

The normal analysis path targets:

1. one normalization/extraction call, if needed
2. one structured assessment call
3. zero or one bounded repair call

The implementation may combine normalization and assessment when quality remains acceptable. Evaluation must record the actual call path.

## 4. Selection criteria

Select a model based on:

- structured-output reliability
- latency within a short interactive review
- cost/free-tier availability
- ability to follow evidence and abstention instructions
- provider stability

No model is permanently embedded in product logic. Model changes require an evaluation comparison and a configuration/version update.

## 5. Safety defaults

- temperature and token limits are configuration
- prompts explicitly say retrieved policy is untrusted context, not an action command
- output validation is mandatory
- uncertain cases require human review
- provider failures do not produce synthetic success
