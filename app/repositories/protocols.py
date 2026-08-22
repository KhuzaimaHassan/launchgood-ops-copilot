"""Repository contracts for the domain persistence boundary."""

from typing import Protocol

from app.domain.models import AIAssessment, AuditEvent, Case, ReviewerDecision


class CaseRepository(Protocol):
    def save_case(self, case: Case) -> Case: ...

    def get_case(self, case_id: str) -> Case | None: ...

    def list_cases(self) -> list[Case]: ...


class AssessmentRepository(Protocol):
    def save_assessment(self, case_id: str, assessment: AIAssessment) -> AIAssessment: ...

    def list_assessments(self, case_id: str) -> list[AIAssessment]: ...


class DecisionRepository(Protocol):
    def save_decision(self, decision: ReviewerDecision) -> ReviewerDecision: ...

    def list_decisions(self, case_id: str) -> list[ReviewerDecision]: ...


class AuditRepository(Protocol):
    def save_audit_event(self, event: AuditEvent) -> AuditEvent: ...

    def list_audit_events(self, case_id: str) -> list[AuditEvent]: ...
