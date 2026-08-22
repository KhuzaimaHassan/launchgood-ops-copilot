"""Sequential fallback runner for the bounded workflow graph."""

from uuid import uuid4

from app.config import AppConfig
from app.domain.models import AIAssessment, Case
from app.providers.protocols import LLMProvider, PolicyRetriever
from app.repositories.sqlite import SQLiteRepository

from .nodes import (
    derive_confidence_and_flags,
    detect_conflicts,
    extract_evidence_and_conflicts,
    formulate_policy_query,
    generate_assessment,
    normalize_case,
    retrieve_policy,
    validate_assessment,
)
from .state import WorkflowState


class AssessmentWorkflow:
    def __init__(
        self,
        *,
        llm_provider: LLMProvider,
        policy_retriever: PolicyRetriever,
        repository: SQLiteRepository | None = None,
        config: AppConfig | None = None,
    ) -> None:
        self.llm_provider = llm_provider
        self.policy_retriever = policy_retriever
        self.repository = repository
        self.config = config or AppConfig()

    def run(self, case: Case, *, analysis_run_id: str | None = None) -> AIAssessment:
        state = WorkflowState(
            case=case,
            analysis_run_id=analysis_run_id or f"run-{uuid4().hex[:10]}",
        )
        normalize_case(state)
        formulate_policy_query(state)
        retrieve_policy(state, self.policy_retriever)
        extract_evidence_and_conflicts(state)
        detect_conflicts(state)

        while state.assessment_draft is None and state.retry_count <= self.config.max_analysis_retries:
            state.errors.clear()
            generate_assessment(state, self.llm_provider)
            validate_assessment(state)
            if state.assessment_draft is None:
                state.retry_count += 1
        if state.assessment_draft is None:
            raise RuntimeError("assessment validation failed after bounded retries")

        derive_confidence_and_flags(
            state,
            high_threshold=self.config.confidence_high_threshold,
            medium_threshold=self.config.confidence_medium_threshold,
        )
        assert state.assessment is not None
        if self.repository:
            self.repository.save_assessment(case.case_id, state.assessment)
        return state.assessment
