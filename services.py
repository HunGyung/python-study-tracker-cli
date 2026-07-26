from models import StudyRecord


# ID 자동 생성 함수
# 첫 생성 -> 1
# 그 뒤부터는 2, 3, 4, ...
def generate_id(records: list[StudyRecord]) -> int:
    if not records:
        return 1

    return max(record.id for record in records) + 1


# 총 공부 시간 계산, 모든 기록의 공부시간을 합산
def calculate_total_minutes(records: list[StudyRecord]) -> int:
    return sum(record.minutes for record in records)


# 과목별 조회를 위한 검색함수
def subject_search(records: list[StudyRecord], subject: str) -> list[StudyRecord]:
    return [record for record in records if record.subject == subject]


# 타겟 기록을 찾아 삭제, 성공하면 True 반환, 실패하면 False 반환
def delete_record(records: list[StudyRecord], target_id: int) -> bool:
    for record in records:
        if record.id == target_id:
            records.remove(record)
            return True

    return False


# 기록 추가
def add_record(
    records: list[StudyRecord], subject: str, content: str, minutes: int, date: str
) -> None:
    record = StudyRecord(
        id=generate_id(records),
        subject=subject,
        content=content,
        minutes=minutes,
        date=date,
    )
    records.append(record)
