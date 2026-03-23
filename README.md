# 한신대학교 AIoT 설계입문

라즈베리파이와 Python을 활용하여 진행한 AIoT 설계입문 실험 내용을 정리한 저장소입니다.  
각 실험은 주차별로 구성되어 있으며, 실험 목적, 사용 기술, 코드, 실행 결과를 함께 기록합니다.

---

## 목차
- [1주차 - 라즈베리파이로 신호등 만들기](#1주차---라즈베리파이로-신호등-만들기)

---

## 1주차 - 라즈베리파이로 신호등 만들기

### 실험 개요
라즈베리파이 GPIO 핀과 LED를 이용하여 차량용 및 보행자용 신호등 시스템을 구현하였다.  
Python의 `gpiozero` 라이브러리를 활용하여 LED의 점등 순서를 제어하였다.

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
- gpiozero
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
