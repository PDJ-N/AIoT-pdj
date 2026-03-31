from gpigzero import DigitalINputDevice
from gpiozero import OutputDevice
import time

# 이번 실습에서는 가스 센서 값을 읽고, 그 값에 따라 부저가 울리게 만드는 흐름을 연습했다.
# 센서는 입력 장치이고 부저는 출력 장치라는 점도 같이 구분해봤다.
bz = OutputDevice (18)
gas=DigitalINputDevice (17)

try:
    while True:
        # 센서 값이 0일 때를 가스가 감지된 상황으로 보고 부저가 바로 울리게 했다.
        if gas.value == 0:
            bz.on()
            print("Gas Detected")
        else:
            # 반대로 감지되지 않으면 부저를 끄고 현재 상태를 출력하게 했다.
            print("No Gas Detected")
            bz.off()

        # 너무 빠르게 반복하지 않게 짧게 쉬면서 센서 상태를 계속 확인하게 만들었다.
        time.sleep(0.2)

except KeyboardInterrupt:
    # 실행 중에 멈출 수도 있어서 종료할 때를 대비한 예외 처리도 넣었다.
    pass

# 끝날 때 부저가 계속 울리면 안 되니까 마지막에 꼭 꺼주도록 했다.
bz.off()
