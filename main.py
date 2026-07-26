import logging
from pathlib import Path

from models import StudyRecord
from services import calculate_total_minutes, subject_search, delete_record, add_record
from ui import list_records, menu, input_subject, subject_not_found, del_target_id, input_record, reset_question
from storage import save_records, load_records, reset_records, StorageError

DATA_FILE = Path(__file__).with_name("records.json")
LOG_FILE = Path(__file__).with_name("app.log")

logger = logging.getLogger(__name__)

def configure_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        encoding="utf-8",
    )

def run() -> None:
    try:
        records = load_records(DATA_FILE)

    except StorageError:
        logger.exception(
            "기록 파일을 불러오지 못했습니다. %s",
            DATA_FILE,
        )
        print(
            "기록 파일을 불러오는 중 오류가 발생했습니다.\n" \
            "프로그램을 종료합니다.")
        return

    while True:
        order = menu()

        # 종료
        if order == 0:
            break
        
        # 기록 추가
        elif order == 1:
            subject, content, minutes, date = input_record()
            add_record(records, subject, content, minutes, date)
            save_records(records, DATA_FILE)
        
        # 기록 조회
        elif order == 2:
            if not records:
                print("\n조회할 기록이 없습니다.\n")
                continue

            list_records(records)
        
        # 총 공부 시간
        elif order == 3:
            print(f"\n총 공부 시간은 {calculate_total_minutes(records)}분 입니다.\n")
        
        # 기록 삭제
        elif order == 4:
            if not records:
                print("\n삭제할 기록이 없습니다.\n")
                continue

            target_id = del_target_id()
            if target_id is None:
                continue

            if delete_record(records, target_id):
                save_records(records, DATA_FILE)
                print("\n삭제가 완료되었습니다.\n")
            else:
                print("\n존재하지않는 ID입니다.\n")
        
        # 과목별 기록 검색
        elif order == 5:
            if not records:
                print("\n조회할 기록이 없습니다.\n")
                continue

            found_record = subject_search(records, input_subject())

            if not found_record:
                subject_not_found()
            else:
                list_records(found_record)
        
        # 기록 초기화
        else:
            if not records:
                print("\n초기화할 기록이 없습니다.\n")
            
            if reset_question() == 1:
                records.clear()
                reset_records(DATA_FILE)
                print("\n모든 기록이 초기화되었습니다.\n")
            
            else:
                print("\n기록 초기화를 취소했습니다.\n")

if __name__ == "__main__":
    configure_logging()
    run()