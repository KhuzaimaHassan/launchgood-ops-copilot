"""Script to test all 9 live FastAPI endpoints on Render."""

import json
import urllib.request

BASE_URL = "https://launchgood-ops-copilot-m9jo.onrender.com"


def make_request(method: str, path: str, data: dict | None = None) -> tuple[int, dict | list | str]:
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            content = resp.read().decode("utf-8")
            try:
                payload = json.loads(content)
            except Exception:
                payload = content
            return status, payload
    except urllib.error.HTTPError as err:
        content = err.read().decode("utf-8")
        try:
            payload = json.loads(content)
        except Exception:
            payload = content
        return err.code, payload


def test_all_endpoints() -> None:
    print(f"=== Testing Live FastAPI Endpoints at {BASE_URL} ===\n")

    # 1. GET /health
    status, payload = make_request("GET", "/health")
    print(f"1. GET /health -> Status {status}: {payload}")

    # 2. GET /cases
    status, payload = make_request("GET", "/cases")
    case_count = len(payload) if isinstance(payload, list) else 0
    print(f"2. GET /cases -> Status {status}: Received {case_count} cases")

    # 3. GET /cases/case-1001
    status, payload = make_request("GET", "/cases/case-1001")
    curr_status = payload.get("case", {}).get("status") if isinstance(payload, dict) else "unknown"
    print(f"3. GET /cases/case-1001 -> Status {status}: Current status = '{curr_status}'")

    # 4. POST /cases/case-1001/analysis
    status, payload = make_request("POST", "/cases/case-1001/analysis")
    print(f"4. POST /cases/case-1001/analysis -> Status {status}")

    # 5. GET /cases/case-1001/assessment
    status, payload = make_request("GET", "/cases/case-1001/assessment")
    has_assessment = isinstance(payload, dict) and payload.get("assessment") is not None
    print(f"5. GET /cases/case-1001/assessment -> Status {status}: Has assessment = {has_assessment}")

    # 6. POST /cases/case-1001/decision
    decision_payload = {
        "reviewer_id": "rev-admin",
        "decision_type": "MODIFY",
        "overridden_risk": "MEDIUM",
        "reviewer_notes": "Live deployed test decision verification.",
    }
    status, payload = make_request("POST", "/cases/case-1001/decision", decision_payload)
    print(f"6. POST /cases/case-1001/decision -> Status {status}: {payload}")

    # 7. GET /cases/case-1001/audit
    status, payload = make_request("GET", "/cases/case-1001/audit")
    event_count = len(payload.get("events", [])) if isinstance(payload, dict) else 0
    print(f"7. GET /cases/case-1001/audit -> Status {status}: Received {event_count} audit events")

    # 8. POST /evaluation/runs
    status, payload = make_request("POST", "/evaluation/runs")
    run_id = payload.get("run_id") if isinstance(payload, dict) else None
    print(f"8. POST /evaluation/runs -> Status {status}: run_id = '{run_id}'")

    # 9. GET /evaluation/runs/{run_id}
    if run_id:
        status, payload = make_request("GET", f"/evaluation/runs/{run_id}")
        total = payload.get("total") if isinstance(payload, dict) else 0
        print(f"9. GET /evaluation/runs/{run_id} -> Status {status}: total evaluated = {total}")

    print("\n=== Live API Endpoint Verification Complete ===")


if __name__ == "__main__":
    test_all_endpoints()
