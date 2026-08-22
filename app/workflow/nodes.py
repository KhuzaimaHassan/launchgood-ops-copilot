"""Single-purpose assessment workflow nodes."""

import json

from app.domain.enums import GroundingStatus, Priority, RecommendationAction, RiskLevel
from app.domain.models import AIAssessment, EvidenceItem, PolicyReference
from app.providers.protocols import LLMProvider, PolicyRetriever

from .state import (
    AssessmentDraft,
    ConflictFlag,
    NormalizedFact,
    NormalizedRiskIndicator,
    NormalizedSignals,
    PolicyQuery,
    WorkflowError,
    WorkflowState,
)


def normalize_case(state: WorkflowState) -> WorkflowState:
    case = state.case
    facts = [
        NormalizedFact(fact=case.campaign.description, source_id=case.campaign.campaign_id)
    ]
    facts.extend(
        NormalizedFact(fact=message.content, source_id=message.source_id)
        for message in case.support_messages
    )
    facts.extend(
        NormalizedFact(fact=update.content, source_id=update.source_id)
        for update in case.campaign_updates
    )
    indicators = [
        NormalizedRiskIndicator(
            indicator=f"{signal.signal_type}: {signal.value}",
            severity=signal.severity.value,
            source_id=signal.source_ref or signal.signal_id,
        )
        for signal in case.risk_signals
    ]
    questions: list[str] = []
    if any(signal.signal_type == "DOCUMENTATION" for signal in case.risk_signals):
        questions.append("What supporting documentation is available?")
    state.normalized_signals = NormalizedSignals(
        issue_category_candidates=[case.intake_category],
        entities=[case.campaign.title],
        key_facts=facts,
        risk_indicators=indicators,
        missing_information_questions=questions,
    )
    return state


def formulate_policy_query(state: WorkflowState) -> WorkflowState:
    if state.normalized_signals is None:
        raise ValueError("normalized signals are required before policy query formulation")
    signals = state.normalized_signals
    indicator_terms = [indicator.indicator.split(":", 1)[0] for indicator in signals.risk_indicators]
    terms = list(signals.issue_category_candidates) + indicator_terms + signals.missing_information_questions
    intake_category = signals.issue_category_candidates[0]
    policy_category = intake_category.removesuffix("_CONCERN")
    state.policy_query = PolicyQuery(
        text="; ".join(terms),
        category=policy_category,
        terms=terms,
    )
    return state


def retrieve_policy(state: WorkflowState, retriever: PolicyRetriever) -> WorkflowState:
    if state.policy_query is None:
        raise ValueError("policy query is required before retrieval")
    matches, metadata = retriever.search(
        query=state.policy_query.text,
        category=state.policy_query.category,
    )
    state.policy_matches = matches
    state.policy_grounding = GroundingStatus(metadata["grounding_status"])
    return state


def extract_evidence_and_conflicts(state: WorkflowState) -> WorkflowState:
    if state.normalized_signals is None:
        raise ValueError("normalized signals are required before evidence extraction")
    state.evidence_items = []
    for fact in state.normalized_signals.key_facts:
        is_risk = indicator_match(fact.source_id, state)
        state.evidence_items.append(
            EvidenceItem(
                source_type="RISK_SIGNAL" if is_risk else "CAMPAIGN",
                source_id=fact.source_id,
                fact=fact.fact,
                supports="RISK" if is_risk else "CATEGORY",
            )
        )
    if not state.evidence_items:
        state.errors.append(WorkflowError(code="INSUFFICIENT_EVIDENCE", message="No source facts found"))
    return state


def indicator_match(source_id: str, state: WorkflowState) -> bool:
    return any(indicator.source_id == source_id for indicator in state.normalized_signals.risk_indicators) if state.normalized_signals else False


def detect_conflicts(state: WorkflowState) -> WorkflowState:
    if state.normalized_signals is None:
        return state
    facts = state.normalized_signals.key_facts
    for left_index, left in enumerate(facts):
        for right in facts[left_index + 1 :]:
            if left.source_id != right.source_id and {"already", "requires"}.issubset(
                set((left.fact + " " + right.fact).lower().split())
            ):
                state.conflicts.append(
                    ConflictFlag(
                        description="Potentially conflicting source language detected",
                        source_ids=[left.source_id, right.source_id],
                    )
                )
    return state


def generate_assessment(state: WorkflowState, provider: LLMProvider) -> WorkflowState:
    prompt = "WORKFLOW_CONTEXT_JSON=" + json.dumps(state.context_for_prompt())
    draft, metadata = provider.generate_structured(prompt=prompt, schema=AssessmentDraft)
    state.assessment_draft = draft
    state.provider_metadata = metadata
    return state


def validate_assessment(state: WorkflowState) -> WorkflowState:
    if state.assessment_draft is None:
        raise ValueError("assessment draft is required")
    try:
        state.assessment_draft = AssessmentDraft.model_validate(state.assessment_draft)
    except Exception as exc:  # noqa: BLE001
        state.errors.append(
            WorkflowError(code="INVALID_ASSESSMENT", message=str(exc), retryable=True)
        )
        state.assessment_draft = None
    return state


def derive_confidence_and_flags(
    state: WorkflowState, *, high_threshold: float = 0.80, medium_threshold: float = 0.55
) -> WorkflowState:
    if state.assessment_draft is None:
        raise ValueError("valid assessment draft is required")
    draft = state.assessment_draft
    flags = list(draft.uncertainty_flags)
    if state.policy_grounding is not GroundingStatus.STRONG:
        flags.append(
            "NO_APPLICABLE_POLICY"
            if state.policy_grounding is GroundingStatus.NONE
            else "WEAK_POLICY_GROUNDING"
        )
    if state.conflicts:
        flags.append("CONFLICTING_EVIDENCE")
    if state.errors:
        flags.append("INSUFFICIENT_EVIDENCE")
    score = draft.confidence_score
    tier = "HIGH" if score >= high_threshold else "MEDIUM" if score >= medium_threshold else "LOW"
    state.assessment = AIAssessment(
        analysis_run_id=state.analysis_run_id,
        summary=draft.summary,
        category=draft.category,
        risk_level=RiskLevel(draft.risk_level),
        priority=Priority(draft.priority),
        confidence_score=score,
        confidence_tier=tier,
        evidence=draft.evidence,
        policy_references=[
            PolicyReference(
                policy_id=match.policy_id,
                chunk_id=match.chunk_id,
                retrieval_score=match.score,
                grounding_status=match.grounding_status,
                excerpt=match.excerpt,
            )
            for match in state.policy_matches
        ],
        recommendation_action=RecommendationAction(draft.recommendation_action),
        recommendation_rationale=draft.recommendation_rationale,
        uncertainty_flags=sorted(set(flags)),
        human_review_required=True,
        escalation_recommended=draft.escalation_recommended or bool(state.conflicts),
    )
    return state
