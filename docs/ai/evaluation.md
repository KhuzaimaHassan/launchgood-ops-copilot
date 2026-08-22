# AI Evaluation Plan

**Status:** Proposed implementation baseline v0.1

## 1. Evaluation goals

Evaluation answers:

- Does the workflow identify the right issue and risk?
- Does it retrieve applicable policy?
- Are recommendations supported by source evidence?
- Does it recognize uncertainty and conflicts?
- Does it preserve the human boundary?

The goal is to expose failure modes, not manufacture a single impressive accuracy number.

## 2. Dataset composition

The first dataset should contain 30–50 synthetic cases across:

- straightforward documentation concerns
- normal/no-action cases
- complaints
- unusual risk signals
- missing information
- conflicting information
- irrelevant or missing policy
- cases requiring escalation

Every case has expected labels and a short rationale written before model output is reviewed.

## 3. Metrics

| Area | Metric |
|---|---|
| category | accuracy and macro F1 |
| risk | macro F1 and confusion matrix |
| priority | accuracy |
| recommendation | exact/semantic agreement with expected action |
| evidence | source-reference precision and support rate |
| RAG | recall@k and irrelevant retrieval rate |
| uncertainty | difficult-case flag recall |
| human boundary | prohibited-action rate, target zero |
| operations | latency, provider failures, repair rate |

Human override rate is descriptive, not an accuracy metric. It may indicate disagreement or appropriate reviewer judgment.

## 4. Evaluation run artifact

Each run stores:

- dataset version
- workflow version
- model/provider configuration
- RAG index and embedding versions
- timestamp
- aggregate metrics
- per-case output
- expected output
- failure reasons

## 5. Release gate

The prototype is not ready for public demonstration if:

- structured output frequently fails validation
- evidence references cannot be traced to source records
- policy claims appear without retrieved policy
- conflicting cases are confidently resolved without a flag
- the model proposes autonomous consequential actions
- evaluation cannot be repeated from documented configuration

Exact numeric quality thresholds are finalized after the first baseline run; the behavioral safety gates above are mandatory from the start.
