# Example using PICO to drive a 2CH Relay.
# ProMake RPI PICO, Slot 3
# 2ch Relay v1.1
from machine import Pin, Timer
from time import sleep

 
O1 = machine.Pin(5 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-1
O2 = machine.Pin(2 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-2


while(True):

    
    O1.value(1)
    sleep(1)
    O1.value(0)
    sleep(1)
 
    O2.value(1)
    sleep(1)
    O2.value(0)
    sleep(1)

