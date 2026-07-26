import json
from pathlib import Path

import pytest

from models import StudyRecord
from storage import StorageError, load_records, reset_records, save_records


def test_load_records_returns_empty_list_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "records.json"

    result = load_records(file_path)

    assert result == []


def test_save_and_load_records(
    tmp_path: Path, sample_records: list[StudyRecord]
) -> None:
    file_path = tmp_path / "records.json"

    save_records(sample_records, file_path)
    result = load_records(file_path)

    assert result == sample_records


def test_save_and_load_empty_records(tmp_path: Path) -> None:
    file_path = tmp_path / "records.json"

    save_records([], file_path)
    result = load_records(file_path)

    assert result == []


def test_save_records_writes_valid_json(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "records.json"
    records = [
        StudyRecord(
            id=1,
            subject="Python",
            content="한글 테스트",
            minutes=60,
            date="2026-07-22",
        )
    ]

    save_records(records, file_path)
    with file_path.open("r", encoding="utf-8") as file:
        result = json.load(file)

    assert result == [
        {
            "id": 1,
            "subject": "Python",
            "content": "한글 테스트",
            "minutes": 60,
            "date": "2026-07-22",
        }
    ]


def test_save_records_preserves_readable_korean(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "records.json"
    records = [
        StudyRecord(
            id=1,
            subject="파이썬",
            content="파일 저장",
            minutes=60,
            date="2026-07-22",
        )
    ]

    save_records(records, file_path)

    result = file_path.read_text(encoding="utf-8")

    assert "파이썬" in result
    assert "파일 저장" in result


def test_reset_records(tmp_path: Path, sample_records) -> None:
    file_path = tmp_path / "records.json"

    save_records(sample_records, file_path)
    reset_records(file_path)

    data = load_records(file_path)

    assert data == []


def test_load_records_raises_storage_error_for_invalid_json(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "records.json"
    file_path.write_text("잘못된 JSON", encoding="utf-8")

    with pytest.raises(StorageError):
        load_records(file_path)
