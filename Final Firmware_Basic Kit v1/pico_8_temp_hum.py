#RPI PICO ProMake Carrier Board
#Receiving temperature and Humidity by Sensor TAG Module

from machine import Pin, I2C, ADC
from utime import sleep


i2c = I2C(0, scl=Pin(17), sda=Pin(16))

#########################################################################################################################################
def sht20_temperature():
    """Obtain the temperature value of SHT20 module
    Return:Temperature
    """
    i2c.writeto(0x40,b'\xf3')                       # Write byte “0xf3” to address 0x40, SHT20
    sleep(0.070)                                    # SHT20 measurement takes time, must wait
    t=i2c.readfrom(0x40, 2)                         # Read 2 bytes of data from the x40 address, SHT20
    return -46.86+175.72*(t[0]*256+t[1])/65535      # Perform temperature conversion processing on the read data T=-46.86+175.72*St/2^16
#########################################################################################################################################

def sht20_humidity():
    """Obtain the humidity value of SHT20 module
    Return:Humidity
    """
    i2c.writeto(0x40,b'\xf5')                       # Write byte “0xf5” to address 0x40, SHT20
    sleep(0.025)                                    # SHT20 measurement takes time, must wait
    t=i2c.readfrom(0x40, 2)                         # Read 2 bytes of data from the x40 address, SHT20
    return -6+125*(t[0]*256+t[1])/65535             # Perform humidity conversion processing on the read data RH=-6+125*Srh/2^16
#########################################################################################################################################

while True:
    
    temper=sht20_temperature()
    humid=sht20_humidity() 
    print("sht20 temperature: %0.1fC sht20 humidity: %0.1f%% " %(temper,humid))
    sleep(1)


