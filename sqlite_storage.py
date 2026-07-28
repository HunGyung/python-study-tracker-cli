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
