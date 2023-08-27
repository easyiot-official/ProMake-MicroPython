#RPI PICO ProMake Carrier Board
#Control WS2812B RGB LED 

import machine
import utime
 
analog_value = machine.ADC(26)
 
while True:
    reading = analog_value.read_u16()     
    print("ADC: ",reading)
    utime.sleep(0.8)