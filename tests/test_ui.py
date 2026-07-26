import pytest

from models import StudyRecord
from ui import (
    del_target_id,
    input_record,
    input_subject,
    menu,
    print_record,
    reset_question,
)


def test_menu_returns_selected_number(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "2")

    result = menu()

    assert result == 2


def test_menu_retries_until_valid_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = iter(["abc", "7", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = menu()

    assert result == 3


def test_menu_prints_errors_for_invalid_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inputs = iter(["abc", "7", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = menu()
    captured = capsys.readouterr()

    assert result == 3
    assert "메뉴는 숫자만 입력해주세요." in captured.out
    assert "메뉴는 0-6 중에 골라주세요." in captured.out


def test_input_subject(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "Python")

    result = input_subject()

    assert result == "Python"


def test_del_target_id_correct(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "3")

    result = del_target_id()

    assert result == 3


def test_del_target_id_incorrect(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "abc")

    result = del_target_id()
    captured = capsys.readouterr()

    assert result is None
    assert "ID는 숫자만 입력해주세요." in captured.out


def test_print_record(
    sample_records: list[StudyRecord], capsys: pytest.CaptureFixture[str]
) -> None:
    print_record(sample_records[0])
    captured = capsys.readouterr()

    assert "ID : 1" in captured.out
    assert "과목 : Python" in captured.out
    assert "공부 내용 : 함수" in captured.out
    assert "공부 시간 : 60분" in captured.out
    assert "날짜 : 2026-07-19" in captured.out
    assert "-" * 20 in captured.out


def test_input_record(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inputs = iter(["Python", "함수", "abc", "0", "60", "2026/07/21", "2026-07-21"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result_subject, result_content, result_minutes, result_date = input_record()
    captured = capsys.readouterr()

    assert result_subject == "Python"
    assert result_content == "함수"
    assert result_minutes == 60
    assert result_date == "2026-07-21"
    assert "공부 시간은 숫자만 입력해주세요. (분 단위)" in captured.out
    assert "공부 시간은 1분 이상이어야 합니다." in captured.out
    assert (
        "날짜는 YYYY-MM-DD 형식으로 입력해주세요. (예시 : 2026-07-17)" in captured.out
    )


def test_reset_question(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    inputs = iter(["abc", "3", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = reset_question()
    captured = capsys.readouterr()

    assert result == 1
    assert "숫자만 입력해주세요. (1/2)" in captured.out
    assert "예(1)/아니오(2) 중에 골라주세요." in captured.out
