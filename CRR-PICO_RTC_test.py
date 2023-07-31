################################################
# This Program is written by Giga Pardaz PARS
# PICO ROBOT Slot 3
# PICO With RTC
import time
from neopixel2 import Neopixel 
from machine import Pin, I2C, PWM
from time import sleep
import ssd1306
import pcf8563
import machine , time
from ssd1306 import SSD1306_I2C
import framebuf,sys
#import ds1307
#########################################################################################################################################
#########################################################################################################################################
i2c = I2C(0, sda=Pin(16), scl=Pin(17),freq = 100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)
IR = machine.Pin(10, machine.Pin.IN)
KEY = machine.Pin(15, machine.Pin.IN)
LED = machine.Pin(14,machine.Pin.OUT)
Buzzer = PWM(Pin(11))
Buzzer.freq(3000)
#########################################################################################################################################
#########################################################################################################################################

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    
#########################################################################################################################################
pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 32   # SSD1306 vertical resolution
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c) # oled controller
oled.fill(0) # clear the OLED
start_x = 0 # start point for text in x-dir
start_y = 2 # start point for text in y-dir
lineskip = 20 # space between text in y-dir
#########################################################################################################################################

numpix = 2
pixels = Neopixel(numpix, 0, 14, "GRB")
 
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0,0,0)
white = (255,255,255)
COLORS = (white,red, yellow, green, blue, white,black)

color0 = red

######################################################################################################################################## 
def pixels_fill(color):
    
    if color == 'Blink':
        print("fills")
        for color in COLORS:
            pixels.set_pixel(0, color)
            pixels.set_pixel(1, color)
            pixels.show()
            time.sleep(0.5)
    if color == 'Error':
            pixels.set_pixel(0, red)
            pixels.set_pixel(1, red)
            pixels.show()
            time.sleep(0.1)        
    if color == 'Off':
            pixels.set_pixel(0, black)
            pixels.set_pixel(1, black)
            pixels.show()
            time.sleep(0.1)
#########################################################################################################################################
def rtc_show(NowCount):
    try:
        
        #ds = ds1307.DS1307(i2c)
        r = pcf8563.PCF8563(i2c)

        real_time = r.datetime()  ;print(real_time)     
        Year = real_time[0]; Month = real_time[1]; Day = real_time[2]; Hour = real_time[4]; Minute = real_time[5]; Second = real_time[6]
        txt_array1 = [str(real_time[0])+str(real_time[1])+str(real_time[2])+' '+ str(real_time[4])+':'+str(real_time[5])+':'+str(real_time[6]),'RTC Test PICO'] # text array

        for iter_ii,txt in enumerate(txt_array1):
            oled.text(txt,start_x,start_y+(iter_ii*lineskip)) # add text at (start_x,start_y)

        oled.show() # show the new text and image
        oled.contrast(255) # increase brightness
        time.sleep(.5)
        oled.invert(0)
        oled.fill(0) # #  clear the OLED
        pixels_fill('Off')
        
    except:
        oled.fill(0)
        txt_array2 = ['00:00:00','Error Read RTC'] # text array
        for iter_ii,txt in enumerate(txt_array2):
            oled.text(txt,start_x,start_y+(iter_ii*lineskip)) # add text at (start_x,start_y)
        oled.show() # show the new text and image
        time.sleep(.1)
        oled.invert(0) # invert the colors from dark -> light, and light -> dark       
        pixels_fill('Error')
        print('Error on read RTC')
        pass
    
   # print('NowCount: ',NowCount)
    return NowCount 
#########################################################################################################################################

pixels.brightness(100)
pixels.fill(orange)
NowTime_set = 0
Buzzer.duty_u16(30000)
time.sleep(0.1)
Buzzer.deinit()

while(True):
    
    if NowTime_set == 0:
       # ds = ds1307.DS1307(i2c)
        r = pcf8563.PCF8563(i2c)

        #NowTime_set  = 1
        now = (2022, 7, 28, 1,5, 1, 0)
       # r.datetime(now)
        
   
    rtc_show(NowTime_set)
    time.sleep(0.7)    
    if KEY.value() == 0: # KEY Pressed
        
        Buzzer.freq(1000)
        display.text('KEY Pressed',0,10,1)
        display.show()
        Buzzer.duty_u16(40000) 
        sleep(0.2)
        display.fill(0)
        display.show()
        Buzzer.deinit()
        pixels_fill('Blink')
        
        
    if IR.value() == 3:
        print('IR: ', IR.value())
        Buzzer.freq(100)
        display.text('IR Rrcieved',0,10,1)
        display.show()
        #Buzzer.toggle()
        Buzzer.duty_u16(30000)
        #LED.toggle()
        sleep(.1)
        display.fill(0)
        display.show()
        Buzzer.freq(5000)
        sleep(.1)
        Buzzer.deinit()
        
#########################################################################################################################################
