# Example for micropython.org device, RP2040 PIO mode
# Connections:
# Pin # | HX711
# ------|-----------
# 12    | data_pin
# 13    | clock_pin
#

from hx711_pio import HX711
from machine import Pin
import time
from time import sleep

pin_OUT = Pin(3, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(2, Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT)

while True:
    hx711.tare()
    value = hx711.read()
    value = hx711.get_value()
    value2 = hx711.read_average()
    sleep(1)
    print(value2)