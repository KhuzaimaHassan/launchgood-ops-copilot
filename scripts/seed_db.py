"""Seed database reset procedure for LaunchGood Ops Copilot demo walkthrough."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import AppConfig
from app.domain.models import Case
from app.repositories.sqlite import SQLiteDatabase, SQLiteRepository


def seed_database() -> None:
    db_path = PROJECT_ROOT / "data" / "app.db"
    config = AppConfig(database_url=f"sqlite:///{db_path}")
    db = SQLiteDatabase(config.database_url)
    repo = SQLiteRepository(db)

    # Clear existing data safely
    conn = db.connection
    conn.execute("DELETE FROM audit_events")
    conn.execute("DELETE FROM decisions")
    conn.execute("DELETE FROM assessments")
    conn.execute("DELETE FROM cases")
    conn.commit()
    print(f"Cleared existing database tables at {db_path}")

    fixture_dir = PROJECT_ROOT / "data" / "fixtures" / "cases"
    fixture_files = sorted(fixture_dir.glob("*.json"))

    print(f"Seeding {len(fixture_files)} cases from {fixture_dir}...")
    for path in fixture_files:
        case_data = Case.model_validate_json(path.read_text(encoding="utf-8"))
        repo.save_case(case_data)
        print(f"  [OK] Seeded {case_data.case_id}: {case_data.title} ({case_data.status.value})")

    print("\nDatabase reset and seed complete!")


if __name__ == "__main__":
    seed_database()
