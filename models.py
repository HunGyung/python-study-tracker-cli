from dataclasses import dataclass


@dataclass
class StudyRecord:
    id: int  # ID (자동으로 생성)
    subject: str  # 과목명
    content: str  # 공부 내용
    minutes: int  # 공부 시간(분 단위)
    date: str  # 날짜
