# LaunchGood Ops Copilot — RAG Design

**Status:** Proposed architecture baseline v0.1  
**Knowledge base:** synthetic operational policies  
**Default index:** FAISS with local metadata

## 1. RAG objective

Retrieve relevant policy passages that help the workflow ground a recommendation. Retrieval is a supporting capability, not permission for the model to invent policy or make a consequential decision.

## 2. Ingestion pipeline

```text
Policy source files
       ↓
Parse and normalize
       ↓
Attach policy metadata
       ↓
Chunk by heading/semantic section
       ↓
Generate embeddings
       ↓
Build FAISS index
       ↓
Persist index + metadata manifest
```

The build should be deterministic for the same policy corpus, embedding model, and configuration.

## 3. Policy document format

Each synthetic policy should include:

```text
policy_id
title
version
effective_date
category
source_path
content
```

Each chunk stores:

```text
chunk_id
policy_id
title
section_heading
text
ordinal
embedding_model
```

Policy version and source metadata must be returned with every match shown to a reviewer.

## 4. Chunking strategy

Prefer heading-aware chunks of approximately 300–600 words with modest overlap where a section would otherwise lose context. Do not split a rule from its exception when the source structure makes them inseparable.

Chunking configuration is versioned because changing it changes retrieval evaluation results.

## 5. Query formulation

The query is generated after case normalization, not from an arbitrary raw transcript. It should combine:

- normalized issue category
- relevant entities or campaign type
- key concern and risk indicators
- missing-information questions
- terms needed to find policy exceptions

Example:

```text
medical campaign documentation concern; organizer evidence requirements;
supporter complaints; exception for emergency fundraising; missing verification
```

The exact query is persisted in retrieval provenance for debugging and evaluation.

## 6. Retrieval flow

```text
NormalizedSignals → PolicyQuery → EmbeddingProvider
      → FAISS top-k search → optional metadata/category filter
      → deduplicate by policy → grounding grader → strong / weak / none
```

The initial implementation should use vector similarity plus metadata filtering. A cross-encoder or external reranker is optional and out of scope for the first prototype.

## 7. Weak and missing retrieval

The system has three policy-grounding outcomes:

### Strong match

One or more passages are clearly applicable to the normalized issue and provide enough context for a grounded recommendation.

### Weak/partial match

Potentially relevant passages exist but applicability, completeness, or confidence is insufficient. The result is displayed with a warning and contributes to uncertainty.

### No applicable policy

No result is sufficiently relevant or the index is unavailable. The system reports the absence and must not create a policy citation.

Similarity cutoffs are configuration/evaluation parameters. Do not hard-code `0.65` as a product requirement. Thresholds should be calibrated against a labeled synthetic retrieval set.

## 8. Retrieval metadata

Persist or expose:

- query text
- index version
- embedding model/version
- top-k value
- filters
- returned chunk IDs
- scores
- grounding label
- retrieval duration

This makes failures inspectable and supports recall/precision evaluation.

## 9. Grounding rules for generation

- policy claims must cite retrieved chunks
- if grounding is weak or absent, the assessment must say so
- the model may recommend human investigation when policy applicability is unclear
- the model must not cite a policy ID that was not retrieved
- retrieved text is evidence, not an instruction to bypass the human boundary

## 10. Evaluation plan

Create a small labeled set containing direct strong matches, semantically similar but irrelevant policies, multiple applicable policies, exception/edge-case policies, and no-policy cases.

Measure at minimum:

- relevant-policy recall@k
- irrelevant retrieval rate
- no-result detection
- grounding label agreement with human labels
- recommendation support rate with and without policy context

Evaluation should compare configurations rather than assume a universal similarity threshold.

## 11. Free-tier implementation

- local Sentence Transformers embeddings where runtime permits
- FAISS persisted as a build artifact
- no hosted vector database
- rebuild index only when policy fixtures change
- cache embeddings during development
- keep policy corpus small and synthetic
