"""OpenCV DNN MobileNet SSD로 USB 웹캠 프레임에서 사람을 탐지한다."""

from datetime import datetime

import config


_cv2 = None
_model = None
_camera = None
_opencv_error_reported = False
_model_error_reported = False
_camera_error_reported = False
_window_error_reported = False
_camera_window_enabled = True


def _get_cv2():
    """OpenCV가 필요할 때만 import하여 mock 테스트를 쉽게 만든다."""
    global _cv2, _opencv_error_reported
    if _cv2 is not None:
        return _cv2

    try:
        import cv2
    except ImportError:
        if not _opencv_error_reported:
            print("[OpenCV 오류] cv2가 없습니다. 'pip install opencv-python'을 실행하세요.")
            _opencv_error_reported = True
        return None

    _cv2 = cv2
    return _cv2


def _get_model():
    """MobileNet SSD 모델을 한 번만 불러와 재사용한다."""
    global _model, _model_error_reported
    if _model is not None:
        # 모델 파일은 용량이 크므로 매번 다시 읽지 않고, 처음 읽은 객체를 재사용한다.
        return _model

    cv2 = _get_cv2()
    if cv2 is None:
        return None

    missing_paths = [
        path
        for path in (config.MODEL_WEIGHTS_PATH, config.MODEL_CONFIG_PATH)
        if not path.is_file()
    ]
    if missing_paths:
        if not _model_error_reported:
            print("[AI 모델 오류] MobileNet SSD 모델 파일이 없습니다.")
            for path in missing_paths:
                print(f"  - 필요한 파일: {path}")
            print("  python3 download_models.py를 실행하거나 수업 때 받은 모델 파일을 models 폴더에 넣으세요.")
            _model_error_reported = True
        return None

    try:
        # TensorFlow 형식의 MobileNet SSD 모델을 OpenCV DNN 모듈로 불러온다.
        # weights(.pb)와 config(.pbtxt) 두 파일이 모두 필요하다.
        _model = cv2.dnn.readNetFromTensorflow(
            str(config.MODEL_WEIGHTS_PATH),
            str(config.MODEL_CONFIG_PATH),
        )
    except cv2.error as exc:
        if not _model_error_reported:
            print(f"[AI 모델 오류] 모델을 읽지 못했습니다: {exc}")
            _model_error_reported = True
        return None

    return _model


def _get_camera():
    """USB 웹캠을 열고, 이미 열려 있으면 기존 객체를 사용한다."""
    global _camera, _camera_error_reported
    if _camera is not None and _camera.isOpened():
        # 이미 열린 카메라 객체가 있으면 재사용한다.
        return _camera

    cv2 = _get_cv2()
    if cv2 is None:
        return None

    # CAMERA_INDEX는 보통 0이다. 웹캠이 여러 개면 1, 2 등으로 바꿀 수 있다.
    camera = cv2.VideoCapture(config.CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

    if not camera.isOpened():
        camera.release()
        if not _camera_error_reported:
            print(
                "[웹캠 오류] USB 웹캠을 열 수 없습니다. "
                "연결 상태와 AIOT_CAMERA_INDEX 값을 확인하세요."
            )
            _camera_error_reported = True
        return None

    _camera = camera
    return _camera


def _draw_person_box(frame, detection, confidence):
    """사람 위치에 박스와 confidence 텍스트를 표시한다."""
    cv2 = _get_cv2()
    image_height, image_width, _ = frame.shape

    # 모델 출력 좌표는 0~1 사이 비율값이므로 실제 이미지 픽셀 좌표로 변환한다.
    left = max(0, int(detection[3] * image_width))
    top = max(0, int(detection[4] * image_height))
    right = min(image_width - 1, int(detection[5] * image_width))
    bottom = min(image_height - 1, int(detection[6] * image_height))

    cv2.rectangle(frame, (left, top), (right, bottom), (23, 230, 210), 2)
    cv2.putText(
        frame,
        f"person {confidence:.2f}",
        (left, max(20, top - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 255),
        2,
    )


def read_camera_frame():
    """웹캠에서 현재 프레임 하나를 읽어 반환한다. 실패하면 None을 반환한다."""
    global _camera
    if config.MOCK_MODE:
        # mock 모드에서는 실제 카메라를 사용하지 않는다.
        return None

    camera = _get_camera()
    if camera is None:
        return None

    try:
        success, frame = camera.read()
    except Exception as exc:
        print(f"[웹캠 오류] 프레임 읽기 중 오류가 발생했습니다: {exc}")
        return None

    if not success or frame is None:
        print("[웹캠 오류] 프레임을 읽지 못했습니다. 다음 반복에서 다시 시도합니다.")
        camera.release()
        _camera = None
        return None

    return frame


def show_frame(frame, wait_ms=1):
    """OpenCV 창에 프레임을 표시한다. q 키를 누르면 True를 반환한다."""
    global _window_error_reported, _camera_window_enabled

    if frame is None or not config.SHOW_CAMERA_WINDOW or not _camera_window_enabled:
        return False

    cv2 = _get_cv2()
    if cv2 is None:
        return False

    try:
        # imshow는 라즈베리파이 Desktop 같은 그래픽 환경에서만 정상적으로 창을 띄운다.
        cv2.imshow(config.CAMERA_WINDOW_NAME, frame)
        key = cv2.waitKey(wait_ms) & 0xFF
    except cv2.error as exc:
        _camera_window_enabled = False
        if not _window_error_reported:
            print(f"[화면 표시 오류] OpenCV 창을 열 수 없습니다: {exc}")
            print("  라즈베리파이 Desktop 환경에서 실행하거나 AIOT_SHOW_CAMERA_WINDOW=0으로 끄세요.")
            _window_error_reported = True
        return False

    if key == ord("q"):
        print("[화면 표시] q 키가 입력되어 프로그램을 종료합니다.")
        return True
    return False


def update_camera_preview():
    """실행 중 카메라 화면을 계속 보여준다. q 키를 누르면 True를 반환한다."""
    if not config.SHOW_CAMERA_WINDOW or config.MOCK_MODE:
        return False

    # PIR 감지가 없더라도 화면 미리보기는 계속 갱신한다.
    frame = read_camera_frame()
    return show_frame(frame)


def detect_person():
    """사람 탐지 여부, confidence, 프레임을 반환한다."""
    if config.MOCK_MODE:
        if config.MOCK_PERSON_DETECTED:
            confidence = config.MOCK_PERSON_CONFIDENCE
            print(f"[MOCK AI] person 탐지, confidence={confidence:.2f}")
            return True, confidence, None
        print("[MOCK AI] person이 탐지되지 않았습니다.")
        return False, 0.0, None

    # 실제 모드에서는 모델과 카메라가 모두 준비되어 있어야 AI 분석이 가능하다.
    model = _get_model()
    camera = _get_camera()
    if model is None or camera is None:
        return False, 0.0, None

    frame = read_camera_frame()
    if frame is None:
        return False, 0.0, None

    cv2 = _get_cv2()
    try:
        # MobileNet SSD는 300x300 크기의 blob 입력을 사용한다.
        # swapRB=True는 OpenCV의 BGR 이미지를 모델 입력에 맞게 RGB 순서로 바꾸는 옵션이다.
        blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True)
        model.setInput(blob)
        output = model.forward()
    except cv2.error as exc:
        print(f"[AI 탐지 오류] 프레임 분석 중 오류가 발생했습니다: {exc}")
        return False, 0.0, frame

    best_confidence = 0.0
    for detection in output[0, 0, :, :]:
        class_id = int(detection[1])
        confidence = float(detection[2])

        # COCO 데이터셋 기준 class_id 1은 person이다.
        # confidence가 기준값 이상일 때만 사람으로 인정한다.
        if (
            class_id == config.PERSON_CLASS_ID
            and confidence >= config.PERSON_CONFIDENCE_THRESHOLD
        ):
            best_confidence = max(best_confidence, confidence)
            _draw_person_box(frame, detection, confidence)

    if best_confidence > 0:
        return True, best_confidence, frame
    return False, 0.0, frame


def save_frame(frame):
    """현재 프레임을 captures 폴더에 저장하고 파일 경로를 반환한다."""
    if frame is None:
        if config.MOCK_MODE:
            print("[MOCK 저장] 실제 프레임이 없어서 이미지 저장을 건너뜁니다.")
        return ""

    cv2 = _get_cv2()
    if cv2 is None:
        return ""

    try:
        config.CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"[이미지 저장 오류] captures 폴더를 만들 수 없습니다: {exc}")
        return ""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    image_path = config.CAPTURE_DIR / f"intrusion_{timestamp}.jpg"

    try:
        if cv2.imwrite(str(image_path), frame):
            print(f"[이미지 저장] {image_path}")
            return str(image_path)
    except cv2.error as exc:
        print(f"[이미지 저장 오류] 저장 실패: {exc}")
        return ""

    print(f"[이미지 저장 오류] 저장 실패: {image_path}")
    return ""


def close_camera():
    """프로그램 종료 시 카메라 자원을 정리한다."""
    global _camera, _camera_window_enabled
    if _camera is not None:
        _camera.release()
        _camera = None
    if _cv2 is not None:
        try:
            _cv2.destroyAllWindows()
        except _cv2.error:
            pass
    _camera_window_enabled = True
