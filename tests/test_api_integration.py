"""FastAPI REST API integration tests using Starlette TestClient."""

import pytest
from starlette.testclient import TestClient

from app.api.app import create_app
from app.config import AppConfig


@pytest.fixture
def api_client():
    config = AppConfig(database_url="sqlite:///:memory:")
    app = create_app(config)
    return TestClient(app)


def test_api_health_endpoint(api_client: TestClient) -> None:
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_list_cases_endpoint(api_client: TestClient) -> None:
    response = api_client.get("/cases")
    assert response.status_code == 200
    cases = response.json()
    assert isinstance(cases, list)
    assert len(cases) >= 5
    case_ids = {c["case_id"] for c in cases}
    assert "case-1001" in case_ids


def test_api_get_case_details_endpoint(api_client: TestClient) -> None:
    response = api_client.get("/cases/case-1001")
    assert response.status_code == 200
    data = response.json()
    assert "case" in data
    assert data["case"]["case_id"] == "case-1001"
    assert "campaign" in data["case"]


def test_api_analyze_case_endpoint(api_client: TestClient) -> None:
    response = api_client.post("/cases/case-1001/analysis")
    assert response.status_code == 200
    data = response.json()
    assert data["case"]["status"] == "AWAITING_HUMAN_DECISION"
    assert data["assessment"] is not None
    assert data["assessment"]["confidence_score"] > 0
    assert "category" in data["assessment"]
    assert "risk_level" in data["assessment"]
    assert "evidence" in data["assessment"]
    assert "policy_references" in data["assessment"]


def test_api_record_decision_endpoint(api_client: TestClient) -> None:
    # First analyze case-1001 to transition status to AWAITING_HUMAN_DECISION
    api_client.post("/cases/case-1001/analysis")

    decision_payload = {
        "decision_type": "APPROVE",
        "overridden_risk": None,
        "overridden_priority": None,
        "overridden_recommendation": None,
        "reviewer_notes": "Integration test approval notes.",
        "reviewer_id": "test-reviewer-01",
    }
    response = api_client.post("/cases/case-1001/decision", json=decision_payload)
    assert response.status_code == 200
    decision = response.json()
    assert decision["case_id"] == "case-1001"
    assert decision["decision_type"] == "APPROVE"

    # Verify updated status
    case_res = api_client.get("/cases/case-1001")
    assert case_res.json()["case"]["status"] == "RESOLVED"


def test_api_get_audit_history_endpoint(api_client: TestClient) -> None:
    api_client.post("/cases/case-1001/analysis")
    response = api_client.get("/cases/case-1001/audit")
    assert response.status_code == 200
    audit = response.json()
    assert "events" in audit
    assert len(audit["events"]) > 0
    first_event = audit["events"][0]
    assert "event_id" in first_event
    assert "event_type" in first_event
    assert "actor_type" in first_event
    assert "payload" in first_event


@pytest.mark.parametrize("action", ["APPROVE", "MODIFY", "REJECT", "ESCALATE"])
def test_case_reload_retains_final_decision_and_original_assessment(api_client, action) -> None:
    original = api_client.post("/cases/case-1003/analysis").json()["assessment"]
    payload = {
        "decision_type": action, "overridden_risk": "MEDIUM",
        "overridden_priority": "URGENT",
        "overridden_recommendation": "Synthetic QA: verify the hospital documents.",
        "reviewer_notes": "Synthetic QA: contradictory procedure updates require review.",
        "reviewer_id": "qa-reviewer",
    }
    response = api_client.post("/cases/case-1003/decision", json=payload)
    assert response.status_code == 200
    recorded = response.json()
    assert recorded["assessment_id"] == original["assessment_id"]
    assert api_client.post("/evaluation/runs").status_code == 200
    for route in ["/cases/case-1003", "/cases/case-1003/assessment"]:
        detail = api_client.get(route).json()
        assert detail["assessment"] == original
        assert detail["decisions"] == [recorded]
        assert detail["case"]["status"] == ("ESCALATED" if action == "ESCALATE" else "RESOLVED")
    other_case = api_client.get("/cases/case-1002").json()
    assert other_case["decisions"] == []
    assert api_client.post("/cases/case-1003/decision", json=payload).status_code == 409
    assert len(api_client.get("/cases/case-1003").json()["decisions"]) == 1


def test_api_evaluation_runs_endpoint(api_client: TestClient) -> None:
    response = api_client.post("/evaluation/runs")
    assert response.status_code == 200
    run = response.json()
    assert "run_id" in run
    assert run["total"] >= 5
    assert "metrics" in run
    assert "category" in run["metrics"]
    assert "action" in run["metrics"]
    assert "escalation" in run["metrics"]
    assert "risk" in run["metrics"]
    assert "priority" in run["metrics"]
    assert "failures" in run
    if run["failures"]:
        first_failure = run["failures"][0]
        assert "case_id" in first_failure
        assert "title" in first_failure
        assert "mismatches" in first_failure or "error" in first_failure
        assert "tags" in first_failure
