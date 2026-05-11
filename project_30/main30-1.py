import paho.mqtt.client as mqtt  # MQTT 통신을 위한 paho-mqtt 라이브러리 불러오기
import time  # 1초 간격으로 메시지를 발행하기 위한 시간 모듈 불러오기
from gpiozero import LED  # 라즈베리파이 GPIO 핀에 연결된 LED를 제어하기 위한 클래스 불러오기
import threading  # 발행과 구독을 동시에 처리하기 위한 스레드 모듈 불러오기

greenLed = LED(16)  # GPIO 16번 핀에 연결된 초록 LED 설정
blueLed = LED(20)  # GPIO 20번 핀에 연결된 파란 LED 설정
redLed = LED(21)  # GPIO 21번 핀에 연결된 빨간 LED 설정

def on_message(client, userdata, msg):  # 브로커로부터 메시지를 받으면 자동으로 실행되는 콜백 함수
    print(msg.topic+" "+str(msg.payload))  # 수신된 토픽 이름과 바이트 데이터를 터미널에 출력
    message = msg.payload.decode()  # 바이트 형태의 메시지를 문자열로 변환
    print(message)  # 변환된 메시지를 다시 출력하여 실제 명령어를 확인
    if message == "green_on":  # "green_on" 명령을 받으면
        greenLed.on()  # 초록 LED 켜기
    elif message == "green_off":  # "green_off" 명령을 받으면
        greenLed.off()  # 초록 LED 끄기
    elif message == "blue_on":  # "blue_on" 명령을 받으면
        blueLed.on()  # 파란 LED 켜기
    elif message == "blue_off":  # "blue_off" 명령을 받으면
        blueLed.off()  # 파란 LED 끄기
    elif message == "red_on":  # "red_on" 명령을 받으면
        redLed.on()  # 빨간 LED 켜기
    elif message == "red_off":  # "red_off" 명령을 받으면
        redLed.off()  # 빨간 LED 끄기

client = mqtt.Client()  # MQTT 클라이언트 객체 생성
client.on_message = on_message  # 메시지 수신 시 on_message 함수가 실행되도록 연결

broker_address="192.168.137.230"  # MQTT 브로커가 실행 중인 라즈베리파이 또는 PC의 IP 주소 설정
client.connect(broker_address)  # 지정한 브로커 주소로 연결 깃허브에 올릴 때는 IP 주소 대신 원문으로 푸시함
client.subscribe("led",1)  # "led" 토픽을 QoS 1로 구독하여 LED 제어 명령을 수신

count = 0  # "hello" 토픽으로 보낼 숫자의 초기값 설정
def send_thread():  # 1초마다 숫자를 증가시켜 MQTT 메시지를 발행하는 스레드 함수
    global count  # 함수 밖에서 선언한 count 값을 수정하기 위해 전역 변수로 사용
    while 1:  # 프로그램이 실행되는 동안 계속 반복
        count = count + 1  # 발행할 숫자를 1씩 증가
        client.publish("hello", str(count))  # "hello" 토픽으로 증가한 숫자를 문자열로 발행
        time.sleep(1.0)  # 1초 대기 후 다음 숫자를 발행

task = threading.Thread(target = send_thread)  # send_thread 함수를 별도 스레드 작업으로 생성
task.start()  # 스레드를 시작하여 발행 작업이 구독 루프와 동시에 실행되도록 함

client.loop_forever()  # MQTT 메시지 수신 대기 루프를 실행하여 "led" 토픽 구독 상태 유지

# 이 코드는 MQTT 프로토콜을 사용하여 라즈베리파이에서 LED를 제어하는 예제입니다.
# "led" 토픽으로 수신된 명령어에 따라 초록, 파란, 빨간 LED를 켜거나 끌 수 있으며, 동시에 "hello" 토픽으로 1초마다 증가하는 숫자를 발행합니다.
# MQTT 브로커의 IP 주소는 실제 환경에 맞게 변경해야 합니다.
