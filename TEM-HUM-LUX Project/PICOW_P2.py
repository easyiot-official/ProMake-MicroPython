import machine
import urequests 
from machine import Pin , I2C
import network, time
import veml7700
import utime

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=10000)
veml = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)
analog_value = machine.ADC(28)
pin = Pin(0, Pin.OUT, Pin.PULL_DOWN)

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'LN97XA771MUS2UGL'  
 
ssid = 'TF-i60 G1-8064'
password = 'Gigapardaz@1024'

# ssid = 'ProMake-w'
# password = 'Madnet1313'
# Configure Pico W as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
 
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
     pass
print('network config:', sta_if.ifconfig())

#*******************************************************************************************************************************************

def sht20_temperature():
    """Obtain the temperature value of SHT20 module
    Return:Temperature
    """
    i2c.writeto(0x40,b'\xf3')                       # Write byte “0xf3” to address 0x40, SHT20
    time.sleep(.070)                                    # SHT20 measurement takes time, must wait
    t=i2c.readfrom(0x40, 2)                         # Read 2 bytes of data from the x40 address, SHT20
    return -46.86+175.72*(t[0]*256+t[1])/65535      # Perform temperature conversion processing on the read data T=-46.86+175.72*St/2^16
#*******************************************************************************************************************************************

def sht20_humidity():
    """Obtain the humidity value of SHT20 module
    Return:Humidity
    """
    i2c.writeto(0x40,b'\xf5')                       # Write byte “0xf5” to address 0x40, SHT20
    time.sleep(0.025)                                    # SHT20 measurement takes time, must wait
    t=i2c.readfrom(0x40, 2)                         # Read 2 bytes of data from the x40 address, SHT20
    return -6+125*(t[0]*256+t[1])/65535

#*******************************************************************************************************************************************


while True:
    
    time.sleep(10) 
    TempSensor=sht20_temperature()
    HumidSensor=sht20_humidity()
    lightSensor = veml.read_lux()
    gasSensor = analog_value.read_u16()     
    print("sht20 temperature: %0.1fC sht20 humidity: %0.1f%%  Lux_Value: %1d MQ_GAS Level: %0.1i" %(TempSensor,HumidSensor,lightSensor,gasSensor))

    Sensor_readings = {'field1':str(TempSensor), 'field2':str(HumidSensor),'field3':str(lightSensor), 'field4':str(gasSensor)} 
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = Sensor_readings, headers = HTTP_HEADERS )  
    request.close() 
    print(Sensor_readings) 