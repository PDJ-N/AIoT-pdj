from gpiozero import MotionSensor
import time

pirPin = MotionSensor(16)  # GPIO16 PIR sensor

try:
    while True:
        sensorValue = pirPin.value
        print(sensorValue)  # 1: motion detected, 0: idle
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
