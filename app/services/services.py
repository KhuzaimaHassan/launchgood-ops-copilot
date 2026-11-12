"""Application services and lifecycle enforcement for Phase 4."""

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.domain.enums import CaseStatus, DecisionType
from app.domain.models import AIAssessment, AuditEvent, Case, ReviewerDecision
from app.repositories.sqlite import SQLiteRepository
from app.workflow.runner import AssessmentWorkflow


def utc_now() -> datetime:
    return datetime.now(UTC)


class CaseService:
    def __init__(self, repository: SQLiteRepository) -> None:
        self.repository = repository

    def list_cases(self) -> list[Case]:
        return self.repository.list_cases()

    def get_case(self, case_id: str) -> Case | None:
        return self.repository.get_case(case_id)


class AnalysisService:
    def __init__(self, repository: SQLiteRepository, workflow: AssessmentWorkflow) -> None:
        self.repository = repository
        self.workflow = workflow

    def analyze(self, case_id: str) -> AIAssessment:
        case = self.repository.get_case(case_id)
        if case is None:
            raise LookupError(f"case not found: {case_id}")
        if case.status not in {CaseStatus.PENDING_ANALYSIS, CaseStatus.FAILED}:
            raise ValueError(f"case cannot be analyzed from state {case.status}")

        case.status = CaseStatus.ANALYZING
        case.updated_at = utc_now()
        self.repository.save_case(case)
        self._audit(case_id, "ANALYSIS_STARTED", {"status": case.status.value})
        try:
            assessment = self.workflow.run(case)
            assessment.case_id = case_id
        except Exception as exc:
            case.status = CaseStatus.FAILED
            case.updated_at = utc_now()
            self.repository.save_case(case)
            self._audit(case_id, "ANALYSIS_FAILED", {"error": type(exc).__name__})
            raise
        case.status = CaseStatus.AWAITING_HUMAN_DECISION
        case.updated_at = utc_now()
        self.repository.save_case(case)
        self._audit(case_id, "ANALYSIS_COMPLETED", {"assessment_id": assessment.assessment_id})
        return assessment

    def latest_assessment(self, case_id: str) -> AIAssessment | None:
        assessments = self.repository.list_assessments(case_id)
        return assessments[-1] if assessments else None

    def _audit(self, case_id: str, event_type: str, payload: dict[str, str]) -> None:
        self.repository.save_audit_event(
            AuditEvent(case_id=case_id, event_type=event_type, actor_type="SYSTEM", payload=payload)
        )


class DecisionService:
    def __init__(self, repository: SQLiteRepository) -> None:
        self.repository = repository

    def decide(self, decision: ReviewerDecision) -> ReviewerDecision:
        case = self.repository.get_case(decision.case_id)
        if case is None:
            raise LookupError(f"case not found: {decision.case_id}")
        if case.status is not CaseStatus.AWAITING_HUMAN_DECISION:
            raise ValueError(f"case cannot receive a decision from state {case.status}")
        assessments = self.repository.list_assessments(case.case_id)
        if assessments:
            decision.assessment_id = assessments[-1].assessment_id
        if decision.decision_type is DecisionType.ESCALATE:
            case.status = CaseStatus.ESCALATED
        else:
            case.status = CaseStatus.RESOLVED
        case.updated_at = utc_now()
        self.repository.save_decision(decision)
        self.repository.save_case(case)
        self.repository.save_audit_event(
            AuditEvent(
                case_id=case.case_id,
                event_type="DECISION_RECORDED",
                actor_type="REVIEWER",
                payload={"decision_id": decision.decision_id, "decision_type": decision.decision_type.value},
            )
        )
        return decision

    def list_decisions(self, case_id: str) -> list[ReviewerDecision]:
        return self.repository.list_decisions(case_id)


from app.config import PROJECT_ROOT


@dataclass
class EvaluationFailure:
    case_id: str
    title: str | None = None
    error: str | None = None
    mismatches: dict[str, str] | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class EvaluationRun:
    run_id: str
    total: int
    succeeded: int
    failed: int
    failures: list[EvaluationFailure]
    metrics: dict[str, float]


class EvaluationService:
    def __init__(self, workflow: AssessmentWorkflow) -> None:
        self.workflow = workflow
        self.runs: dict[str, EvaluationRun] = {}

    def run(self, cases: list[Case], expected_by_case: dict[str, dict] | None = None) -> EvaluationRun:
        run = EvaluationRun(
            run_id=f"eval-{uuid4().hex[:10]}",
            total=len(cases),
            succeeded=0,
            failed=0,
            failures=[],
            metrics={},
        )
        comparisons: list[dict[str, bool]] = []
        expected_map = expected_by_case or self.load_ground_truth()

        for case in cases:
            try:
                # Benchmarks must not replace the assessment a human actually reviewed.
                assessment = self.workflow.run(
                    case, analysis_run_id=f"{run.run_id}-{case.case_id}", persist=False
                )
                run.succeeded += 1
                expected = expected_map.get(case.case_id)
                if expected:
                    dim_comparison = {
                        "category": assessment.category == expected.get("expected_category"),
                        "risk": assessment.risk_level.value == expected.get("expected_risk"),
                        "priority": assessment.priority.value == expected.get("expected_priority"),
                        "action": assessment.recommendation_action.value == expected.get("expected_action"),
                        "escalation": assessment.escalation_recommended == expected.get("expected_escalation"),
                    }
                    comparisons.append(dim_comparison)
                    
                    mismatches: dict[str, str] = {}
                    for dim, match in dim_comparison.items():
                        if not match:
                            expected_key = f"expected_{dim}"
                            actual_val = getattr(assessment, "escalation_recommended" if dim == "escalation" else "category" if dim == "category" else f"{dim}_level" if dim == "risk" else f"{dim}" if dim == "priority" else "recommendation_action")
                            if hasattr(actual_val, "value"):
                                actual_val = actual_val.value
                            mismatches[dim] = f"actual '{actual_val}' vs expected '{expected.get(expected_key)}'"
                    if mismatches:
                        run.failures.append(
                            EvaluationFailure(
                                case_id=case.case_id,
                                title=case.title,
                                mismatches=mismatches,
                                tags=expected.get("tags", []),
                            )
                        )
            except Exception as exc:  # noqa: BLE001
                run.failed += 1
                run.failures.append(
                    EvaluationFailure(
                        case_id=case.case_id,
                        title=case.title,
                        error=type(exc).__name__,
                    )
                )

        if comparisons:
            for key in comparisons[0]:
                run.metrics[key] = round(
                    sum(1 for comparison in comparisons if comparison[key]) / len(comparisons), 3
                )
        self.runs[run.run_id] = run
        return run

    @staticmethod
    def load_ground_truth(path: Path | None = None) -> dict[str, dict]:
        path = path or (PROJECT_ROOT / "data" / "evaluation" / "ground_truth.json")
        if not path.exists():
            return {}
        return {item["case_id"]: item for item in json.loads(path.read_text(encoding="utf-8"))}

    def get(self, run_id: str) -> EvaluationRun | None:
        return self.runs.get(run_id)
