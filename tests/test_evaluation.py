from pathlib import Path

from app.domain.models import Case
from app.providers.fake import FakeLLMProvider
from app.rag.retriever import LocalPolicyRetriever
from app.services.services import EvaluationService
from app.workflow.runner import AssessmentWorkflow


def test_evaluation_reports_ground_truth_metrics() -> None:
    cases = [
        Case.model_validate_json(path.read_text())
        for path in sorted(Path("data/fixtures/cases").glob("*.json"))
    ]
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
    )
    service = EvaluationService(workflow)
    result = service.run(cases, expected_by_case=service.load_ground_truth())

    assert result.total == 5
    assert result.succeeded == 5
    assert "category" in result.metrics
    assert "escalation" in result.metrics
    assert result.failed == 0
    assert result.failures == []
    assert result.metrics == dict.fromkeys(
        ["category", "risk", "priority", "action", "escalation"], 1.0
    )


def test_evaluation_contains_conflict_and_no_policy_cases() -> None:
    cases = [
        Case.model_validate_json(Path("data/fixtures/cases/case-1003.json").read_text()),
        Case.model_validate_json(Path("data/fixtures/cases/case-1004.json").read_text()),
    ]
    workflow = AssessmentWorkflow(
        llm_provider=FakeLLMProvider(),
        policy_retriever=LocalPolicyRetriever.from_policy_directory(Path("data/policies")),
    )

    conflict = workflow.run(cases[0])
    no_policy = workflow.run(cases[1])
    assert "CONFLICTING_EVIDENCE" in conflict.uncertainty_flags
    assert "NO_APPLICABLE_POLICY" in no_policy.uncertainty_flags
