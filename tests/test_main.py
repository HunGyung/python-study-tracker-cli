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
