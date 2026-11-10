"""HTTP request and response schemas."""


from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import DecisionType, Priority, RiskLevel
from app.domain.models import AIAssessment, Case, ReviewerDecision
from app.services.services import EvaluationRun


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision_type: DecisionType
    overridden_risk: RiskLevel | None = None
    overridden_priority: Priority | None = None
    overridden_recommendation: str | None = None
    reviewer_notes: str | None = None
    reviewer_id: str = Field(min_length=1)


class EvaluationFailure(BaseModel):
    case_id: str
    title: str | None = None
    error: str | None = None
    mismatches: dict[str, str] | None = None
    tags: list[str] = Field(default_factory=list)


class EvaluationRunResponse(BaseModel):
    run_id: str
    total: int
    succeeded: int
    failed: int
    failures: list[EvaluationFailure]
    metrics: dict[str, float]

    @classmethod
    def from_run(cls, run: EvaluationRun) -> "EvaluationRunResponse":
        return cls(
            run_id=run.run_id,
            total=run.total,
            succeeded=run.succeeded,
            failed=run.failed,
            failures=[
                EvaluationFailure(**f.__dict__) if hasattr(f, "__dict__") else EvaluationFailure(**f)
                for f in run.failures
            ],
            metrics=run.metrics,
        )


class CaseResponse(BaseModel):
    case: Case
    assessment: AIAssessment | None = None
    decisions: list[ReviewerDecision] = Field(default_factory=list)


class AuditResponse(BaseModel):
    events: list[dict]


class HealthResponse(BaseModel):
    status: str
