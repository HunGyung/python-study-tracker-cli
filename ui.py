from models import StudyRecord
from datetime import datetime

# 시작화면(메뉴화면)
def menu() -> int:
    while True:
        try:
            order = int(input("=== 학습 기록 관리 ===\n1. 기록 추가\n2. 기록 조회\n3. 총 공부 시간\n4. 기록 삭제\n5. 과목별 기록 검색\n6. 기록 초기화\n0. 종료\n선택:"""))
            if order < 0 or order > 6:
                print("\n메뉴는 0-6 중에 골라주세요.\n")
                continue
            break
            
        except ValueError:
            print("\n메뉴는 숫자만 입력해주세요. (0-6)\n")
    return order

# record 출력 형식
def print_record(record: StudyRecord) -> None:
    print(f"\nID : {record.id}")
    print(f"과목 : {record.subject}")
    print(f"공부 내용 : {record.content}")
    print(f"공부 시간 : {record.minutes}분")
    print(f"날짜 : {record.date}")
    print("-"*20, "\n")

# 모든 record 출력
def list_records(records: list[StudyRecord]) -> None:
    for record in records:
        print_record(record)

# 과목별 검색에 사용
def input_subject() -> str:
    return input("\n검색할 과목 : ")

# 과목별 검색에 사용
def subject_not_found() -> None:
    print("\n존재하지않는 과목명입니다.\n")

# 삭제할 기록 ID 입력
def del_target_id() -> int | None:
    try:
        return int(input("삭제할 기록 ID : ")) 
    except ValueError:
        print("\nID는 숫자만 입력해주세요.\n")
        return None

# 기록 추가를 위해 내용 입력
def input_record() -> tuple[str, str, int, str]:
    subject = input("과목 : ")
    content = input("공부 내용 : ")
    while True:
        try:
            minutes = int(input("공부 시간 : "))

            if minutes <= 0:
                print("\n공부 시간은 1분 이상이어야 합니다.\n")
                continue
            break

        except ValueError:
            print("\n공부 시간은 숫자만 입력해주세요. (분 단위)\n")

    while True:
        try:
            date =input("날짜 : ")
            datetime.strptime(date, "%Y-%m-%d")
            break
        
        except ValueError:
            print("날짜는 YYYY-MM-DD 형식으로 입력해주세요. (예시 : 2026-07-17)")
    
    return subject, content, minutes, date

def reset_question() -> int:
    while True:
        try:
            order = int(input(
                "정말로 기록을 초기화하시겠습니까?\n1. 예\n2. 아니오\n: "))
            if order < 1 or order > 2:
                print("\n예(1)/아니오(2) 중에 골라주세요.\n")
                continue
            return order
        except ValueError:
            print("\n숫자만 입력해주세요. (1/2)\n")