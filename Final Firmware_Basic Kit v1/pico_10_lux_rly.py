#This code run on ProMake PI PICO Kit HW REV 1.2
#For getting data from SHT20 and VEML7700(Light Sensor)
# PM-RLY :Slot1

from machine import Pin, I2C,ADC
from time import sleep
import ssd1306
import veml7700


i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=10000)
O1 = machine.Pin(5 , machine.Pin.OUT , machine.Pin.PULL_UP) # Relay Output

try:
    veml = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)
    print("Ligt Sensor VEML7700 is founded.")
    
except:
    print("Ligt Sensor VEML7700 not found.")


while True:

    lux_val = veml.read_lux()   
   # print("Lux_Value: %1d" %(lux_val))
    
    sleep(0.5)
    
    if (lux_val< 50):
        
        print("Ambient light is not enough.")
        print("Lux_Value: %1d" %(lux_val))
        O1.value(1)
        
    elif (lux_val > 500):
        
        print("Ambient light is sufficient")
        print("Lux_Value: %1d" %(lux_val))
        O1.value(0)

