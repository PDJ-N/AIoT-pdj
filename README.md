# 한신대학교 AIoT 설계입문

라즈베리파이와 Python을 활용하여 진행한 AIoT 설계입문 실험 내용을 정리한 저장소입니다.  
각 실험은 프로젝트 폴더 기준으로 누적되며, 실험 개요, 목적, 사용 부품, 사용 기술, 주요 코드, 학습 내용, 실행 결과를 함께 기록합니다.

---

## 목차
- [project2 - 라즈베리파이로 신호등 만들기](#project2---라즈베리파이로-신호등-만들기)
- [project6 - MQ-2 가스 감지 모듈과 능동부저를 이용한 가스 경보 시스템](#project6---mq-2-가스-감지-모듈과-능동부저를-이용한-가스-경보-시스템)
- [project14 - PIR 모션 센서와 카메라를 이용한 움직임 감지 촬영 시스템](#project14---pir-모션-센서와-카메라를-이용한-움직임-감지-촬영-시스템)
- [project20 - 플라스크 웹서버를 이용한 LED 제어](#project20---플라스크-웹서버를-이용한-led-제어)
- [project24 - API Key 발급받아 온습도 표시 GUI 프로그램 만들기](#project24---api-key-발급받아-온습도-표시-gui-프로그램-만들기)
- [project28 - 텔레그램으로 일기예보를 알려주는 알리미 만들기](#project28---텔레그램으로-일기예보를-알려주는-알리미-만들기)
- [project30 - MQTT 통신으로 제어하는 장치 만들기](#project30---mqtt-통신으로-제어하는-장치-만들기)
- [project32 - AI 음성 인식 날씨 안내 장치 만들기](#project32---ai-음성-인식-날씨-안내-장치-만들기)
- [project34 - OpenCV 졸음방지 디바이스 만들기](#project34---opencv-졸음방지-디바이스-만들기)

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

---

## project24 - API Key 발급받아 온습도 표시 GUI 프로그램 만들기

### 실험 개요
OpenWeatherMap에서 발급받은 API Key를 이용하여 서울의 현재 날씨 데이터를 가져오고, Python의 `tkinter`를 활용하여 온도와 습도를 GUI 창에 표시하는 프로그램을 구현하였다.  
OpenWeatherMap API는 현재 날씨 데이터를 JSON 형식으로 제공하며, 프로그램에서는 API 응답 데이터 중 `main.temp`와 `main.humidity` 값을 추출하여 화면에 출력하였다.  
해당 내용은 `project_24` 폴더의 `main24-3.py` 파일 기준으로 정리하였다.

### 실험 목적
- OpenWeatherMap 회원가입 및 API Key 발급 과정을 이해한다.
- API Key가 API 요청에서 인증 문자열로 사용되는 방식을 학습한다.
- Python으로 웹 API에 요청을 보내고 JSON 데이터를 처리하는 방법을 익힌다.
- `tkinter`를 이용하여 온도와 습도를 표시하는 간단한 GUI 프로그램을 구현한다.
- `window.after()`를 사용하여 일정 시간마다 데이터를 갱신하는 방법을 학습한다.

### 사용 부품 및 환경
- Raspberry Pi 또는 Python 실행 환경
- 인터넷 연결 환경
- OpenWeatherMap 계정
- OpenWeatherMap API Key

### 사용 기술
- Python
- `urllib.request`
- `json`
- `tkinter`
- OpenWeatherMap API
- JSON 데이터 처리
- GUI 프로그래밍

### 주요 코드
```python
import urllib.request, json, tkinter, tkinter.font

# OpenWeatherMap에서 발급받은 API 키를 입력하는 부분
# 실제 사용 시에는 본인의 API 키를 넣어야 한다.
API_KEY = "Enter your API key here"

# 1분마다 날씨 정보를 가져와 화면에 표시하는 함수
def tick1Min():
    # OpenWeatherMap API 요청 주소를 만든다.
    # q=Seoul은 서울의 날씨를 의미하고, units=metric은 섭씨 온도를 사용한다.
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

    # API 주소에 접속하여 날씨 데이터를 요청한다.
    with urllib.request.urlopen(url) as r:
        # 응답으로 받은 JSON 데이터를 Python 딕셔너리 형태로 변환한다.
        data = json.loads(r.read())

    # JSON 데이터에서 현재 온도와 습도 값을 가져온다.
    temp = data["main"]["temp"]
    humi = data["main"]["humidity"]

    # 가져온 온도와 습도 정보를 라벨에 출력한다.
    label.config(text=f"{temp:.1f}C   {humi}%")

    # 60000ms, 즉 1분 후에 tick1Min 함수를 다시 실행한다.
    window.after(60000, tick1Min)

# tkinter 윈도우를 생성한다.
window = tkinter.Tk()
window.title("TEMP HUMI DISPLAY")
window.geometry("400x100")
window.resizable(False, False)

# 화면에 표시할 글자 크기를 설정한다.
font = tkinter.font.Font(size=30)

# 온도와 습도를 출력할 라벨을 생성한다.
label = tkinter.Label(window, text="", font=font)
label.pack()

# 프로그램 시작 시 처음 한 번 날씨 정보를 가져온다.
tick1Min()

# tkinter 이벤트 루프를 실행하여 창이 계속 유지되도록 한다.
window.mainloop()
```

### 학습 내용
OpenWeatherMap API를 사용하기 위해서는 먼저 웹사이트에 회원가입한 뒤 API Key를 발급받아야 한다. API Key는 API 서버가 요청 사용자를 확인하기 위한 인증 문자열로 사용되며, 요청 URL에 포함되어 서버에서 유효성을 검증한다.  
이번 실험에서는 `urllib.request.urlopen()`을 사용하여 OpenWeatherMap API 주소에 요청을 보냈고, 응답으로 받은 JSON 데이터를 `json.loads()`를 통해 Python 딕셔너리 형태로 변환하였다. 이후 `data["main"]["temp"]`와 `data["main"]["humidity"]`를 사용하여 현재 온도와 습도 값을 추출하였다.  
또한 `tkinter`의 `Tk()`, `Label`, `Font`를 이용하여 GUI 창을 만들고, `label.config()`로 화면에 표시되는 값을 갱신하였다. `window.after(60000, tick1Min)`을 사용하여 1분마다 같은 함수를 다시 실행하도록 구성하면서, GUI 프로그램에서 주기적으로 데이터를 업데이트하는 방식도 학습하였다.  
API Key는 발급 직후 바로 동작하지 않을 수 있으며, 서버에서 활성화되는 데 시간이 필요할 수 있다. 따라서 실행했을 때 온도와 습도가 바로 표시되지 않으면 일정 시간이 지난 뒤 다시 실행하여 확인해야 한다. 또한 API Key는 개인 인증 정보이므로 GitHub나 보고서 캡처에 그대로 노출하지 않도록 주의해야 한다.

### 실행 결과
발급받은 API Key를 코드의 `API_KEY` 변수에 입력한 뒤 프로그램을 실행하면 `TEMP HUMI DISPLAY`라는 제목의 GUI 창이 나타나고, 서울의 현재 온도와 습도가 표시된다.  
실습에서는 OpenWeatherMap 웹사이트에서 Seoul을 검색하여 표시된 온습도와 GUI 프로그램의 결과를 비교하였고, OpenWeatherMap에서 제공하는 값과 프로그램에 표시된 값이 일치함을 확인하였다.  
이를 통해 외부 웹 API 호출, JSON 데이터 처리, GUI 출력, 주기적 갱신을 하나의 프로그램으로 연결하는 기본적인 API 기반 AIoT 응용 구조를 이해할 수 있었다.

---

## project28 - 텔레그램으로 일기예보를 알려주는 알리미 만들기

### 실험 개요
OpenWeatherMap API에서 서울의 3시간 간격 일기예보 데이터를 가져오고, 이를 보기 좋은 문자열로 가공한 뒤 텔레그램 봇을 통해 자동 전송하는 알리미 프로그램을 구현하였다.  
이전 실습에서 발급받은 OpenWeatherMap API Key를 활용하였으며, 텔레그램 BotFather에서 발급받은 봇 토큰과 chat_id를 사용하여 개인 텔레그램 계정으로 메시지를 전송하였다.  
해당 내용은 `project_28` 폴더의 `main28.py`, `main28-1.py`, `main28-2.py` 파일 기준으로 정리하였다.

### 실험 목적
- OpenWeatherMap의 예보 API를 호출하여 3시간 단위 날씨 데이터를 가져오는 방법을 학습한다.
- JSON 응답에서 시간, 기온, 습도, 날씨 설명 값을 추출하는 방법을 이해한다.
- 추출한 데이터를 `(07h 15.2C 60% clear sky)`와 같은 메시지 형식으로 가공한다.
- 텔레그램 봇 토큰과 chat_id를 이용하여 Python에서 메시지를 전송한다.
- `datetime`과 `asyncio`를 활용하여 정해진 시간에 알림을 보내는 자동화 흐름을 구현한다.

### 사용 부품 및 환경
- Raspberry Pi 또는 Python 실행 환경
- 인터넷 연결 환경
- OpenWeatherMap 계정 및 API Key
- Telegram 계정
- Telegram BotFather로 생성한 봇 토큰
- 메시지를 받을 Telegram chat_id

### 사용 기술
- Python
- `urllib.request`
- `json`
- `datetime`
- `asyncio`
- `python-telegram-bot`
- OpenWeatherMap Forecast API
- Telegram Bot API

### 파일별 역할
- `main28.py`: 서울 예보 API를 호출하여 시간, 기온, 습도, 날씨 설명 데이터를 리스트로 확인한다.
- `main28-1.py`: 예보 데이터를 사람이 읽기 쉬운 문자열 형태로 가공하여 출력한다.
- `main28-2.py`: 가공된 날씨 메시지를 정해진 시간마다 텔레그램으로 자동 전송한다.

### 주요 코드
```python
import urllib.request
import json
import datetime
import asyncio
from telegram import Bot

telegram_id = 'Enter your chat ID here'
my_token = 'Enter your bot token here'
api_key = 'Enter your API key here'

bot = Bot(token=my_token)

ALERT_HOURS = [7, 10, 13, 16, 19, 22]
ALERT_TIMES = ["08:30", "15:20"]

def getWeather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())

    text = ""
    for i in range(8):
        item = data['list'][i]
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
        temp = item['main']['temp']
        humi = item['main']['humidity']
        desc = item['weather'][0]['description']
        text += f"({hour}h {temp}C {humi}% {desc})\n"

    return text

async def main():
    try:
        while True:
            now = datetime.datetime.now()
            hm = now.strftime('%H:%M')

            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0
            is_alert_time = hm in ALERT_TIMES and now.second == 0

            if is_alert_hour or is_alert_time:
                msg = getWeather()
                print(msg)
                await bot.send_message(chat_id=telegram_id, text=msg)

            await asyncio.sleep(1)

    except KeyboardInterrupt:
        pass

asyncio.run(main())
```

### 학습 내용
먼저 `main28.py`에서는 OpenWeatherMap Forecast API 주소를 만들고 `urllib.request.urlopen()`으로 요청을 보냈다. API 응답은 JSON 형식이므로 `json.loads()`를 사용하여 Python에서 다룰 수 있는 자료형으로 변환하였다. 이후 `data['list']`에 들어 있는 예보 목록에서 시간, 기온, 습도, 날씨 설명을 각각 추출하였다.  
`main28-1.py`에서는 추출한 데이터를 단순 리스트 출력이 아니라 텔레그램 메시지로 보내기 좋은 문자열 형태로 가공하였다. `cnt=8`은 3시간 간격 예보 8개를 의미하므로 약 하루치 예보를 확인할 수 있으며, 각 항목은 `(시간h 기온C 습도% 날씨설명)` 형식으로 정리하였다.  
최종 단계인 `main28-2.py`에서는 `Bot(token=my_token)`으로 텔레그램 봇 객체를 만들고, 조건에 맞는 시간이 되었을 때 `bot.send_message()`로 날씨 메시지를 전송하도록 구성하였다. `ALERT_HOURS`는 오전 7시부터 3시간 간격의 정각 알림을 담당하고, `ALERT_TIMES`는 실습 확인을 위해 원하는 시각을 직접 추가할 수 있는 부분이다.  
또한 `while True` 반복문 안에서 현재 시간을 1초마다 확인하고, `now.second == 0` 조건을 함께 사용하여 같은 분 안에서 메시지가 여러 번 전송되는 것을 줄였다. `asyncio.sleep(1)`을 사용하여 비동기 방식으로 대기하면서 텔레그램 메시지 전송 함수도 `await`로 실행하였다.

### 실행 결과
API Key, 텔레그램 봇 토큰, chat_id를 코드에 입력한 뒤 프로그램을 실행하면 지정된 시간에 서울의 일기예보 메시지가 터미널에 출력되고 텔레그램으로도 전송된다.  
실습에서는 현재 시간의 1분 뒤를 `ALERT_TIMES`에 추가하여 테스트하였고, 해당 시간이 되었을 때 터미널에 날씨 메시지 로그가 나타나며 텔레그램에서도 동일한 메시지를 정상적으로 수신하는 것을 확인하였다.  
이를 통해 외부 날씨 API 호출, JSON 데이터 처리, 메시지 문자열 가공, 텔레그램 봇 전송, 시간 조건 기반 자동화를 연결한 AIoT 알림 시스템의 기본 구조를 이해할 수 있었다.

---

## project30 - MQTT 통신으로 제어하는 장치 만들기

### 실험 개요
MQTT 통신을 이용하여 PC에서 발행한 메시지로 라즈베리파이에 연결된 LED를 제어하고, 라즈베리파이에서도 주기적으로 메시지를 발행하는 양방향 통신 프로그램을 구현하였다.  
처음에는 PC의 MQTT.fx에서 `led` 토픽으로 `green_on`, `blue_off`와 같은 명령을 발행하고, 라즈베리파이가 이를 구독하여 LED를 제어하는 흐름을 확인하였다. 이후 `threading`을 사용하여 라즈베리파이가 `led` 토픽을 계속 구독하면서 동시에 `hello` 토픽으로 숫자 값을 1초마다 발행하도록 확장하였다.  
해당 내용은 `project_30` 폴더의 `main30-1.py` 파일 기준으로 정리하였다.

### 실험 목적
- MQTT의 publish/subscribe 구조를 이해한다.
- PC에서 발행한 MQTT 메시지를 라즈베리파이가 구독하여 GPIO LED를 제어하는 방법을 학습한다.
- 라즈베리파이에서 특정 토픽으로 메시지를 발행하고 PC에서 이를 구독하여 확인하는 방법을 익힌다.
- `threading`을 사용하여 메시지 수신 대기와 주기적 메시지 발행을 동시에 처리하는 구조를 구현한다.

### 사용 부품 및 환경
- Raspberry Pi
- 브레드보드 1개
- 초록 LED 1개
- 파랑 LED 1개
- 빨강 LED 1개
- 330옴 저항 3개
- 암/수 점퍼 케이블
- MQTT.fx가 설치된 PC
- MQTT 브로커 접속 환경

### 사용 기술
- Python
- `paho-mqtt`
- `gpiozero`
- `threading`
- MQTT publish/subscribe 통신
- GPIO 출력 제어

### 주요 코드
```python
import paho.mqtt.client as mqtt  # MQTT 통신을 위한 paho-mqtt 라이브러리 불러오기
import time  # 1초 간격으로 메시지를 발행하기 위한 시간 모듈 불러오기
from gpiozero import LED  # 라즈베리파이 GPIO 핀에 연결된 LED를 제어하기 위한 클래스 불러오기
import threading  # 발행과 구독을 동시에 처리하기 위한 스레드 모듈 불러오기

greenLed = LED(16)  # GPIO 16번 핀에 연결된 초록 LED 설정
blueLed = LED(20)  # GPIO 20번 핀에 연결된 파란 LED 설정
redLed = LED(21)  # GPIO 21번 핀에 연결된 빨간 LED 설정

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    message = msg.payload.decode()
    print(message)
    if message == "green_on":
        greenLed.on()
    elif message == "green_off":
        greenLed.off()
    elif message == "blue_on":
        blueLed.on()
    elif message == "blue_off":
        blueLed.off()
    elif message == "red_on":
        redLed.on()
    elif message == "red_off":
        redLed.off()

client = mqtt.Client()
client.on_message = on_message

broker_address="192.168.137.230"
client.connect(broker_address)
client.subscribe("led",1)

count = 0
def send_thread():
    global count
    while 1:
        count = count + 1
        client.publish("hello", str(count))
        time.sleep(1.0)

task = threading.Thread(target = send_thread)
task.start()

client.loop_forever()
```

### 학습 내용
MQTT는 발행자와 구독자가 직접 연결되는 방식이 아니라, 브로커를 중심으로 토픽을 통해 데이터를 주고받는 publish/subscribe 구조를 사용한다. 이번 실험에서는 PC의 MQTT.fx가 `led` 토픽으로 LED 제어 명령을 발행하고, 라즈베리파이의 Python 프로그램이 해당 토픽을 구독하여 메시지에 따라 GPIO 16번, 20번, 21번 핀의 LED를 제어하였다.  
수신된 MQTT 메시지는 바이트 형태이므로 `msg.payload.decode()`를 사용하여 문자열로 변환한 뒤, `green_on`, `green_off`, `blue_on`, `blue_off`, `red_on`, `red_off` 명령에 따라 각각의 LED를 켜거나 끄도록 구성하였다. 이를 통해 MQTT 메시지가 실제 하드웨어 출력 제어로 이어지는 흐름을 확인하였다.  
또한 `client.loop_forever()`는 MQTT 메시지를 계속 수신하기 위한 무한 대기 루프이므로, 이 코드가 실행되면 그 아래의 일반 코드는 순차적으로 실행되기 어렵다. 따라서 `main30-1.py`에서는 `send_thread()` 함수를 별도의 스레드로 실행하여 `hello` 토픽으로 숫자 값을 1초마다 발행하고, 메인 흐름에서는 `led` 토픽 수신을 계속 유지하도록 구성하였다.  
이를 통해 라즈베리파이가 MQTT 메시지를 받는 구독자 역할과 메시지를 보내는 발행자 역할을 동시에 수행할 수 있으며, `threading`을 사용하면 하나의 Python 프로그램 안에서 양방향 통신 흐름을 구현할 수 있음을 학습하였다.

### 실행 결과
라즈베리파이에서 `main30-1.py`를 실행한 뒤 PC의 MQTT.fx Publish 메뉴에서 `led` 토픽으로 `green_on`, `green_off`, `blue_on`, `blue_off`, `red_on`, `red_off` 명령을 발행하면 각 색상의 LED가 명령에 맞게 켜지고 꺼지도록 구현하였다.  
동시에 MQTT.fx의 Subscribe 메뉴에서 `hello` 토픽을 구독하면 라즈베리파이가 1초마다 발행하는 숫자 값이 순서대로 수신되는 것을 확인하였다.  
이를 통해 MQTT 기반 LED 제어와 `threading`을 이용한 주기적 메시지 발행을 함께 수행하는 양방향 AIoT 통신 구조를 구현할 수 있었다.

---

## project32 - AI 음성 인식 날씨 안내 장치 만들기

### 실험 개요
라즈베리파이 5에서 마이크로 입력받은 음성을 Python으로 인식하고, 사용자가 "날씨"라는 단어를 말하면 OpenWeatherMap API를 통해 서울의 현재 기온과 습도를 조회한 뒤 `espeak`로 음성 안내하는 프로그램을 구현하였다.  
처음에는 날씨 API와 TTS 출력을 연결하여 주기적으로 날씨를 읽어 주는 구조를 확인하고, 이후 Google Speech Recognition을 이용한 한국어 음성 인식 결과와 날씨 안내 기능을 결합하였다.  
해당 내용은 `project_32` 폴더의 `main32.py`, `main32-1.py`, `main32-2.py` 파일 기준으로 정리하였다.

### 실험 목적
- 마이크 입력을 Python에서 받아오는 방법을 학습한다.
- Google Speech Recognition을 이용하여 한국어 음성을 텍스트로 변환하는 과정을 이해한다.
- 인식된 문장에서 특정 키워드를 찾아 조건문으로 처리하는 방법을 익힌다.
- OpenWeatherMap API 응답에서 현재 기온과 습도 값을 추출한다.
- `espeak`를 이용하여 텍스트 형태의 날씨 정보를 음성으로 출력한다.

### 사용 부품 및 환경
- Raspberry Pi 5
- 마이크 또는 USB 오디오 입력 장치
- 스피커 또는 오디오 출력 장치
- 인터넷 연결 환경
- OpenWeatherMap 계정 및 API Key
- Python 3.12.10 실행 환경

### 사용 기술
- Python
- `speech_recognition`
- PyAudio
- `requests`
- OpenWeatherMap Current Weather API
- Google Speech Recognition
- `espeak` TTS

### 파일별 역할
- `main32.py`: 마이크 음성을 입력받아 Google Speech Recognition으로 한국어 텍스트를 인식하고, "날씨" 키워드 감지를 확인한다.
- `main32-1.py`: OpenWeatherMap API에서 서울의 현재 기온과 습도를 가져와 `espeak`로 반복 안내한다.
- `main32-2.py`: 음성 입력, STT 변환, 키워드 감지, 날씨 API 호출, TTS 출력을 하나의 흐름으로 통합한다.

### 주요 코드
```python
import speech_recognition as sr
import requests
import os

API_KEY = "Enter your API key here"
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

def speak(option, msg):
    os.system("espeak {} '{}'".format(option, msg))

try:
    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)

            if "날씨" in text:
                print("날씨 음성을 인식하였습니다.")
                response = requests.get(url)
                data = response.json()

                temp = data["main"]["temp"]
                humi = data["main"]["humidity"]

                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    pass
```

### 학습 내용
`speech_recognition` 라이브러리의 `Recognizer()`와 `Microphone()`을 사용하면 마이크로 입력된 음성을 Python 프로그램에서 받아올 수 있다. 이후 `recognize_google(audio, language='ko-KR')`를 사용하여 녹음된 음성을 한국어 텍스트로 변환하였다. 이 과정은 Google Speech Recognition 서비스를 사용하므로 인터넷 연결이 필요하다.  
인식된 문장에서 특정 단어가 포함되어 있는지 확인할 때는 `if "날씨" in text:`와 같이 작성해야 한다. 반대로 `if text in "날씨":`처럼 작성하면 사용자가 말한 전체 문장이 `"날씨"`라는 짧은 문자열 안에 포함되는지를 검사하게 되므로, `"오늘 날씨 알려줘"`와 같은 문장은 올바르게 감지되지 않는다.  
날씨 정보는 OpenWeatherMap Current Weather API를 이용하여 가져왔고, 응답으로 받은 JSON 데이터에서 `data["main"]["temp"]`와 `data["main"]["humidity"]` 값을 추출하였다. 추출한 기온과 습도는 문자열로 조합한 뒤 `espeak` 명령어에 전달하여 음성으로 출력하였다. 이를 통해 마이크 입력, STT, 키워드 판단, 웹 API 호출, TTS 출력이 하나의 AIoT 음성 서비스 흐름으로 연결되는 구조를 이해할 수 있었다.

### 실행 결과
`main32-1.py`를 실행하면 OpenWeatherMap API에서 가져온 서울의 현재 기온과 습도가 터미널에 출력되고, 같은 내용이 `espeak`를 통해 음성으로 안내된다.  
`main32-2.py`를 실행한 뒤 마이크에 "날씨"가 포함된 문장을 말하면 Google Speech Recognition으로 음성이 텍스트로 변환되고, 키워드가 감지되었을 때 서울의 현재 기온과 습도를 조회하여 음성으로 출력한다.  
이를 통해 사용자의 음성 명령을 기반으로 외부 날씨 데이터를 조회하고, 다시 음성으로 안내하는 기초적인 AI 음성 날씨 안내 장치를 구현할 수 있음을 확인하였다.

---

## project34 - OpenCV 졸음방지 디바이스 만들기

### 실험 개요
OpenCV를 이용하여 웹캠 영상에서 얼굴과 눈을 실시간으로 탐지하고, 눈이 감긴 상태로 판단되면 능동부저로 경보음을 출력하는 졸음방지 디바이스를 구현하였다.  
`main34.py`에서는 얼굴과 눈이 탐지된 위치를 사각형으로 표시하는 기본 영상 처리 흐름을 확인하고, `main34-1.py`에서는 눈 탐지 결과에 따라 GPIO 16번 핀에 연결된 부저를 제어하도록 확장하였다.  
해당 내용은 `project_34` 폴더의 `main34.py`, `main34-1.py` 파일 기준으로 정리하였다.

### 실험 목적
- OpenCV의 Haar Cascade 분류기를 이용하여 얼굴과 눈을 탐지하는 방법을 학습한다.
- 웹캠에서 입력된 영상을 프레임 단위로 읽고 흑백 영상으로 변환하는 과정을 이해한다.
- 얼굴 영역 내부에서 눈을 탐지하여 눈 개수에 따라 상태를 판단하는 구조를 구현한다.
- `gpiozero`의 `Buzzer`를 사용하여 영상 인식 결과와 GPIO 출력 장치를 연동한다.
- 사용자가 `q` 키를 입력하면 프로그램을 종료하고, 종료 시 부저를 안전하게 끄는 흐름을 확인한다.

### 사용 부품 및 환경
- Raspberry Pi
- 웹캠 1개
- 능동부저 1개
- 브레드보드 1개
- 암/수 점퍼 케이블 2개
- OpenCV와 `gpiozero`가 설치된 Python 실행 환경

### 사용 기술
- Python
- OpenCV
- `cv2`
- Haar Cascade 얼굴/눈 탐지
- `gpiozero`
- GPIO 출력 제어

### 파일별 역할
- `main34.py`: 웹캠 영상에서 얼굴과 눈을 탐지하고, 탐지된 영역을 각각 파란색과 초록색 사각형으로 표시한다.
- `main34-1.py`: 눈 탐지 개수를 기준으로 졸음 상태를 판단하고, 눈이 1개 이하로 감지되면 능동부저를 울린다.

### 주요 코드
```python
import cv2
from gpiozero import Buzzer

buzzerPin = Buzzer(16)

def main():
    camera = cv2.VideoCapture(-1)
    camera.set(3,640)
    camera.set(4,480)

    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'
    face_cascade = cv2.CascadeClassifier(face_xml)
    eye_cascade = cv2.CascadeClassifier(eye_xml)

    while( camera.isOpened() ):
        _, image = camera.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)
        print("faces detected Number: " + str(len(faces)))

        if len(faces):
            for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

                face_gray = gray[y:y+h, x:x+w]
                face_color = image[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(face_gray,scaleFactor=1.1,minNeighbors=5)

                if len(eyes) <= 1:
                    buzzerPin.on()
                else:
                    buzzerPin.off()

                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

        cv2.imshow('result', image)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    buzzerPin.off()

if __name__ == '__main__':
    main()
```

### 학습 내용
OpenCV의 `VideoCapture(-1)`를 사용하면 연결된 웹캠을 자동으로 열 수 있으며, `camera.read()`를 통해 현재 화면을 프레임 단위로 받아올 수 있다. 얼굴과 눈 탐지에는 OpenCV에 내장된 Haar Cascade XML 모델을 사용하였고, 컬러 영상은 `cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`를 통해 흑백 영상으로 변환한 뒤 탐지를 수행하였다. 흑백 영상은 컬러 영상보다 연산량이 적어 실시간 탐지에 적합하다.  
먼저 `main34.py`에서는 전체 영상에서 얼굴을 탐지하고, 탐지된 얼굴 영역 내부에서 다시 눈을 찾도록 구성하였다. 얼굴 영역은 파란색 사각형으로 표시하고, 눈 영역은 초록색 사각형으로 표시하여 탐지 결과를 GUI 창에서 직접 확인할 수 있도록 하였다.  
이후 `main34-1.py`에서는 탐지된 눈의 개수를 조건문으로 판단하였다. 눈이 2개 이상 감지되면 정상 상태로 보고 부저를 끄며, 눈이 1개 이하로 감지되면 눈을 감은 상태로 판단하여 능동부저를 켜도록 구성하였다. 이를 통해 영상 처리 결과가 실제 GPIO 출력 제어로 이어지는 AIoT 응용 흐름을 학습하였다.

### 실행 결과
`main34.py`를 실행하면 웹캠 영상이 GUI 창에 표시되고, 얼굴에는 파란색 사각형, 눈에는 초록색 사각형이 표시된다. 터미널에는 현재 프레임에서 탐지된 얼굴 수가 `"faces detected Number"` 형식으로 출력된다.  
`main34-1.py`를 실행한 뒤 사용자가 눈을 감으면 탐지된 눈 개수가 1개 이하로 줄어들면서 GPIO 16번 핀에 연결된 능동부저가 울리도록 구현하였다. 다시 눈이 2개 이상 감지되면 부저가 꺼지고, `q` 키를 누르면 OpenCV 창이 닫히며 프로그램이 종료된다.  
이를 통해 OpenCV 기반 얼굴/눈 인식과 라즈베리파이 GPIO 부저 제어를 결합한 기초적인 졸음방지 알림 디바이스를 구현할 수 있음을 확인하였다.
