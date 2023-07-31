################################################
# This Program is written by Giga Pardaz PARS
# Relay 8CH v1.1

from machine import Pin,I2C
import time
from utime import sleep

##################################################
#time.sleep(0.05)
i2c = I2C(0, sda=Pin(16), scl=Pin(17),freq = 100000)
KEY = machine.Pin(15, machine.Pin.IN)


PCA9554_I2C_ADDRESS             = 0x38
PCA9554_CMD_Output             = b'\x00'
PCA9554_CMD_Input            = b'\xFF'
PCA9554_Output_FF            = b'\xFF'
PCA9554_Output_00            = b'\x00'

PCA9554_IN_REG= const(0x00) #Input register
PCA9554_OUT_REG = const(0x01) #Output register
PCA9554_POL_REG = const(0x02) #Polarity inversion register (1=data inverted)
PCA9554_DIR_REG = const(0x03) #Config register (0=output, 1=input)

Relay_1_ON = b'\xFE' #const(0xFE)
Relay_2_ON = b'\xFD' #const(0xFD)
Relay_3_ON = b'\xFB' #const(0xFB)
Relay_4_ON = b'\xF7' #const(0xF7)
Relay_5_ON = b'\xEF' #const(0xEF)
Relay_6_ON = b'\xDF' #const(0xDF)
Relay_7_ON = b'\xBF' #const(0xDF)
Relay_8_ON = b'\x7F' #const(0xDF)

Control ="All"
###############################################################################
def handle_interrupt(Pin):           #defining interrupt handling function
    global Control
    if Control =="All":
        Control ="Single"
    else:
        Control ="All"
    print("Intrupt",Control)
    
KEY_Interrupt=Pin(15,Pin.IN)   # setting GPIO15 PIR_Interrupt as input
#Attach external interrupt to GPIO15 and rising edge as an external event source
KEY_Interrupt.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
############################################################################### 
def setup():
    i2c.writeto_mem(PCA9554_I2C_ADDRESS , PCA9554_DIR_REG , PCA9554_CMD_Output )         
    i2c.writeto_mem(PCA9554_I2C_ADDRESS , PCA9554_OUT_REG , PCA9554_Output_FF )
    time.sleep_us(5)
    print('Setup Done.')
###############################################################################
    
setup()
Relay_Array = [Relay_1_ON,Relay_2_ON,Relay_3_ON,Relay_4_ON,Relay_5_ON,Relay_6_ON]

while(True):
    if Control == "Single":
    #for i in range(4):    
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_1_ON )
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_2_ON)
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_3_ON)
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_4_ON)
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_5_ON)
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_6_ON)
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_7_ON)
        sleep(1)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , Relay_8_ON)
        sleep(1)
        
    if Control == "All":
       
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , PCA9554_Output_00)
        sleep(2)
        i2c.writeto_mem(PCA9554_I2C_ADDRESS, PCA9554_OUT_REG , PCA9554_Output_FF)
        sleep(2)

