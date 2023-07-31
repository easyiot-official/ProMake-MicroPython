"""
Raspberry Pi Pico/MicroPython + ESP-C3-12F exercise

ESP-C3-12F with AT-command firmware:
AT version:2.2.0.0(s-90458f0 - ESP32C3 - Jun 18 2021 10:24:22)

Scan Access Point
"""

import usys, uos
import machine
import utime
import gc
import urequests
# 
AP = "TF-i60 G1-8064"
PASS = "Gigapardaz@1024"

# AP = 'Rauof'
# PASS = '0987654321@0987654321'
# AP = 'Mdgo'
# PASS = 'md6dast@'


class color:
    BLACK =   '\033[1;30;48m'
    RED =     '\033[1;31;48m'
    GREEN =   '\033[1;32;48m'
    YELLOW =  '\033[1;33;48m'
    BLUE =    '\033[1;34;48m'
    MAGENTA = '\033[1;35;48m'
    CYAN =    '\033[1;36;48m'
    END =     '\033[1;37;0m'

print("====================================")
print(usys.implementation[0], uos.uname()[3],
      "\nrun on", uos.uname()[4])
print("------------------------------------")


esp_reset = machine.Pin(22, machine.Pin.OUT)

#uart_esp =machine.UART(0, timeout=1000)
uart_esp = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1), bits=8, parity=None, stop=1)
#uart_esp = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1), bits=8, parity=None, stop=1)


#print("UART(0) connected to ESP: \n", uart_esp, "\n")

#==================================
"""
esp_sendCMD_waitResp: send comand to ESP, and wait response
if targetResp catched, return True
otherwise return False
"""
def esp_sendCMD_waitResp(cmd, uart=uart_esp, timeout=2000, targetResp="OK"):
    print(color.MAGENTA + cmd + color.END)
    print(uart_esp)
    uart.write(cmd)
    return esp_waitResp(uart, timeout, targetResp)

"""
esp_waitResp: wait ESP response
if targetResp catched, return True
otherwise return False
"""
def esp_waitResp(uart=uart_esp, timeout=2000, targetResp="OK"):
    targetCatched = False
    prvMills = utime.ticks_ms()
    print(color.BLUE)
    while (utime.ticks_diff(utime.ticks_ms(), prvMills))<timeout:
        line=uart.readline()
        if line is not None:
            try:
                line_decoded = line.strip().decode()
                if line_decoded == targetResp:
                    print(color.GREEN + line_decoded)
                    targetCatched = True
                    break
                
                #more checking for Response
                elif line_decoded == "OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "ERROR":
                    print(color.RED + line_decoded)
                    break
                
                elif line_decoded == "SEND OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "SEND FAIL":
                    print(color.RED + line_decoded)
                    break
                
                else:
                    print(line_decoded)
            except UnicodeError:
                print(line)
    
    print(color.END)
    return targetCatched

# In my test there are something
# like "################################################"
# follow ready of AT+RST/AT+RESTORE or hardware reset,
# Just dummy wait response to clear it
def esp_waitDummtResp(uart=uart_esp, timeout=2000):
    esp_waitResp(uart=uart_esp, timeout=2000)

#A dummy infinity loop
#to monitor any data sent from ESP via UART
def esp_dummyMonitor(uart=uart_esp):
    while True:
        line=uart.readline()
        if line is not None:
            try:
                line_decoded = line.strip().decode()
                print(line_decoded)
            except UnicodeError:
                print(line)
                
def Internet_connection():
    
        try:
            response = urequests.get("http://clients3.google.com/generate_204")
            print(response.status_code)
            if response.status_code == 204:
                print("online")
            elif response.status_code == 200:
                print("portal")
                #Connect_WiFi('AT+CWJAP="Rauof","0987654321@0987654321"\r\n', timeout=5000) #Connect to AP

            else:
                print("offline")
                #Connect_WiFi('AT+CWJAP="Rauof","0987654321@0987654321"\r\n', timeout=5000) #Connect to AP

        except:
            print("error")
           # Connect_WiFi('AT+CWJAP="Rauof","0987654321@0987654321"\r\n', timeout=5000) #Connect to AP

        gc.collect()
#==================================

print()
print("=== Start ===")

#hardware reset ESP
print("Hardware reset")
esp_reset.value(1)
utime.sleep(0.5)
esp_reset.value(0)
utime.sleep(0.5)
esp_reset.value(1)

print("wait 'ready' from Hardware Reset\n")
esp_waitResp(targetResp='ready')
esp_waitDummtResp()

esp_sendCMD_waitResp('AT\r\n')          #Test AT startup
esp_sendCMD_waitResp('AT+RESTORE\r\n')

#uart_esp =machine.UART(0, timeout=1000)



esp_sendCMD_waitResp('AT+GMR\r\n')      #Check version information


esp_waitResp(targetResp='ready')    #wait ready
esp_waitDummtResp()

esp_sendCMD_waitResp('AT+CIPAPMAC?\r\n')  #Query MAC address of ESP SoftAP
esp_sendCMD_waitResp('AT+CIPSTAMAC?\r\n') #Query MAC address of ESP station

esp_sendCMD_waitResp('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode
esp_sendCMD_waitResp('AT+CWMODE?\r\n')  #Query the Wi-Fi mode again

preScanTime = utime.ticks_ms()
esp_sendCMD_waitResp('AT+CWLAP\r\n', timeout=10000)  #List Available APs
print("Time used to Scan AP: ",
      utime.ticks_diff(utime.ticks_ms(), preScanTime),
      "(ms)")




esp_sendCMD_waitResp('AT+UART_DEF=9600,8,1,0,0\r\n')
uart_esp = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1), bits=8, parity=None, stop=1)

esp_sendCMD_waitResp('AT\r\n')          #Test AT startup
esp_sendCMD_waitResp('AT+CWJAP="' +AP+'","' +PASS+'"'+'\r\n', timeout=5000) #Connect to AP
esp_sendCMD_waitResp('AT+CIFSR\r\n')    #Obtain the Local IP Address

Internet_connection()
print("\n~ bye ~\n");
Internet_connection()

