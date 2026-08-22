"""Validated domain models for Phase 0 contracts."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import (
    CaseStatus,
    ConfidenceTier,
    DecisionType,
    GroundingStatus,
    Priority,
    RecommendationAction,
    RiskLevel,
    SourceType,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class SourceRecord(ContractModel):
    source_id: str = Field(min_length=1)
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class Campaign(ContractModel):
    campaign_id: str = Field(default_factory=lambda: f"campaign-{uuid4().hex[:10]}", min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    organizer_summary: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class SupportMessage(SourceRecord):
    case_id: str = Field(min_length=1)
    channel: str = Field(min_length=1)
    author_role: str = Field(min_length=1)


class CampaignUpdate(SourceRecord):
    campaign_id: str = Field(min_length=1)


class RiskSignal(ContractModel):
    signal_id: str = Field(default_factory=lambda: f"signal-{uuid4().hex[:10]}", min_length=1)
    case_id: str = Field(min_length=1)
    signal_type: str = Field(min_length=1)
    value: dict[str, Any] = Field(default_factory=dict)
    severity: RiskLevel
    source_ref: str | None = None


class Case(ContractModel):
    case_id: str = Field(default_factory=lambda: f"case-{uuid4().hex[:10]}", min_length=1)
    campaign: Campaign
    title: str = Field(min_length=1)
    intake_category: str = Field(min_length=1)
    initial_priority: Priority
    status: CaseStatus = CaseStatus.PENDING_ANALYSIS
    support_messages: list[SupportMessage] = Field(default_factory=list)
    campaign_updates: list[CampaignUpdate] = Field(default_factory=list)
    risk_signals: list[RiskSignal] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @field_validator("updated_at")
    @classmethod
    def updated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamps must include timezone information")
        return value


class PolicyReference(ContractModel):
    policy_reference_id: str = Field(default_factory=lambda: f"policy-ref-{uuid4().hex[:10]}")
    policy_id: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)
    retrieval_score: float = Field(ge=0.0)
    grounding_status: GroundingStatus
    excerpt: str = Field(min_length=1)


class EvidenceItem(ContractModel):
    evidence_id: str = Field(default_factory=lambda: f"evidence-{uuid4().hex[:10]}")
    source_type: SourceType
    source_id: str = Field(min_length=1)
    fact: str = Field(min_length=1)
    supports: str = Field(min_length=1)


class AIAssessment(ContractModel):
    assessment_id: str = Field(default_factory=lambda: f"assessment-{uuid4().hex[:10]}")
    analysis_run_id: str = Field(min_length=1)
    case_id: str | None = None
    summary: str = Field(min_length=1)
    category: str = Field(min_length=1)
    risk_level: RiskLevel
    priority: Priority
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_tier: ConfidenceTier
    evidence: list[EvidenceItem] = Field(min_length=1)
    policy_references: list[PolicyReference] = Field(default_factory=list)
    recommendation_action: RecommendationAction
    recommendation_rationale: str = Field(min_length=1)
    uncertainty_flags: list[str] = Field(default_factory=list)
    human_review_required: bool = True
    escalation_recommended: bool = False
    created_at: datetime = Field(default_factory=utc_now)


class ReviewerDecision(ContractModel):
    decision_id: str = Field(default_factory=lambda: f"decision-{uuid4().hex[:10]}")
    case_id: str = Field(min_length=1)
    assessment_id: str | None = None
    decision_type: DecisionType
    overridden_risk: RiskLevel | None = None
    overridden_priority: Priority | None = None
    overridden_recommendation: str | None = None
    reviewer_notes: str | None = None
    reviewer_id: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class AuditEvent(ContractModel):
    event_id: str = Field(default_factory=lambda: f"event-{uuid4().hex[:10]}")
    case_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    actor_type: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
