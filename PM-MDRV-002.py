################################################
# This Program is written by Giga Pardaz PARS
# PICO ROBOT Slot 3
# MB MDRV M2 DC Motor

from machine import Pin, I2C, PWM
import time
from utime import sleep

##################################################

i2c = I2C(0, sda=Pin(16), scl=Pin(17),freq = 100000)

KEY = machine.Pin(15, machine.Pin.IN)
LED = machine.Pin(25,machine.Pin.OUT)

pwma = PWM(Pin(2))
pwmb = PWM(Pin(3))
pwma.freq(25000)
pwmb.freq(25000)

#Buzzer = PWM(Pin(20))
#Buzzer.freq(3000)

PCA9538_I2C_ADDRESS             = 0x73
PCA9538_CMD_Output              = b'\x00'
Stop_All_Motor                  = b'\x00'      
Forward_All_Motor               = b'\x15'
Backwrad_All_Motor              = b'\x1A'
Turn_Right                      = b'\x16'
Turn_Left                       = b'\x19'
pca9538_IN_REG  = const(0x00) #Input register
pca9538_OUT_REG = const(0x01) #Output register
pca9538_POL_REG = const(0x02) #Polarity inversion register (1=data inverted)
pca9538_DIR_REG = const(0x03) #Config register (0=output, 1=input)

###############################################################################
def forward(speed):
    i2c.writeto_mem(PCA9538_I2C_ADDRESS, pca9538_OUT_REG , Forward_All_Motor)
    duty_16 = int((speed*60000)/100)
    pwmb.duty_u16(duty_16)
    pwma.duty_u16(duty_16)
    time.sleep_us(5)

###############################################################################
def backward(speed):   
    i2c.writeto_mem(PCA9538_I2C_ADDRESS, pca9538_OUT_REG , Backwrad_All_Motor )
    duty_16 = int((speed*65536)/100) 
    pwmb.duty_u16(duty_16)
    pwma.duty_u16(duty_16)
    time.sleep_us(5)
###############################################################################
def stop_motor():
    i2c.writeto_mem(PCA9538_I2C_ADDRESS, pca9538_OUT_REG , Stop_All_Motor )
    time.sleep_us(5)
###############################################################################
     
def setup():
    i2c.writeto_mem(PCA9538_I2C_ADDRESS , pca9538_DIR_REG , PCA9538_CMD_Output )         # write to 0X73 (PCA9538 Add) 
    i2c.writeto_mem(PCA9538_I2C_ADDRESS , pca9538_OUT_REG , Stop_All_Motor )
    print('setup done.')
###############################################################################
    
setup()

for x in range(1,100,10):
    forward(x)
    sleep(1)
       
stop_motor()
sleep(.4)

for y in range(1,100,10):
    backward(y)
    sleep(.4)

stop_motor()    
print('Done')
        
