from pathlib import Path

from app.domain.models import Case
from app.providers.fake import FakeLLMProvider
from app.rag.retriever import LocalPolicyRetriever
from app.workflow.runner import AssessmentWorkflow


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
