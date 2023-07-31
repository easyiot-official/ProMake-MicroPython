# Example using PIO to drive a Isolated GPIO.
# ProMake RPI PICO, Slot 3
# Isolated GPIO V1.0

from machine import Pin, Timer,I2C,ADC
from time import sleep
from neopixel2 import Neopixel
 
numpix = 2
pixels = Neopixel(numpix, 0, 14, "GRB")
 
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
Off =(0,0,0)
color0 = red
color0 = yellow
color1 = red
pixels.brightness(200)

I1 = machine.Pin(28 , machine.Pin.IN , machine.Pin.PULL_UP) # Isolated Input-1
I2 = machine.Pin(18 , machine.Pin.IN , machine.Pin.PULL_UP) # Isolated Input-2

O1 = machine.Pin(13 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-1
O2 = machine.Pin(12 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-2


while(True):
    if I1.value()==0:
        print('I1 triged.' ,I1.value())
        pixels.set_pixel(1, Off)
        pixels.set_pixel(0, green)
        pixels.show()
        sleep(0.1)
    elif I2.value()==0:
        print('I2 triged.' ,I2.value())
        pixels.set_pixel(0, Off)
        pixels.set_pixel(1, green)
        pixels.show()
        sleep(0.1)
    else:    
        pixels.set_pixel(0, Off)
        pixels.set_pixel(1, Off)
        pixels.show()
        sleep(0.1)
    
    O1.value(1)
    O2.value(1)
    sleep(.2)
    O1.value(0)
    O2.value(0)
    sleep(.2)
 
