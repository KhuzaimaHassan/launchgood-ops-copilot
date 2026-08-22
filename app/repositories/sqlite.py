"""Small SQLite persistence adapter for the prototype domain contracts."""

import sqlite3
from pathlib import Path

from app.domain.models import AIAssessment, AuditEvent, Case, ReviewerDecision


class SQLiteDatabase:
    def __init__(self, database_url: str = "sqlite:///./data/app.db") -> None:
        self.path = self._path_from_url(database_url)
        if self.path != Path(":memory:"):
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path.as_posix(), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    @staticmethod
    def _path_from_url(database_url: str) -> Path:
        if database_url == "sqlite:///:memory:":
            return Path(":memory:")
        prefix = "sqlite:///"
        if not database_url.startswith(prefix):
            raise ValueError("Phase 1 SQLite repository requires a sqlite:/// database URL")
        return Path(database_url.removeprefix(prefix))

    def initialize(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()


class SQLiteRepository:
    """Repository collection sharing one SQLite connection."""

    def __init__(self, database: SQLiteDatabase) -> None:
        self.db = database

    def save_case(self, case: Case) -> Case:
        payload = case.model_dump_json()
        self.db.connection.execute(
            """INSERT INTO cases(case_id, payload, created_at, updated_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(case_id) DO UPDATE SET payload=excluded.payload,
               updated_at=excluded.updated_at""",
            (case.case_id, payload, case.created_at.isoformat(), case.updated_at.isoformat()),
        )
        self.db.connection.commit()
        return case

    def get_case(self, case_id: str) -> Case | None:
        row = self.db.connection.execute(
            "SELECT payload FROM cases WHERE case_id = ?", (case_id,)
        ).fetchone()
        return Case.model_validate_json(row["payload"]) if row else None

    def list_cases(self) -> list[Case]:
        rows = self.db.connection.execute(
            "SELECT payload FROM cases ORDER BY created_at"
        ).fetchall()
        return [Case.model_validate_json(row["payload"]) for row in rows]

    def save_assessment(self, case_id: str, assessment: AIAssessment) -> AIAssessment:
        self._save_payload(
            "assessments",
            assessment.assessment_id,
            case_id,
            assessment.model_dump_json(),
            assessment.created_at.isoformat(),
        )
        return assessment

    def list_assessments(self, case_id: str) -> list[AIAssessment]:
        return [
            AIAssessment.model_validate_json(row["payload"])
            for row in self._rows("assessments", case_id)
        ]

    def save_decision(self, decision: ReviewerDecision) -> ReviewerDecision:
        self._save_payload(
            "decisions",
            decision.decision_id,
            decision.case_id,
            decision.model_dump_json(),
            decision.created_at.isoformat(),
        )
        return decision

    def list_decisions(self, case_id: str) -> list[ReviewerDecision]:
        return [
            ReviewerDecision.model_validate_json(row["payload"])
            for row in self._rows("decisions", case_id)
        ]

    def save_audit_event(self, event: AuditEvent) -> AuditEvent:
        self._save_payload(
            "audit_events",
            event.event_id,
            event.case_id,
            event.model_dump_json(),
            event.created_at.isoformat(),
        )
        return event

    def list_audit_events(self, case_id: str) -> list[AuditEvent]:
        return [
            AuditEvent.model_validate_json(row["payload"])
            for row in self._rows("audit_events", case_id)
        ]

    def _save_payload(
        self, table: str, record_id: str, case_id: str, payload: str, created_at: str
    ) -> None:
        self.db.connection.execute(
            f"INSERT OR REPLACE INTO {table}"
            "(\"" + self._id_column(table) + "\", case_id, payload, created_at)"
            " VALUES (?, ?, ?, ?)",
            (record_id, case_id, payload, created_at),
        )
        self.db.connection.commit()

    def _rows(self, table: str, case_id: str) -> list[sqlite3.Row]:
        return self.db.connection.execute(
            f"SELECT payload FROM {table} WHERE case_id = ? ORDER BY created_at", (case_id,)
        ).fetchall()

    @staticmethod
    def _id_column(table: str) -> str:
        return {
            "assessments": "assessment_id",
            "decisions": "decision_id",
            "audit_events": "event_id",
        }[table]
