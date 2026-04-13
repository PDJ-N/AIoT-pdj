from flask import Flask # 플라스크 웹 서버 라이브러리
from gpiozero import LED # 라즈베리파이 GPIO LED 제어 라이브러리

app = Flask(__name__) # Flask 앱 생성

red_led = LED(21) # GPIO 21번 핀에 연결된 LED 설정

@app.route('/') # 기본 주소(/) 접속 시 실행
def flask(): 
    return "hello Flask" # 브라우저에 텍스트 출력

@app.route('/ledon') # /ledon 주소 접속 시 실행
def ledOn():
    red_led.on() # LED 켜기
    return "<h1> LED ON </h1> " # 브라우저에 결과 출력

@app.route('/ledoff') # /ledoff 주소 접속 시 실행
def LedOff():
    red_led.off() # LED 끄기
    return "<h1> LED OFF </h1>" # 브라우저에 결과 출력

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = "80") # 모든 IP(0.0.0.0)에서 80번 포트로 웹 서버 실행

    # Flask 앱이 실행되면 웹 브라우저에서 라즈베리파이 IP 주소로 접속하여 LED를 켜고 끌 수 있습니다. 예를 들어, 라즈베리파이의 IP 주소가
    # 플라스크 웹서버를 이용하여 LED를 제어하는 방법을 보여주는 간단한 예제입니다. 웹 브라우저에서 http://<라즈베리파이_IP>/ledon 으로 접속하면 LED가 켜지고 http://<라즈베리파이_IP>/ledoff 으로 접속하면 LED가 꺼집니다.
