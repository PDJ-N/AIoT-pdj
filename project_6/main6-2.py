from gpigzero import DigitalINputDevice
from gpiozero import OutputDevice
import time
bz = OutputDevice (18)
gas=DigitalINputDevice (17)

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
