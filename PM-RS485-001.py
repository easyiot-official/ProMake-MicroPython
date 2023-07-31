# Example using PIO to drive a Isolated GPIO.
# ProMake RPI PICO, Slot 3
# RS485 V1.1
'''
 ##@name：		RS485_send.py
 ##@auther:		waveshare team
 ##@info:		This code has configured a serial port of Pico to connect to our PICO-2CH-RS485, 
			which will continuously emit an incremental data.	
'''
from machine import UART, Pin
import time


uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart1 = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

RX_DIR = machine.Pin(19 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-1
TX_DIR = machine.Pin(5 , machine.Pin.OUT , machine.Pin.PULL_UP) # Isolated Output-1
TX_DIR.value(1)
RX_DIR.value(0)

a=0
txData = b'RS485 send test...\r\n'
uart0.write(txData)
print('RS485 send test...')
time.sleep(0.1)


while True:
    a=a+1
    time.sleep(0.5) 
    uart0.write("{}\r\n".format(a))
    
    rxData = bytes()
    while uart1.any() > 0:
        rxData = uart1.read()
        try:
            print('TX:',a,'RX:',rxData.decode('utf_8'))
        except OSError:
            print("Something else went wrong")
