from pathlib import Path

from app.domain.enums import CaseStatus, DecisionType
from app.domain.models import Case, ReviewerDecision
from app.providers.fake import FakeLLMProvider
from app.rag.retriever import LocalPolicyRetriever
from app.repositories.sqlite import SQLiteDatabase, SQLiteRepository
from app.services.services import AnalysisService, DecisionService
from app.workflow.runner import AssessmentWorkflow


def build_services() -> tuple[SQLiteRepository, AnalysisService, DecisionService]:
    repository = SQLiteRepository(SQLiteDatabase("sqlite:///:memory:"))
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
        repository=repository,
    )
    return repository, AnalysisService(repository, workflow), DecisionService(repository)


def test_analysis_and_decision_enforce_lifecycle() -> None:
    case = Case.model_validate_json(Path("data/fixtures/cases/case-1001.json").read_text())
    repository, analysis, decisions = build_services()
    repository.save_case(case)

    assessment = analysis.analyze(case.case_id)
    assert assessment.human_review_required is True
    assert repository.get_case(case.case_id).status is CaseStatus.AWAITING_HUMAN_DECISION

    decisions.decide(
        ReviewerDecision(
            case_id=case.case_id,
            assessment_id=assessment.assessment_id,
            decision_type=DecisionType.MODIFY,
            reviewer_id="reviewer-1",
            reviewer_notes="Synthetic review note",
        )
    )
    assert repository.get_case(case.case_id).status is CaseStatus.RESOLVED
