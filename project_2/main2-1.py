from gpiozero import LEDBoard
from time import sleep

# 이번 실습에서는 LEDBoard로 여러 개의 LED를 한 번에 제어하는 방법을 연습했다.
# 앞의 3개는 차량 신호등, 뒤의 2개는 보행자 신호등이라고 생각하고 연결했다.
# 핀 순서를 직접 맞춰보면서 어떤 LED가 어떤 역할인지 같이 익혔다.
leds = LEDBoard(2,3,4,20,21)

try:
    while 1:
        # 첫 번째는 차량이 지나가고 보행자는 기다리는 상태다.
        # tuple 값으로 LED 여러 개를 한 번에 바꿀 수 있는 점이 편하다고 느꼈다.
        leds.value = (0,0,1,1,0)
        sleep(3.0)

        # 두 번째는 차량 노란불 상태로, 곧 멈춘다는 흐름을 표현했다.
        leds.value = (0,1,0,1,0)
        sleep(1.0)

        # 세 번째는 차량을 멈추고 보행자가 건널 수 있게 바꾼 상태다.
        # sleep 시간을 주면서 신호가 순서대로 반복되도록 만드는 것도 같이 연습했다.
        leds.value = (1,0,0,0,1)
        sleep(3.0)
    
except KeyboardInterrupt:
    # 실행하다가 Ctrl+C로 멈출 수도 있어서 예외 처리도 같이 넣어봤다.
    pass

# 프로그램이 끝날 때는 LED가 계속 켜져 있지 않게 마지막에 전부 꺼주도록 했다.
leds.off()
