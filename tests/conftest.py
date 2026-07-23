import pytest
from models import StudyRecord

@pytest.fixture
def sample_records() -> list[StudyRecord]:
    return [
        StudyRecord(
            id=1,
            subject="Python",
            content="함수",
            minutes=60,
            date="2026-07-19"
        ),
        StudyRecord(
            id=2,
            subject="SQL",
            content="JOIN",
            minutes=30,
            date="2026-07-19",
        ),
        StudyRecord(
            id=3,
            subject="Python",
            content="Coding Test",
            minutes=60,
            date="2026-07-19"
        ),
        StudyRecord(
            id=4,
            subject="SQL",
            content="GROUPBY",
            minutes=50,
            date="2026-07-19",
        ),
        StudyRecord(
            id=5,
            subject="Math",
            content="Calculus",
            minutes=100,
            date="2026-07-19",
        ),
    ]