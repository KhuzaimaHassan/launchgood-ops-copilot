from app.domain.enums import Priority
from app.domain.models import Campaign, Case
from app.repositories.sqlite import SQLiteDatabase, SQLiteRepository


def test_sqlite_repository_round_trips_case() -> None:
    database = SQLiteDatabase("sqlite:///:memory:")
    repository = SQLiteRepository(database)
    case = Case(
        campaign=Campaign(title="Synthetic", description="Synthetic description"),
        title="Case 1",
        intake_category="DOCUMENTATION_CONCERN",
        initial_priority=Priority.HIGH,
    )

    repository.save_case(case)

    loaded = repository.get_case(case.case_id)
    assert loaded is not None
    assert loaded.case_id == case.case_id
    assert repository.list_cases()[0].title == "Case 1"
    database.close()
