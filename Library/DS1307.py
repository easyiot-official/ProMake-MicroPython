from machine import I2C, Pin
import ds1307
i2c = I2C(0) # SCL=A8, SDA=C9
i2c.scan()
ds = ds1307.DS1307(i2c)
ds.datetime()

print(ds)