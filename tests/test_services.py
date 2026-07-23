from models import StudyRecord
from services import generate_id, calculate_total_minutes, subject_search, delete_record, add_record

def test_generate_id_returns_one_when_records_are_empty() -> None:
    # Arrange: 테스트에 필요한 데이터 준비
    records: list[StudyRecord] = []

    # Act: 테스트할 함수 실행
    result = generate_id(records)

    # Assert: 결과 확인
    assert result == 1

# generate_id가 최댓값에 1을 더하는지 확인
def test_generate_id_returns_next_id() -> None:
    records = [
        StudyRecord(
            id=1,
            subject="Python",
            content="함수",
            minutes=60,
            date="2026-07-19"
        ),
        StudyRecord(
            id=3,
            subject="SQL",
            content="JOIN",
            minutes=30,
            date="2026-07-19",
        ),
    ]

    result = generate_id(records)

    assert result == 4

# 빈 목록의 총 공부 시간은 0인지 확인
def test_calculate_total_minutes_if_records_are_empty() -> None:
    records: list[StudyRecord] = []

    result = calculate_total_minutes(records)

    assert result == 0

# 60분과 30분 기록의 합계는 90이다.
def test_calculate_total_minutes_60_and_30() -> None:
    records = [
        StudyRecord(
            id=1,
            subject="Python",
            content="함수",
            minutes=60,
            date="2026-07-19"
        ),
        StudyRecord(
            id=3,
            subject="SQL",
            content="JOIN",
            minutes=30,
            date="2026-07-19",
        ),
    ]

    result = calculate_total_minutes(records)

    assert result == 90

# Python 검색 시 Python 기록만 반환한다.
def test_subject_search(sample_records: list[StudyRecord]) -> None:
    result = subject_search(sample_records, "Python")

    assert [record.id for record in result] == [1, 3]
    assert all(record.subject == "Python" for record in result)

# 기록이 비어있을 때 과목 검샘을 하면 빈 목록을 반환한다.
def test_subject_search_if_records_are_empty() -> None:
    records: list[StudyRecord] = []

    result = subject_search(records, "Python")

    assert not result

# 없는 과목을 검색하면 빈 목록을 반환한다.
def test_subject_search_if_non_exist_subject(sample_records: list[StudyRecord]) -> None:
    result = subject_search(sample_records, "Algorithm")

    assert not result

# 존재하는 ID를 삭제하면 True를 반환하고 목록에서도 사라진다.
def test_delete_record(sample_records: list[StudyRecord]) -> None:
    result = delete_record(sample_records, 1)

    assert result is True
    assert all(record.id != 1 for record in sample_records)
    assert len(sample_records) == 4

# 존재하지 않는 ID를 삭제하면 False를 반환하며 목록은 변하지 않는다.
def test_delete_record_nonexist_id(sample_records: list[StudyRecord]) -> None:
    original_records = sample_records.copy()
    result = delete_record(original_records, 6)

    assert result is False
    assert sample_records == original_records

# 기록 추가 후 목록 길이가 1이 되고 각 필드가 정확하다.
def test_add_record() -> None:
    records: list[StudyRecord] = []

    subject="Python"
    content="함수"
    minutes=60
    date="2026-07-19"

    add_record(records, subject, content, minutes, date)

    assert len(records) == 1
    assert records[0].id == 1
    assert records[0].subject == subject
    assert records[0].content == content
    assert records[0].minutes == minutes
    assert records[0].date == date

# 기록을 연속 추가하면 ID가 1과 2로 생성된다.
def test_add_record_continuous() -> None:
    records: list[StudyRecord] = []

    subject1="Python"
    content1="함수"
    minutes1=60
    date1="2026-07-19"

    subject2="SQL"
    content2="JOIN"
    minutes2=30
    date2="2026-07-19"

    add_record(records, subject1, content1, minutes1, date1)
    add_record(records, subject2, content2, minutes2, date2)

    assert len(records) == 2
    assert [record.id for record in records] == [1, 2]