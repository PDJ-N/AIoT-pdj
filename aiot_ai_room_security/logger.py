"""침입 이벤트를 CSV 로그로 저장한다."""

import csv
from datetime import datetime

import config


CSV_HEADER = ["timestamp", "event_type", "message", "confidence", "image_path"]


def write_event(event_type, message, confidence, image_path):
    """logs/event_log.csv에 이벤트 한 줄을 추가한다."""
    log_path = config.LOG_FILE_PATH

    # logs 폴더가 없으면 자동으로 만든다.
    # 라즈베리파이에서 처음 실행해도 별도 폴더 생성 작업이 필요 없다.
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # 파일이 처음 만들어졌거나 비어 있으면 CSV 헤더를 먼저 기록한다.
    needs_header = not log_path.exists() or log_path.stat().st_size == 0
    with log_path.open("a", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        if needs_header:
            writer.writerow(CSV_HEADER)

        # confidence는 보고서에서 보기 좋도록 소수점 4자리 문자열로 저장한다.
        timestamp = datetime.now().isoformat(timespec="seconds")
        writer.writerow([
            timestamp,
            event_type,
            message,
            f"{confidence:.4f}",
            image_path,
        ])

    print(f"[로그 저장] {log_path}")
