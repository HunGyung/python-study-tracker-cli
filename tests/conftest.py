from pathlib import Path

import pytest

from models import StudyRecord
from sqlite_storage import initialize_database, insert_record


@pytest.fixture
def sample_records() -> list[StudyRecord]:
    return [
        StudyRecord(
            id=1, subject="Python", content="함수", minutes=60, date="2026-07-19"
        ),
        StudyRecord(
            id=2,
            subject="SQL",
            content="JOIN",
            minutes=30,
            date="2026-07-19",
        ),
        StudyRecord(
            id=3, subject="Python", content="Coding Test", minutes=60, date="2026-07-19"
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


@pytest.fixture
def populated_db(tmp_path: Path) -> tuple[Path, list[StudyRecord]]:
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    records = [
        insert_record(
            db_path,
            subject="Python",
            content="SQLite 학습",
            minutes=30,
            date="2026-07-29",
        ),
        insert_record(
            db_path,
            subject="SQL",
            content="SELECT 학습",
            minutes=20,
            date="2026-07-29",
        ),
        insert_record(
            db_path,
            subject="Python",
            content="코테 연습",
            minutes=60,
            date="2026-07-29",
        ),
        insert_record(
            db_path,
            subject="SQL",
            content="GROUP BY 학습",
            minutes=30,
            date="2026-07-29",
        ),
    ]

    return db_path, records
