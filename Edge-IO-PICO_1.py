################################################
# This Program is written by Giga Pardaz PARS
# Edge-IO-PICO

from machine import Pin, I2C, PWM, Timer , UART
import time
from utime import sleep

##################################################
#time.sleep(0.05)
i2c = I2C(0, sda=Pin(16), scl=Pin(17),freq = 100000)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
LED = machine.Pin(25,machine.Pin.OUT)



Buzzer = PWM(Pin(20))
Buzzer.freq(3000)



PCA9555_I2C_ADDRESS             = 0x20
PCA9555_CMD_Output             = b'\x00'
PCA9555_CMD_Input              = b'\xFF'
PCA9555_Output_FF              = b'\xFF'
PCA9555_Output_00              = b'\x00'

pca9555_IN0_REG  = const(0x00) #Input register
pca9555_IN1_REG  = const(0x01) #Input register

pca9555_OUT0_REG = const(0x02) #Output register
pca9555_OUT1_REG = const(0x03) #Output register

pca9555_POL0_REG = const(0x04) #Polarity inversion register (1=data inverted)
pca9555_POL1_REG = const(0x05) #Polarity inversion register (1=data inverted)

pca9555_DIR0_REG = const(0x06) #Config register (0=output, 1=input)
pca9555_DIR1_REG = const(0x07) #Config register (0=output, 1=input)


Relay_1_ON = b'\xFE' #const(0xFE)
Relay_2_ON = b'\xFD' #const(0xFD)
Relay_3_ON = b'\xFB' #const(0xFB)
Relay_4_ON = b'\xF7' #const(0xF7)
Relay_5_ON = b'\xEF' #const(0xEF)
Relay_6_ON = b'\xDF' #const(0xDF)

MSG_LED_ON = const(0x7F)
###############################################################################

def handle_interrupt(Pin):           #defining interrupt handling function
    global Control
    if Control =="Auto":
        Control ="Manual"
    else:
        Control ="Auto"
    print("Intrupt",Control)
    
KEY_Interrupt=Pin(20,Pin.IN)   # setting GPIO20 INT-IO_Interrupt as input

#Attach external interrupt to GPIO15 and rising edge as an external event source
KEY_Interrupt.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

###############################################################################

#i2c.writeto_mem(PCA9538_I2C_ADDRESS, pca9538_OUT_REG , Forward_All_Motor)
   
###############################################################################
     
def setup():
    i2c.writeto_mem(PCA9555_I2C_ADDRESS , pca9555_DIR0_REG , PCA9555_CMD_Output )         # write to 0X20 (PCA9555 Add)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS , pca9555_DIR1_REG , PCA9555_CMD_Output )         # write to 0X20 (PCA9555 Add) 

    i2c.writeto_mem(PCA9555_I2C_ADDRESS , pca9555_OUT0_REG , PCA9555_Output_FF )
    #time.sleep_us(5)
    #distance()
    print('Setup Done.',' Ya Mahdi.')
###############################################################################
#timer=Timer(-1)
#timer2=Timer(-1)
#timer.init(period=100, mode=Timer.PERIODIC,callback=lambda t: distance())
#timer2.init(period=1000, mode=Timer.PERIODIC,callback=lambda t: print('Distance:' ,dist,' Obstacle:',Obstacle,' Run:',run,'Last_Dir:',last_dir,'Control:',Control))  
###############################################################################
    
setup()
Relay_Array = [Relay_1_ON,Relay_2_ON,Relay_3_ON,Relay_4_ON,Relay_5_ON,Relay_6_ON]
while(True):
           
    #for i in range(len (Relay_Array)):
     #   c = b'Relay_Array[i]'
    #print(i,Relay_Array[i],c)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS, pca9555_OUT0_REG , Relay_1_ON)
    sleep(1)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS, pca9555_OUT0_REG , Relay_2_ON)
    sleep(1)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS, pca9555_OUT0_REG , Relay_3_ON)
    sleep(1)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS, pca9555_OUT0_REG , Relay_4_ON)
    sleep(1)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS, pca9555_OUT0_REG , Relay_5_ON)
    sleep(1)
    i2c.writeto_mem(PCA9555_I2C_ADDRESS, pca9555_OUT0_REG , Relay_6_ON)
    sleep(1)