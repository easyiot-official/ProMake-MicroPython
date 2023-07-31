# This code run on ProMake PI PICO Kit HW REV 1.2,1.5
# Storage MB v1.1

import sdcard  
import machine  
import uos  
sd_spi = machine.SPI(0, sck = machine.Pin(6, machine.Pin.OUT), mosi = machine.Pin(7, machine.Pin.OUT), miso = machine.Pin(4, machine.Pin.IN))  
sd = sdcard.SDCard(sd_spi, machine.Pin(5))  
  
uos.mount(sd, "/sd")  
  
print("Size: {} MB".format(sd.sectors/2048)) # to display card's capacity in MB  
print(uos.listdir("/sd"))  
print("\n=======================\n")  
print("Basic SDcard Test \n")  
  
with open("/sd/test2.txt", "w") as f: # Write - new file  
    f.write("First Message\r\n")  
  
with open("/sd/test2.txt", "a") as f: # Append  
    f.write("Easy IOT Kits\r\n")  
  
with open("/sd/test2.txt", "a  ") as f:  
    f.write("First test SD Card!\r\n")  
      
with open("/sd/test2.txt", "a  ") as f:  
    for i in range(10):  
        f.write(str(i) + ", " + str(i*i*i) + ", " + str(i*i*i*i) + "\r\n")  
  
  
with open("/sd/test2.txt", "a  ") as f:  
    f.write("Looping all done!\r\n")  
          
with open("/sd/test2.txt", "r") as f:  
    print("Printing lines in file: Method #1\n")  
    line = f.readline()  
    while line != '':   # NOT EOF  
        print(line)  
        line = f.readline()  
  
  
with open("/sd/test2.txt", "r") as f:  
    lines = f.readlines()  
    print("Printing lines in file: Method #2")  
    for line in lines:  
        print(line)  
  
uos.umount("/sd")