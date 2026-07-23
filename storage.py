import json
from pathlib import Path
from dataclasses import asdict

from models import StudyRecord

# 기록 저장
def save_records(records: list[StudyRecord], file_path: Path) -> None:
    # 저장을 위해 records를 json 형태로 변환
    data = [asdict(record) for record in records]

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# 기록 불러오기
def load_records(file_path: Path) -> list[StudyRecord]:
    # 기록이 없다면 빈 목록 반환(프로그램 시작시 기록이 없어 종료되는 것을 방지)
    if not file_path.exists():
        return []
    
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # json 형태로 불러온 것을 다시 StudyRecord 형태로 반환
    return [StudyRecord(**item) for item in data]

def reset_records(file_path: Path) -> None:
    save_records([], file_path)