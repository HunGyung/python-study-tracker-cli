import sqlite3
from pathlib import Path

from models import StudyRecord
from sqlite_storage import (
    calculate_total_minutes,
    delete_record,
    fetch_all_records,
    find_records_by_subject,
    initialize_database,
    insert_record,
    reset_records,
)


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


def test_fetch_all_records_return_saved_records(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    first_record = insert_record(
        db_path,
        subject="Python",
        content="SQLite 학습",
        minutes=30,
        date="2026-07-29",
    )
    second_record = insert_record(
        db_path,
        subject="SQL",
        content="SELECT 학습",
        minutes=20,
        date="2026-07-29",
    )

    records = fetch_all_records(db_path)

    assert records == [first_record, second_record]


def test_find_records_by_subject(populated_db: tuple[Path, list[StudyRecord]]) -> None:
    db_path, records = populated_db

    result = find_records_by_subject(db_path, "Python")

    assert result == [records[0], records[2]]


def test_find_records_by_subject_returns_empty_list_when_not_found(
    populated_db: tuple[Path, list[StudyRecord]],
) -> None:
    db_path, _ = populated_db

    result = find_records_by_subject(db_path, "없는 과목")

    assert result == []


# 존재하는 ID를 삭제하면 True를 반환하고 목록에서도 사라진다.
def test_delete_record(populated_db: tuple[Path, list[StudyRecord]]) -> None:
    db_path, records = populated_db

    result = delete_record(db_path, records[0].id)

    assert result is True
    assert fetch_all_records(db_path) == records[1:]


# 존재하지 않는 ID를 삭제하면 False를 반환하며 목록은 변하지 않는다.
def test_delete_record_nonexist_id(
    populated_db: tuple[Path, list[StudyRecord]],
) -> None:
    db_path, records = populated_db

    result = delete_record(db_path, 5)

    assert result is False
    assert fetch_all_records(db_path) == records


def test_calculate_total_minutes(populated_db: tuple[Path, list[StudyRecord]]) -> None:
    db_path, records = populated_db

    assert calculate_total_minutes(db_path) == sum(record.minutes for record in records)


def test_calculate_total_minutes_returns_zero_when_database_is_empty(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    assert calculate_total_minutes(db_path) == 0


def test_reset_records(populated_db: tuple[Path, list[StudyRecord]]) -> None:
    db_path, _ = populated_db

    reset_records(db_path)

    assert fetch_all_records(db_path) == []
