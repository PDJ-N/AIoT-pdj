# 한신대학교 AIoT 설계입문

라즈베리파이와 Python을 활용하여 진행한 AIoT 설계입문 실험 내용을 정리한 저장소입니다.  
각 실험은 프로젝트 폴더 기준으로 누적되며, 실험 개요, 목적, 사용 부품, 사용 기술, 주요 코드, 학습 내용, 실행 결과를 함께 기록합니다.

---

## 목차
- [project2 - 라즈베리파이로 신호등 만들기](#project2---라즈베리파이로-신호등-만들기)
- [project6 - MQ-2 가스 감지 모듈과 능동부저를 이용한 가스 경보 시스템](#project6---mq-2-가스-감지-모듈과-능동부저를-이용한-가스-경보-시스템)
- [project14 - PIR 모션 센서와 카메라를 이용한 움직임 감지 촬영 시스템](#project14---pir-모션-센서와-카메라를-이용한-움직임-감지-촬영-시스템)
- [project20 - 플라스크 웹서버를 이용한 LED 제어](#project20---플라스크-웹서버를-이용한-led-제어)

---

## project2 - 라즈베리파이로 신호등 만들기

### 실험 개요
라즈베리파이 GPIO 핀과 LED를 이용하여 차량용 및 보행자용 신호등 시스템을 구현하였다.  
Python의 `gpiozero` 라이브러리를 활용하여 LED의 점등 순서를 제어하였다.  
해당 내용은 `project_2` 폴더 기준으로 정리하였다.

### 실험 목적
- GPIO 핀 제어 방법을 이해한다.
- LED를 활용한 신호등 시스템을 구현한다.
- Python을 이용한 하드웨어 제어 방법을 학습한다.

### 사용 부품
- Raspberry Pi
- LED 5개
- 저항
- 브레드보드
- 점퍼 케이블

### 사용 기술
- Python
- `gpiozero`
- GPIO 제어

### 주요 코드
```python
from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(2, 3, 4, 20, 21)

try:
    while 1:
        leds.value = (0, 0, 1, 1, 0)
        sleep(3.0)
        leds.value = (0, 1, 0, 1, 0)
        sleep(1.0)
        leds.value = (1, 0, 0, 0, 1)
        sleep(3.0)

except KeyboardInterrupt:
    pass

leds.off()
```

### 학습 내용
라즈베리파이의 GPIO 핀을 이용하면 외부 LED와 같은 출력 장치를 제어할 수 있으며, `gpiozero` 라이브러리를 사용하면 여러 개의 LED도 비교적 간단하게 다룰 수 있다.  
이번 실험에서는 차량용 신호와 보행자용 신호를 함께 구성하면서 점등 순서를 코드로 제어하는 방법을 학습하였다.

### 실행 결과
차량용 LED와 보행자용 LED가 설정된 순서에 따라 반복적으로 점등되도록 구현하였다.  
이를 통해 신호등의 기본 동작을 라즈베리파이 기반으로 구현할 수 있음을 확인하였다.

---

## project6 - MQ-2 가스 감지 모듈과 능동부저를 이용한 가스 경보 시스템

### 실험 개요
MQ-2(FC-22) 가스 감지 모듈의 디지털 출력값을 읽어 가스 감지 여부를 판단하고, 감지 시 능동부저가 동작하도록 구현하였다.  
Python의 `gpiozero` 라이브러리를 사용하여 센서 입력과 출력 장치 제어를 수행하였으며, 반복문을 통해 센서 상태를 지속적으로 확인하도록 구성하였다.  
해당 내용은 `project_6` 폴더 기준으로 정리하였다.

### 실험 목적
- MQ-2(FC-22) 가스 감지 모듈의 디지털 출력 동작을 이해한다.
- 라즈베리파이 GPIO를 이용하여 능동부저를 제어하는 방법을 학습한다.
- 센서 입력과 경보 출력을 연동한 기초적인 가스 감지 시스템을 구현한다.

### 사용 부품
- Raspberry Pi
- MQ-2(FC-22) 가스 감지 모듈 1개
- 능동부저 1개
- 브레드보드
- 점퍼 케이블

### 사용 기술
- Python
- `gpiozero`
- GPIO 입력/출력 제어
- 디지털 센서 신호 처리

### 주요 코드
```python
from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice
import time

bz = OutputDevice(18)
gas = DigitalInputDevice(17)

try:
    while True:
        if gas.value == 0:
            bz.on()
            print("Gas Detected")
        else:
            print("No Gas Detected")
            bz.off()

        time.sleep(0.2)

except KeyboardInterrupt:
    pass

bz.off()
```

### 학습 내용
MQ-2 센서는 가연성 가스나 연기 농도 변화에 따라 센서 내부의 전도도가 달라지는 특성을 이용하여 가스를 감지한다. FC-22 모듈은 이러한 센서 반응을 바탕으로 디지털 출력 신호를 제공하므로, 라즈베리파이에서 감지 여부를 비교적 간단하게 읽을 수 있다.  
능동부저는 내부 발진 회로가 포함되어 있어 전압이 인가되면 별도의 주파수 생성 없이 소리를 낼 수 있으므로, GPIO의 ON/OFF 제어만으로 경보음을 출력할 수 있다.  
이번 실험을 통해 디지털 센서 입력을 읽고, 그 결과에 따라 출력 장치를 즉시 제어하는 기본적인 AIoT 시스템 구조를 이해할 수 있었다.

### 실행 결과
가스 센서의 디지털 출력값이 감지 상태일 때 부저가 켜지고 `"Gas Detected"`가 출력되도록 구현하였다. 반대로 가스가 감지되지 않는 상태에서는 부저가 꺼지고 `"No Gas Detected"`가 출력되도록 구성하였다.  
이를 통해 센서 상태 변화에 따라 경보 장치가 연동되는 기본 동작을 확인할 수 있었다.

---

## project14 - PIR 모션 센서와 카메라를 이용한 움직임 감지 촬영 시스템

### 실험 개요
PIR 모션 센서를 이용해 주변의 움직임을 감지하고, 감지 신호가 들어오면 카메라로 사진을 자동 촬영하도록 구현하였다.  
`main14.py`에서는 PIR 센서의 기본 감지값을 확인하고, `main14-1.py`에서는 감지 결과를 카메라 촬영 기능과 연동하였다.  
해당 내용은 `project_14` 폴더 기준으로 정리하였다.

### 실험 목적
- PIR 모션 센서의 동작 방식과 출력값을 이해한다.
- 라즈베리파이에서 센서 입력을 읽고 조건문으로 처리하는 방법을 학습한다.
- 움직임 감지 이벤트를 카메라 촬영 기능과 연결하여 간단한 감시 시스템을 구현한다.

### 사용 부품
- Raspberry Pi
- PIR 모션 센서 1개
- Raspberry Pi Camera 또는 호환 카메라 모듈 1개
- 브레드보드
- 점퍼 케이블

### 사용 기술
- Python
- `gpiozero`
- `picamera2`
- `datetime`
- GPIO 입력 처리

### 주요 코드
```python
from gpiozero import MotionSensor
import time
from picamera2 import Picamera2
import datetime

pirPin = MotionSensor(16)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

try:
    while True:
        sensorValue = pirPin.value
        if sensorValue == 1:
            now = datetime.datetime.now()
            fileName = now.strftime('%Y-%m-%d %H:%M:%S')
            picam2.capture_file(fileName + '.jpg')
            time.sleep(0.5)

except KeyboardInterrupt:
    pass
```

### 학습 내용
PIR 센서는 적외선 변화량을 바탕으로 사람이나 물체의 움직임을 감지하며, 감지 시 1에 가까운 값을 출력하고 감지가 없을 때는 0에 가까운 값을 출력한다.  
먼저 센서의 `.value` 값을 반복적으로 출력해 보면서 실제로 움직임이 있을 때 값이 어떻게 변하는지 확인하였다. 이후 이 값을 조건문과 연결하여 움직임이 감지되면 즉시 사진을 촬영하도록 확장하였다.  
또한 파일명에 현재 시간을 넣어 사진이 덮어써지지 않도록 구성하고, 짧은 대기 시간을 추가하여 같은 움직임에 대해 사진이 과도하게 연속 저장되지 않도록 조정하였다.

### 실행 결과
PIR 센서가 움직임을 감지하면 현재 시각을 기준으로 한 이름의 이미지 파일이 자동으로 저장되도록 구현하였다.  
이를 통해 센서 입력, 조건 처리, 카메라 제어를 결합한 기초적인 움직임 감지 촬영 시스템을 구현할 수 있음을 확인하였다.

---

## project20 - 플라스크 웹서버를 이용한 LED 제어

### 실험 개요
Flask 웹 서버와 라즈베리파이 GPIO를 연동하여 웹 브라우저에서 LED를 제어하는 시스템을 구현하였다.  
`main20.py`에서는 URL 주소를 통해 LED를 제어하는 기본 방식을 확인하고, `main20-1.py`에서는 `index.html`의 버튼 입력을 받아 LED를 제어하도록 확장하였다.  
해당 내용은 `project_20` 폴더 기준으로 정리하였다.

### 실험 목적
- Flask 웹 서버의 기본 동작과 라우팅 방식을 이해한다.
- HTML 폼과 POST 요청을 이용하여 웹 입력을 서버로 전달하는 방법을 학습한다.
- 라즈베리파이 GPIO 제어와 웹 서버를 연동한 기초적인 AIoT 제어 시스템을 구현한다.

### 사용 부품
- Raspberry Pi
- 빨강 LED 1개
- 330옴 저항 1개
- 암/수 점퍼 케이블 2개

### 사용 기술
- Python
- Flask
- `gpiozero`
- HTML
- GPIO 출력 제어

### 주요 코드
```python
from flask import Flask, render_template, request
from gpiozero import LED

app = Flask(__name__)
red_led = LED(21)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def data():
    data = request.form['led']
    if data == 'on':
        red_led.on()
    elif data == 'off':
        red_led.off()
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
```

### 학습 내용
Flask는 `@app.route()`를 사용하여 특정 URL 요청에 맞는 함수를 실행할 수 있으며, 이를 통해 웹 브라우저의 요청과 GPIO 제어 코드를 연결할 수 있다. 먼저 `main20.py`에서는 `/ledon`, `/ledoff`와 같은 주소로 접속할 때 LED를 켜고 끄는 기본 방식을 확인하였다.  
이후 `main20-1.py`에서는 Flask의 `templates` 폴더 규칙을 이용하여 `index.html`을 불러오고, HTML 폼에서 전송된 `led` 값을 `request.form`으로 받아 LED를 제어하도록 확장하였다. 웹 페이지의 버튼 클릭이 서버의 POST 요청으로 전달되고, 서버는 그 값에 따라 GPIO 21번 LED를 제어한다.  
이번 실습을 통해 웹 서버, HTML 폼, GPIO 출력 제어가 하나의 흐름으로 연결되는 기초적인 웹 기반 AIoT 제어 구조를 이해할 수 있었다.

### 실행 결과
라즈베리파이에서 Flask 서버를 실행한 뒤, 웹 브라우저에서 해당 IP 주소로 접속하여 LED를 켜고 끌 수 있도록 구현하였다.  
특히 `index.html`의 `[on]`, `[off]` 버튼을 이용하여 보다 직관적으로 LED를 제어할 수 있음을 확인하였다.
