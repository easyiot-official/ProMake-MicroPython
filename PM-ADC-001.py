# This code run on ProMake PI PICO Kit HW REV 1.2,1.5
# ADC 4CH v1.0

from machine import I2C, Pin, Timer
import ads1x15
from array import array
from time import sleep

addr = 72
gain = 1
_BUFFERSIZE = const(10)

data = array("h", (0 for _ in range(_BUFFERSIZE)))
i2c = machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))


ads = ads1x15.ADS1115(i2c, addr, gain)
#
# Interrupt service routine for data acquisition
# activated by a pin level interrupt
#
def sample_auto(x, adc = ads.alert_read, data = data):
    global index_put
    if index_put < _BUFFERSIZE:
        data[index_put] = adc()
        index_put += 1

index_put = 0

irq_pin = Pin(13, Pin.IN, Pin.PULL_UP)
#ads.conversion_start(5, 0) #Rate Channel0,1,2,3

irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=sample_auto)

while True :
    #sample_auto(0)
    ads.conversion_start(5, 0)
    CH0= ads.alert_read()
    sleep(0.1)
    
    ads.conversion_start(5, 1)
    CH1= ads.alert_read()
    sleep(0.1)
    
    ads.conversion_start(5, 2)
    CH2= ads.alert_read()
    sleep(0.1)
    
    ads.conversion_start(5, 3)
    CH3= ads.alert_read()
    sleep(0.1)
   
    print('CH0:',CH1,'CH1:',CH2,'CH2:',CH3,'CH3:',CH0)
    

