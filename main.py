import logging
import sqlite3
from pathlib import Path

from sqlite_storage import (
    calculate_total_minutes,
    delete_record,
    fetch_all_records,
    find_records_by_subject,
    initialize_database,
    insert_record,
    reset_records,
)
from ui import (
    del_target_id,
    input_record,
    input_subject,
    list_records,
    menu,
    reset_question,
    subject_not_found,
)

DB_FILE = Path(__file__).with_name("study_tracker.db")
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
        initialize_database(DB_FILE)

        while True:
            order = menu()

            # 종료
            if order == 0:
                break

            # 기록 추가
            elif order == 1:
                subject, content, minutes, date = input_record()
                insert_record(DB_FILE, subject, content, minutes, date)

            # 기록 조회
            elif order == 2:
                records = fetch_all_records(DB_FILE)

                if not records:
                    print("\n조회할 기록이 없습니다.\n")
                    continue

                list_records(records)

            # 총 공부 시간
            elif order == 3:
                print(
                    f"\n총 공부 시간은 {calculate_total_minutes(DB_FILE)}분 입니다.\n"
                )

            # 기록 삭제
            elif order == 4:
                records = fetch_all_records(DB_FILE)

                if not records:
                    print("\n삭제할 기록이 없습니다.\n")
                    continue

                target_id = del_target_id()
                if target_id is None:
                    continue

                if delete_record(DB_FILE, target_id):
                    print("\n삭제가 완료되었습니다.\n")
                else:
                    print("\n존재하지않는 ID입니다.\n")

            # 과목별 기록 검색
            elif order == 5:
                records = fetch_all_records(DB_FILE)

                if not records:
                    print("\n조회할 기록이 없습니다.\n")
                    continue

                found_record = find_records_by_subject(DB_FILE, input_subject())

                if not found_record:
                    subject_not_found()
                else:
                    list_records(found_record)

            # 기록 초기화
            else:
                records = fetch_all_records(DB_FILE)

                if not records:
                    print("\n초기화할 기록이 없습니다.\n")
                    continue

                if reset_question() == 1:
                    reset_records(DB_FILE)
                    print("\n모든 기록이 초기화되었습니다.\n")

                else:
                    print("\n기록 초기화를 취소했습니다.\n")

    except sqlite3.Error:
        logger.exception("데이터베이스 작업 중 오류가 발생했습니다. %s", DB_FILE)
        print("데이터베이스 작업 중 오류가 발생했습니다.\n프로그램을 종료합니다.")


if __name__ == "__main__":
    configure_logging()
    run()
