#RPI PICO ProMake Carrier Board
#LED Blink
#The LED will turn on for one second and then turn off for one second

from machine import Pin
from time import sleep

LED = Pin(25,Pin.OUT)

while True:
    LED.on()
    sleep(1)
    LED.off()
    sleep(1)