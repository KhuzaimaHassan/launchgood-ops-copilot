from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.config import AppConfig
from app.domain.enums import CaseStatus, ConfidenceTier, DecisionType, Priority, RiskLevel
from app.domain.models import AIAssessment, Campaign, Case, EvidenceItem, ReviewerDecision


def make_case() -> Case:
    return Case(
        campaign=Campaign(title="Fictional campaign", description="Synthetic description"),
        title="Documentation review",
        intake_category="DOCUMENTATION_CONCERN",
        initial_priority=Priority.HIGH,
    )


def test_case_defaults_to_pending_analysis() -> None:
    case = make_case()
    assert case.status is CaseStatus.PENDING_ANALYSIS


def test_assessment_rejects_confidence_outside_canonical_range() -> None:
    with pytest.raises(ValidationError):
        AIAssessment(
            analysis_run_id="run-1",
            summary="summary",
            category="DOCUMENTATION_CONCERN",
            risk_level=RiskLevel.MEDIUM,
            priority=Priority.HIGH,
            confidence_score=1.01,
            confidence_tier=ConfidenceTier.HIGH,
            evidence=[
                EvidenceItem(
                    source_type="CAMPAIGN",
                    source_id="campaign-1",
                    fact="fact",
                    supports="RISK",
                )
            ],
            recommendation_action="INVESTIGATE",
            recommendation_rationale="rationale",
        )


def test_reviewer_decision_keeps_override_fields_optional() -> None:
    decision = ReviewerDecision(
        case_id="case-1",
        decision_type=DecisionType.MODIFY,
        reviewer_id="reviewer-1",
    )
    assert decision.overridden_risk is None
    assert decision.overridden_priority is None


def test_config_rejects_invalid_threshold_order() -> None:
    with pytest.raises(ValidationError):
        AppConfig(confidence_high_threshold=0.60, confidence_medium_threshold=0.70)


def test_timezone_aware_timestamp_is_accepted() -> None:
    case = make_case()
    case.updated_at = datetime.now(UTC)
    assert case.updated_at.tzinfo is not None
