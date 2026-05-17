import requests  # OpenWeatherMap API에 HTTP 요청을 보내기 위한 라이브러리
import os  # espeak 명령어를 실행하기 위한 운영체제 관련 라이브러리
import time  # 일정 시간마다 날씨를 다시 안내하기 위한 시간 라이브러리

# OpenWeatherMap에서 발급받은 API 키를 입력하는 부분
# 실제 실행할 때는 "Enter your API key here" 부분에 본인의 API 키를 넣어야 한다.
API_KEY = "Enter your API key here"

# 서울의 현재 날씨를 섭씨 온도 기준으로 요청하는 API 주소를 만든다.
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

# espeak를 이용하여 문자열을 음성으로 출력하는 함수
def speak(option, msg):
    # option에는 속도, 음높이, 음량, 음성 종류 같은 설정값을 넣는다.
    # msg에는 실제로 읽어 줄 날씨 안내 문장을 넣는다.
    os.system("espeak {} '{}'".format(option, msg))

try:
    # 프로그램이 종료되기 전까지 날씨 정보를 반복해서 가져온다.
    while 1:
        # OpenWeatherMap API에 요청을 보내고 응답 데이터를 JSON 형태로 변환한다.
        response = requests.get(url)
        data = response.json()

        # JSON 데이터 중 main 항목에서 현재 기온과 습도 값을 추출한다.
        temp = data["main"]["temp"]
        humi = data["main"]["humidity"]

        # 가져온 기온과 습도 값을 사람이 들을 수 있는 문장으로 만든다.
        msg = '    기온은 ' + str(int(temp)) + ' 도 습도는 ' + str(humi) + '퍼센트 입니다.'
        print(msg)

        # espeak 음성 출력 옵션을 설정한다.
        # -s는 말하는 속도, -p는 음높이, -a는 음량, -v는 사용할 음성을 의미한다.
        option = '-s 180 -p 50 -a 200 -v ko+f5'
        speak(option, msg)

        # 10초마다 같은 과정을 반복하여 날씨를 다시 안내한다.
        time.sleep(10.0)

except KeyboardInterrupt:
    # Ctrl+C를 누르면 오류 메시지 없이 프로그램을 종료한다.
    pass
