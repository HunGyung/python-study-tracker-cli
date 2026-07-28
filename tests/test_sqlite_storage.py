import sqlite3
from pathlib import Path

from models import StudyRecord
from sqlite_storage import initialize_database, insert_record


def test_initialize_database_creates_study_records_table(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "study_tracker.db"

    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
                AND name = 'study_records'
            """
        ).fetchone()

    assert result == ("study_records",)


def test_insert_record_saves_and_returns_record(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "study_tracker.db"
    initialize_database(db_path)

    result = insert_record(
        db_path=db_path,
        subject="Python",
        content="SQLite INSERT",
        minutes=60,
        date="2026-07-27",
    )

    assert result == StudyRecord(
        id=1, subject="Python", content="SQLite INSERT", minutes=60, date="2026-07-27"
    )

    with sqlite3.connect(db_path) as connection:
        saved_row = connection.execute(
            """
            SELECT id, subject, content, minutes, date
            FROM study_records
            WHERE id = 1
            """
        ).fetchone()

    assert saved_row == (
        1,
        "Python",
        "SQLite INSERT",
        60,
        "2026-07-27",
    )
