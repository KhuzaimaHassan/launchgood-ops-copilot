"""FastAPI application factory and thin route adapters."""


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import PROJECT_ROOT, AppConfig
from app.domain.models import Case, ReviewerDecision
from app.providers import get_llm_provider
from app.rag.retriever import LocalPolicyRetriever
from app.repositories.sqlite import SQLiteDatabase, SQLiteRepository
from app.services.services import AnalysisService, CaseService, DecisionService, EvaluationService
from app.workflow.runner import AssessmentWorkflow

from .schemas import (
    AuditResponse,
    CaseResponse,
    DecisionRequest,
    EvaluationRunResponse,
    HealthResponse,
)


def create_app(config: AppConfig | None = None) -> FastAPI:
    config = config or AppConfig.from_env()
    database = SQLiteDatabase(config.database_url)
    repository = SQLiteRepository(database)
    
    # Auto-seed synthetic cases if DB is fresh
    fixture_dir = PROJECT_ROOT / "data" / "fixtures" / "cases"
    if fixture_dir.exists():
        existing_ids = {c.case_id for c in repository.list_cases()}
        for path in sorted(fixture_dir.glob("*.json")):
            fixture = Case.model_validate_json(path.read_text(encoding="utf-8"))
            if fixture.case_id not in existing_ids:
                repository.save_case(fixture)

    policy_dir = PROJECT_ROOT / "data" / "policies"
    retriever = LocalPolicyRetriever.from_policy_directory(
        policy_dir, index_version=config.rag_index_version
    )
    workflow = AssessmentWorkflow(
        llm_provider=get_llm_provider(config),
        policy_retriever=retriever,
        repository=repository,
        config=config,
    )
    case_service = CaseService(repository)
    analysis_service = AnalysisService(repository, workflow)
    decision_service = DecisionService(repository)
    evaluation_service = EvaluationService(workflow)

    app = FastAPI(title="LaunchGood Ops Copilot", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.get("/cases", response_model=list[Case])
    def list_cases() -> list[Case]:
        return case_service.list_cases()

    @app.get("/cases/{case_id}", response_model=CaseResponse)
    def get_case(case_id: str) -> CaseResponse:
        case = case_service.get_case(case_id)
        if case is None:
            raise HTTPException(status_code=404, detail="case not found")
        return CaseResponse(
            case=case,
            assessment=analysis_service.latest_assessment(case_id),
            decisions=decision_service.list_decisions(case_id),
        )

    @app.post("/cases/{case_id}/analysis", response_model=CaseResponse)
    def analyze_case(case_id: str) -> CaseResponse:
        try:
            assessment = analysis_service.analyze(case_id)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="analysis failed") from exc
        case = case_service.get_case(case_id)
        assert case is not None
        return CaseResponse(case=case, assessment=assessment)

    @app.get("/cases/{case_id}/assessment", response_model=CaseResponse)
    def get_assessment(case_id: str) -> CaseResponse:
        case = case_service.get_case(case_id)
        if case is None:
            raise HTTPException(status_code=404, detail="case not found")
        return CaseResponse(
            case=case,
            assessment=analysis_service.latest_assessment(case_id),
            decisions=decision_service.list_decisions(case_id),
        )

    @app.post("/cases/{case_id}/decision")
    def record_decision(case_id: str, request: DecisionRequest) -> ReviewerDecision:
        decision = ReviewerDecision(case_id=case_id, **request.model_dump())
        try:
            return decision_service.decide(decision)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.get("/cases/{case_id}/audit", response_model=AuditResponse)
    def get_audit(case_id: str) -> AuditResponse:
        if case_service.get_case(case_id) is None:
            raise HTTPException(status_code=404, detail="case not found")
        events = [event.model_dump(mode="json") for event in repository.list_audit_events(case_id)]
        return AuditResponse(events=events)

    @app.post("/evaluation/runs", response_model=EvaluationRunResponse)
    def run_evaluation() -> EvaluationRunResponse:
        return EvaluationRunResponse.from_run(
            evaluation_service.run(
                case_service.list_cases(),
                expected_by_case=evaluation_service.load_ground_truth(),
            )
        )

    @app.get("/evaluation/runs/{run_id}", response_model=EvaluationRunResponse)
    def get_evaluation(run_id: str) -> EvaluationRunResponse:
        run = evaluation_service.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="evaluation run not found")
        return EvaluationRunResponse.from_run(run)

    return app
