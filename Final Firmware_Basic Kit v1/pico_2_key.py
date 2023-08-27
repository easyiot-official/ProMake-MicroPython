#RPI PICO ProMake Carrier Board
#LED Control By Key
#The LED will turn on and off by pressing KEY(GP15) on ProMake PICO Carrier 

from machine import Pin
from utime import sleep

KEY = machine.Pin(15, machine.Pin.IN)
LED = machine.Pin(25,machine.Pin.OUT)

while True:
    
    if KEY.value() == 0: # KEY Pressed
        
        LED.on()
    
    else:
        
        LED.off()