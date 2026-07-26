import logging
from pathlib import Path

import pytest

import main


def test_run_logs_error_and_exits_for_invalid_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    file_path = tmp_path / "records.json"
    file_path.write_text("잘못된 JSON", encoding="utf-8")

    monkeypatch.setattr(main, "DATA_FILE", file_path)

    with caplog.at_level(logging.ERROR):
        main.run()

    captured = capsys.readouterr()

    assert "프로그램을 종료합니다." in captured.out
    assert "기록 파일을 불러오지 못했습니다." in caplog.text


def test_run_skips_reset_question_when_records_are_empty(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    menu_choices = iter([6, 0])

    monkeypatch.setattr(main, "load_records", lambda _: [])
    monkeypatch.setattr(main, "menu", lambda: next(menu_choices))

    def fail_if_called() -> int:
        pytest.fail("기록이 없을 때 reset_question()이 호출되었습니다.")

    monkeypatch.setattr(main, "reset_question", fail_if_called)

    main.run()

    captured = capsys.readouterr()

    assert "초기화할 기록이 없습니다." in captured.out
