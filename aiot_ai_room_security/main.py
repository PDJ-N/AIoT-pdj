"""PIR 센서와 OpenCV AI를 활용한 방 침입 감지 시스템의 진입점."""

import time

import buzzer
import config
import sensor
import telegram_notifier
import vision_ai
from logger import write_event


ALERT_MESSAGE = "방에 사람이 감지되었습니다."


def _cooldown_active(last_alert_time):
    """마지막 알림 후 cooldown 시간이 지나지 않았는지 확인한다."""
    if last_alert_time is None:
        return False

    elapsed = time.monotonic() - last_alert_time
    if elapsed < config.ALERT_COOLDOWN_SECONDS:
        remaining = config.ALERT_COOLDOWN_SECONDS - elapsed
        print(f"[cooldown] {remaining:.1f}초 동안 중복 알림을 막습니다.")
        return True
    return False


def _handle_motion(last_alert_time):
    """PIR 움직임 감지 후 AI 확인과 침입 이벤트 처리를 수행한다."""
    print("[PIR] 움직임 감지. USB 웹캠 프레임을 가져와 AI로 확인합니다.")

    # 1단계: 움직임이 감지된 순간의 카메라 프레임을 AI 모델로 분석한다.
    # detect_person()은 (사람 감지 여부, confidence, 분석된 프레임)을 반환한다.
    person_detected, confidence, frame = vision_ai.detect_person()

    # 카메라 화면 표시 옵션이 켜져 있으면 현재 프레임을 OpenCV 창에 보여준다.
    # 옵션이 꺼져 있거나 SSH 환경이면 아무 동작 없이 지나간다.
    vision_ai.show_frame(frame)
    if not person_detected:
        print("[AI] 기준 confidence 이상의 person 객체가 없습니다.")
        return last_alert_time

    # 2단계: 사람이 계속 화면에 있을 때 텔레그램 알림이 반복 발송되지 않도록 막는다.
    if _cooldown_active(last_alert_time):
        return last_alert_time

    print(f"[침입 감지] {ALERT_MESSAGE} confidence={confidence:.2f}")

    # 3단계: 감지 당시 프레임을 파일로 저장한다.
    # 저장된 사진 경로는 텔레그램 사진 전송과 CSV 로그 기록에 함께 사용된다.
    image_path = vision_ai.save_frame(frame)

    # 4단계: 부저는 네트워크 오류와 무관하게 먼저 울리도록 한다.
    buzzer.beep(config.BUZZER_BEEP_SECONDS)

    # 5단계: 텔레그램 정보가 설정되어 있으면 메시지와 사진을 보낸다.
    # token/chat_id가 비어 있으면 notifier 내부에서 전송만 건너뛴다.
    telegram_notifier.send_message(ALERT_MESSAGE)
    telegram_notifier.send_photo(image_path, caption=ALERT_MESSAGE)

    # 6단계: 결과보고서에 활용할 수 있도록 CSV 로그를 남긴다.
    write_event("INTRUSION", ALERT_MESSAGE, confidence, image_path)

    return time.monotonic()


def main():
    """무한 루프에서 PIR 센서를 확인하고, Ctrl+C 입력 시 안전하게 종료한다."""
    print("AI 침입 감지 시스템 대기 중...")
    print(
        f"MOCK_MODE={config.MOCK_MODE}, "
        f"confidence 기준={config.PERSON_CONFIDENCE_THRESHOLD:.2f}, "
        f"cooldown={config.ALERT_COOLDOWN_SECONDS:.1f}초, "
        f"카메라 화면 표시={config.SHOW_CAMERA_WINDOW}"
    )
    if config.SHOW_CAMERA_WINDOW:
        print("[화면 표시] OpenCV 카메라 창이 열립니다. 창을 닫으려면 q 키 또는 Ctrl+C를 누르세요.")

    last_alert_time = None
    loop_count = 0

    try:
        while True:
            loop_count += 1
            try:
                # 카메라 미리보기 옵션이 켜진 경우, PIR 감지 여부와 별개로 화면을 계속 갱신한다.
                # OpenCV 창에서 q 키를 누르면 True가 반환되어 while 루프가 종료된다.
                if vision_ai.update_camera_preview():
                    break

                # PIR 센서가 움직임을 감지한 경우에만 AI 분석을 실행한다.
                # 이렇게 하면 매 순간 AI를 돌리는 것보다 CPU 사용량을 줄일 수 있다.
                if sensor.read_motion():
                    last_alert_time = _handle_motion(last_alert_time)
            except Exception as exc:
                # 가능한 한 전체 프로그램이 강제 종료되지 않도록 루프 내부 오류를 잡는다.
                print(f"[루프 오류] 이번 반복에서 오류가 발생했습니다: {exc}")

            if config.MAX_LOOP_COUNT > 0 and loop_count >= config.MAX_LOOP_COUNT:
                print("[실행 종료] AIOT_MAX_LOOP_COUNT에 도달했습니다.")
                break

            time.sleep(config.PIR_POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n[사용자 종료] Ctrl+C가 입력되었습니다.")
    finally:
        vision_ai.close_camera()
        buzzer.all_off()
        print("[시스템 종료] 부저를 끄고 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
