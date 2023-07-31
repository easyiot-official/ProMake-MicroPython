# Example using PICO to drive a 1CH Relay.
# ProMake RPI PICO, Slot 3
# Basic TAG v1.0

from machine import Pin
import utime

from dht import DHT11, InvalidChecksum


# Wait 1 second to let the sensor power up
utime.sleep(1)

pin = Pin(5, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)
ldr = machine.ADC(26)

while True:
    try:
        print("Temperature: {}".format(sensor.temperature),"Humidity: {}".format(sensor.humidity),"Light: ",ldr.read_u16())
        #print("Humidity: {}".format(sensor.humidity))
        #print(ldr.read_u16())
    except InvalidChecksum:
        print("Checksum from the sensor was invalid")
    utime.sleep(1)
