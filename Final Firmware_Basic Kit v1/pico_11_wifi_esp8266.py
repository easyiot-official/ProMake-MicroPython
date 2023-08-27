#RPI PICO ProMake Carrier Board
#Interfacing rpi PICO with ESP8266

from machine import Pin, UART
import utime


AP = "SSID"
PASS = "PASSWORD"


uart0 = UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1), bits=8, parity=None, stop=1)
esp_reset = Pin(22, machine.Pin.OUT)

#*******************************************************************************************************************************************
def Rx_ESP_Data():
    recv=bytes()
    while uart0.any()>0:
        recv+=uart0.read(1)
    res=recv.decode('utf-8')
    return res
#*******************************************************************************************************************************************
def Connect_WiFi(cmd, uart=uart0, timeout=3000):
    uart.write(cmd)
    utime.sleep(7.0)
    Wait_ESP_Rsp(uart, timeout)
#*******************************************************************************************************************************************
def Send_AT_Cmd(cmd, uart=uart0, timeout=3000):
    uart.write(cmd)
    Wait_ESP_Rsp(uart, timeout)
#*******************************************************************************************************************************************    
def Wait_ESP_Rsp(uart=uart0, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])

    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)   
#*******************************************************************************************************************************************

print("=== Start ===")

#hardware reset ESP
print("Hardware reset")
print()
esp_reset.value(1)
utime.sleep(0.5)
esp_reset.value(0)
utime.sleep(0.5)
esp_reset.value(1)

Send_AT_Cmd('AT\r\n')          #Test AT startup
Send_AT_Cmd('AT+GMR\r\n')      #Check version information
#Send_AT_Cmd('AT+RESTORE\r\n')  #Restore Factory Default Settings

Send_AT_Cmd('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode

preScanTime = utime.ticks_ms()
Send_AT_Cmd('AT+CWLAP\r\n', timeout=10000)  #List Available APs
print("Time used to Scan AP: ",
      utime.ticks_diff(utime.ticks_ms(), preScanTime),
      "(ms)")

Connect_WiFi('AT+CWJAP="'+ AP +'","' + PASS + '"\r\n', timeout=5000) #Connect to AP
Send_AT_Cmd('AT+CIFSR\r\n',timeout=5000)    #Obtain the Local IP Address

print ('ESP8266 Configuration is done.')

