# Example using PIO to drive a Isolated GPIO.
# ProMake RPI PICO, Slot 3
# GAS MQ ver1.2
import machine
import utime
 
analog_value = machine.ADC(26)
 
while True:
    reading = analog_value.read_u16()     
    print("ADC: ",reading)
    utime.sleep(0.8)