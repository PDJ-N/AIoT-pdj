import speech_recognition as sr  # 마이크 음성을 텍스트로 변환하기 위한 라이브러리
import requests  # OpenWeatherMap API에 HTTP 요청을 보내기 위한 라이브러리
import os  # espeak 명령어를 실행하기 위한 운영체제 관련 라이브러리

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
    # 프로그램이 종료되기 전까지 계속 마이크 입력을 기다린다.
    while True:
        # 음성 인식을 수행할 Recognizer 객체를 생성한다.
        r = sr.Recognizer()
        
        # 기본 마이크를 입력 장치로 사용한다.
        with sr.Microphone() as source:
            print("Say something!")
            # 사용자가 말한 음성을 녹음한다.
            audio = r.listen(source)
            
        try:
            # 녹음한 음성을 Google Speech Recognition을 이용해 한국어 텍스트로 변환한다.
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)

            # 인식된 문장 안에 "날씨"라는 단어가 포함되어 있으면 날씨 안내를 실행한다.
            if "날씨" in text:
                print("날씨 음성을 인식하였습니다.")

                # OpenWeatherMap API에 요청을 보내고 응답 데이터를 JSON 형태로 변환한다.
                response = requests.get(url)
                data = response.json()

                # JSON 데이터 중 main 항목에서 현재 기온과 습도 값을 추출한다.
                temp = data["main"]["temp"]
                humi = data["main"]["humidity"]
                
                # 가져온 기온과 습도 값을 사람이 들을 수 있는 문장으로 만든다.
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                
                # espeak 음성 출력 옵션을 설정한다.
                # -s는 말하는 속도, -p는 음높이, -a는 음량, -v는 사용할 음성을 의미한다.
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg)
            
        except sr.UnknownValueError:
            # 음성은 입력되었지만 Google STT가 내용을 이해하지 못한 경우
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            # 인터넷 연결 문제나 Google STT 서비스 요청 실패가 발생한 경우
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    # Ctrl+C를 누르면 오류 메시지 없이 프로그램을 종료한다.
    pass


# 이 코드는 마이크로부터 음성을 입력받아 Google Speech Recognition을 이용해 텍스트로 변환한 후,
# "날씨"라는 단어가 포함된 문장이 인식되면 OpenWeatherMap API를 통해 서울의 현재 기온과 습도를 가져와서 espeak로 음성 안내를 하는 예제입니다.
# API 키와 espeak 옵션은 실제 환경에 맞게 조정해야 합니다. 실제 저의 api키는 공개할 수 없으므로 "Enter your API key here" 부분에 본인의 키를 입력하여 사용해야 합니다. 