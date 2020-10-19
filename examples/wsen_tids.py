#!/usr/bin/env python

# Example: I2C_MP_USB reads Würth Elektronik temperature sensor WSEN-TIDS
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# WSEN-TIDS Temperatur Sensor IC
#     https://www.we-online.de/katalog/de/WSEN-TIDS
#     Sensor: 2521020222501
#     Eval board: 2521020222591


from i2c_mp_usb import I2C_MP_USB as SMBus
import time

# device address 
address = 0x38 #SA0 pin high
#address = 0x3F #SA0 pin low

bus = SMBus()

# read and check device id 
deviceId = bus.read_byte_data(address, 0x01)
if deviceId != 0xa0:
    raise OSError('Temperature sensor not found')

# perform software reset
bus.write_byte_data(address, 0x0C, 0x02) # set
bus.write_byte_data(address, 0x0C, 0x00) # release

# setup: enable BDU, 25 Hz, auto increment, continous mode
bus.write_byte_data(address, 0x04, 0x4C)

try:
    while True:

        # wait some time
        time.sleep(0.5)

        # read out temperature
        temperature = bus.read_word_data(address, 0x06)

        # temperature is given as 16-bit signed2’s complement word. convert it
        temperature = (temperature ^ 0x8000) - 0x8000

        # print out the result
        print('Temperature in °C: ', 0.01 * temperature)

except KeyboardInterrupt:
        pass

