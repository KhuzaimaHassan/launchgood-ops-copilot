from pathlib import Path

import pytest

from app.config import AppConfig
from app.domain.enums import ConfidenceTier, GroundingStatus, Priority, RiskLevel
from app.domain.models import Case
from app.providers.fake import FakeLLMProvider
from app.rag.retriever import LocalPolicyRetriever
from app.workflow.nodes import derive_confidence_and_flags
from app.workflow.runner import AssessmentWorkflow
from app.workflow.state import AssessmentDraft, WorkflowState


def test_assessment_workflow_returns_grounded_structured_result() -> None:
    case = Case.model_validate_json(Path("data/fixtures/cases/case-1001.json").read_text())
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
    )

    assessment = workflow.run(case)

    assert assessment.analysis_run_id.startswith("run-")
    assert assessment.confidence_score <= 1.0
    assert assessment.human_review_required is True
    assert assessment.evidence


def test_conflicting_records_without_intake_signals_require_high_priority_review() -> None:
    case = Case.model_validate_json(Path("data/fixtures/cases/case-1003.json").read_text())
    assert not case.risk_signals
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
    )
    assessment = workflow.run(case)

    assert assessment.risk_level is RiskLevel.HIGH
    assert assessment.priority is Priority.HIGH
    assert assessment.escalation_recommended
    assert assessment.human_review_required
    assert "CONFLICTING_EVIDENCE" in assessment.uncertainty_flags
    assert assessment.confidence_score == 0.54
    assert assessment.confidence_tier is ConfidenceTier.LOW
    assert {"update-1003-01", "update-1003-02"} <= {
        item.source_id for item in assessment.evidence
    }


def test_no_policy_case_is_low_confidence_without_inventing_high_risk() -> None:
    case = Case.model_validate_json(Path("data/fixtures/cases/case-1004.json").read_text())
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
    )
    assessment = workflow.run(case)
    assert assessment.risk_level is RiskLevel.LOW
    assert "NO_APPLICABLE_POLICY" in assessment.uncertainty_flags
    assert assessment.confidence_score == 0.54
    assert assessment.confidence_tier is ConfidenceTier.LOW


@pytest.mark.parametrize(
    ("grounding", "provider_score", "expected_score", "expected_tier"),
    [
        (GroundingStatus.STRONG, 0.88, 0.88, ConfidenceTier.HIGH),
        (GroundingStatus.WEAK, 0.88, 0.79, ConfidenceTier.MEDIUM),
        (GroundingStatus.NONE, 0.88, 0.54, ConfidenceTier.LOW),
        (GroundingStatus.NONE, 0.20, 0.20, ConfidenceTier.LOW),
    ],
)
def test_grounding_caps_never_raise_provider_confidence(
    grounding, provider_score, expected_score, expected_tier
) -> None:
    case = Case.model_validate_json(Path("data/fixtures/cases/case-1002.json").read_text())
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
    )
    baseline = workflow.run(case)
    draft = AssessmentDraft(
        summary=baseline.summary, category=baseline.category,
        risk_level=baseline.risk_level.value, priority=baseline.priority.value,
        confidence_score=provider_score, evidence=baseline.evidence,
        recommendation_action=baseline.recommendation_action.value,
        recommendation_rationale=baseline.recommendation_rationale,
    )
    state = WorkflowState(
        case=case, analysis_run_id="confidence-test", assessment_draft=draft,
        policy_grounding=grounding,
    )
    derive_confidence_and_flags(state)
    assert state.assessment.confidence_score == expected_score
    assert state.assessment.confidence_tier is expected_tier


def test_uncertainty_caps_follow_configured_confidence_tiers() -> None:
    config = AppConfig(confidence_high_threshold=0.70, confidence_medium_threshold=0.40)
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
        config=config,
    )
    case = Case.model_validate_json(Path("data/fixtures/cases/case-1003.json").read_text())
    assessment = workflow.run(case)
    assert assessment.confidence_score == 0.39
    assert assessment.confidence_tier is ConfidenceTier.LOW
