import logging
import sqlite3
from pathlib import Path

import pytest

import main


def test_run_logs_error_and_exits_when_database_initialization_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def raise_database_error(_: Path) -> None:
        raise sqlite3.OperationalError("데이터베이스를 열 수 없습니다.")

    monkeypatch.setattr(
        main,
        "initialize_database",
        raise_database_error,
    )

    with caplog.at_level(logging.ERROR):
        main.run()

    captured = capsys.readouterr()

    assert "프로그램을 종료합니다." in captured.out
    assert "데이터베이스 작업 중 오류가 발생했습니다." in caplog.text


def test_run_skips_reset_question_when_records_are_empty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    db_path = tmp_path / "test.db"
    menu_choices = iter([6, 0])

    monkeypatch.setattr(main, "DB_FILE", db_path)
    monkeypatch.setattr(main, "menu", lambda: next(menu_choices))

    def fail_if_called() -> int:
        pytest.fail("기록이 없을 때 reset_question()이 호출되었습니다.")

    monkeypatch.setattr(main, "reset_question", fail_if_called)

    main.run()

    captured = capsys.readouterr()

    assert "초기화할 기록이 없습니다." in captured.out
