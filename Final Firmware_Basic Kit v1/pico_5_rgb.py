#RPI PICO ProMake Carrier Board
#Control WS2812B RGB LED 

import time
from neopixel import Neopixel
 
LED_NUM = 2
LED_PIN = 14

pixels = Neopixel(LED_NUM , LED_PIN , "GRB")
 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

COLOR = [BLACK , RED , YELLOW , GREEN , CYAN , BLUE , PURPLE , WHITE]
pixels.brightness(100)


while True:

    for color in COLOR:
        
        pixels.set_pixel(0, color)
        pixels.set_pixel(1, color)
        pixels.show()
        time.sleep(0.2)
    
    for i in range(len(COLOR)-1):
        
        pixels.set_pixel(0, COLOR[i])
        pixels.set_pixel(1, COLOR[i+1])
        pixels.show()
        time.sleep(0.2)