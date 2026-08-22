"""Typed state carried through the assessment workflow."""

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import GroundingStatus
from app.domain.models import AIAssessment, Case, EvidenceItem
from app.providers.protocols import PolicyMatch, ProviderMetadata


class WorkflowModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NormalizedFact(WorkflowModel):
    fact: str = Field(min_length=1)
    source_id: str = Field(min_length=1)


class NormalizedRiskIndicator(WorkflowModel):
    indicator: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    source_id: str | None = None


class NormalizedSignals(WorkflowModel):
    issue_category_candidates: list[str] = Field(min_length=1)
    entities: list[str] = Field(default_factory=list)
    key_facts: list[NormalizedFact] = Field(default_factory=list)
    risk_indicators: list[NormalizedRiskIndicator] = Field(default_factory=list)
    missing_information_questions: list[str] = Field(default_factory=list)


class PolicyQuery(WorkflowModel):
    text: str = Field(min_length=1)
    category: str | None = None
    terms: list[str] = Field(default_factory=list)


class ConflictFlag(WorkflowModel):
    description: str = Field(min_length=1)
    source_ids: list[str] = Field(min_length=2)


class WorkflowError(WorkflowModel):
    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    retryable: bool = False


class AssessmentDraft(WorkflowModel):
    summary: str = Field(min_length=1)
    category: str = Field(min_length=1)
    risk_level: str = Field(min_length=1)
    priority: str = Field(min_length=1)
    confidence_score: float = Field(ge=0.0, le=1.0)
    evidence: list[EvidenceItem] = Field(min_length=1)
    recommendation_action: str = Field(min_length=1)
    recommendation_rationale: str = Field(min_length=1)
    uncertainty_flags: list[str] = Field(default_factory=list)
    human_review_required: bool = True
    escalation_recommended: bool = False


@dataclass
class WorkflowState:
    case: Case
    analysis_run_id: str
    normalized_signals: NormalizedSignals | None = None
    policy_query: PolicyQuery | None = None
    policy_matches: list[PolicyMatch] = field(default_factory=list)
    policy_grounding: GroundingStatus = GroundingStatus.NONE
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    conflicts: list[ConflictFlag] = field(default_factory=list)
    assessment_draft: AssessmentDraft | None = None
    assessment: AIAssessment | None = None
    provider_metadata: ProviderMetadata | None = None
    retry_count: int = 0
    errors: list[WorkflowError] = field(default_factory=list)

    def context_for_prompt(self) -> dict[str, Any]:
        return {
            "analysis_run_id": self.analysis_run_id,
            "normalized_signals": self.normalized_signals.model_dump()
            if self.normalized_signals
            else None,
            "policy_query": self.policy_query.model_dump() if self.policy_query else None,
            "policy_matches": [match.__dict__ for match in self.policy_matches],
            "evidence_items": [item.model_dump() for item in self.evidence_items],
            "conflicts": [conflict.model_dump() for conflict in self.conflicts],
        }
