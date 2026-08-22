"""Smoke test for UI bootstrap and service wiring with isolated test DB."""

from app.config import PROJECT_ROOT, AppConfig
from app.domain.enums import CaseStatus
from app.domain.models import Case
from app.providers.fake import FakeLLMProvider
from app.rag.retriever import LocalPolicyRetriever
from app.repositories.sqlite import SQLiteDatabase, SQLiteRepository
from app.services.services import AnalysisService, CaseService
from app.workflow.runner import AssessmentWorkflow


def test_ui_build_services_bootstraps_sqlite_and_fixtures() -> None:
    config = AppConfig(database_url="sqlite:///:memory:")
    repository = SQLiteRepository(SQLiteDatabase(config.database_url))
    fixture_dir = PROJECT_ROOT / "data" / "fixtures" / "cases"
    
    for path in sorted(fixture_dir.glob("*.json")):
        repository.save_case(Case.model_validate_json(path.read_text(encoding="utf-8")))

    retriever = LocalPolicyRetriever.from_policy_directory(PROJECT_ROOT / "data" / "policies")
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=retriever,
        repository=repository,
        config=config,
    )
    
    case_service = CaseService(repository)
    analysis_service = AnalysisService(repository, workflow)
    
    cases = case_service.list_cases()
    assert len(cases) >= 5
    assert any(case.status is CaseStatus.PENDING_ANALYSIS for case in cases)
    
    # Verify isolated analysis execution
    first_case = cases[0]
    assessment = analysis_service.analyze(first_case.case_id)
    assert assessment.case_id == first_case.case_id
    assert assessment.confidence_score > 0
