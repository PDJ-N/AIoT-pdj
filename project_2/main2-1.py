from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(2,3,4,20,21)

try:
    while 1:
        leds.value = (0,0,1,1,0)
        sleep(3.0)
        leds.value = (0,1,0,1,0)
        sleep(1.0)
        leds.value = (1,0,0,0,1)
        sleep(3.0)
    
except KeyboardInterrupt:
    pass

leds.off()
