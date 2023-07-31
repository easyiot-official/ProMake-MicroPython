from machine import Pin , PWM
from utime import sleep

led = Pin(25,Pin.OUT)
ina1 = Pin(5,Pin.OUT)
ina2 = Pin(26, Pin.OUT)
pwma = PWM(Pin(2))
pwma.freq(10000)

inb1 = Pin(0,Pin.OUT)
inb2 = Pin(1, Pin.OUT)
pwmb = PWM(Pin(3))
pwmb.freq(10000)



led.toggle()


def RotateCW(duty):
    ina1.value(1)
    ina2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)

    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwmb.duty_u16(duty_16)
    
def RotateCCW(duty):
    ina1.value(0)
    ina2.value(1)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty*65536)/100)
    pwmb.duty_u16(duty_16)
    
def StopMotor():
    ina1.value(0)
    ina2.value(0)
    pwma.duty_u16(0)
    inb1.value(0)
    inb2.value(0)
    pwmb.duty_u16(0)

#duty_cycle=float(input("Enter pwm duty cycle"))
#duty_cycle= 100
for i in range(101):
    print ("Duty Cycle",i)
    RotateCW(i)
    sleep(0.1)
    if i == 100:
        sleep(5)
StopMotor()    
for j in range(101):
    print ("Duty Cycle",j)
    RotateCCW(j)
    sleep(0.1)
    if j == 100:
        sleep(5)
StopMotor()