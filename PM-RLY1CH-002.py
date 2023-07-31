# Example using PICO to drive a 1CH Relay.
# ProMake RPI PICO, Slot 3
# 1CH Relay v1.0

from machine import Pin, Timer
from time import sleep

 
O1 = machine.Pin(5 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-1


while(True):

    
    O1.value(1)
    sleep(1)
    O1.value(0)
    sleep(1)
 