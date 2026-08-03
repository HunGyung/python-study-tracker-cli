import sqlite3
from pathlib import Path

from models import StudyRecord


def initialize_database(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS study_records(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                content TEXT NOT NULL,
                minutes INTEGER NOT NULL CHECK(minutes > 0),
                date TEXT NOT NULL
            )
            """
        )


def insert_record(
    db_path: Path,
    subject: str,
    content: str,
    minutes: int,
    date: str,
) -> StudyRecord:
    with sqlite3.connect(db_path) as connection:
        # SQL Injection을 방지하기위해 파라미터 바인딩 사용
        cursor = connection.execute(
            """
            INSERT INTO study_records (
                subject,
                content,
                minutes,
                date
            )
            VALUES (?, ?, ?, ?)
            """,
            (subject, content, minutes, date),
        )

        record_id = cursor.lastrowid

        if record_id is None:
            raise RuntimeError("SQLite에서 생성된 기록 ID를 가져오지 못했습니다.")

        return StudyRecord(
            id=record_id,
            subject=subject,
            content=content,
            minutes=minutes,
            date=date,
        )


def fetch_all_records(db_path: Path) -> list[StudyRecord]:
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, subject, content, minutes, date
            FROM study_records
            ORDER BY id;
            """
        ).fetchall()

    return [
        StudyRecord(
            id=row[0],
            subject=row[1],
            content=row[2],
            minutes=row[3],
            date=row[4],
        )
        for row in rows
    ]


def find_records_by_subject(db_path: Path, target: str) -> list[StudyRecord]:
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, subject, content, minutes, date
            FROM study_records
            WHERE subject = ?
            ORDER BY id;
            """,
            (target,),
        ).fetchall()

    return [
        StudyRecord(
            id=row[0],
            subject=row[1],
            content=row[2],
            minutes=row[3],
            date=row[4],
        )
        for row in rows
    ]


def delete_record(db_path: Path, target_id: int) -> bool:
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(
            """
                DELETE FROM study_records
                WHERE id = ?
                """,
            (target_id,),
        )

    return cursor.rowcount > 0


def calculate_total_minutes(db_path: Path) -> int:
    with sqlite3.connect(db_path) as connection:
        # SUM은 행이 없으면 NULL을 반환하므로 NULL일 경우 0으로 대체 (~= ifnull())
        total = connection.execute(
            """
            SELECT COALESCE(SUM(minutes), 0)
            FROM study_records
            """
        ).fetchone()

    return int(total[0])


def reset_records(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            DELETE FROM study_records
            """
        )
