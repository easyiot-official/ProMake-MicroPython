#RPI PICO ProMake Carrier Board
#Control LED brightness with PWM


from machine import Pin, PWM
from utime import sleep

LED = PWM(Pin(25))
LED.freq(1000)

while True:
    
    for duty in range(65535):
        LED.duty_u16(duty)
        sleep(0.0003)

    for duty in range(65535, 0, -1):
        LED.duty_u16(duty)
        sleep(0.0003)
    sleep(0.5) 