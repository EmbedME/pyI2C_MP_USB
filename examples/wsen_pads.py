#!/usr/bin/env python

# Example: I2C_MP_USB reads Würth Elektronik absolute pressure sensor WSEN-PADS
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# WSEN-PADS Absolute Pressure Sensor
#     https://www.we-online.de/katalog/en/WSEN-PADS
#     Sensor: 2511020213301
#     Eval board: 2511223013391


from i2c_mp_usb import I2C_MP_USB as SMBus
import time

# device address 
address = 0x5d

bus = SMBus()

# read and check device id 
deviceId = bus.read_byte_data(address, 0x0f)
if deviceId != 0xb3:
    raise OSError('Pressure sensor not found')

# perform software reset
bus.write_byte_data(address, 0x11, 0x04)
time.sleep(0.5)

# setup: low noice, auto increment
bus.write_byte_data(address, 0x11, 0x12)
# setup: enable BDU, 50 Hz
bus.write_byte_data(address, 0x10, 0x4E)

try:
    while True:

        # wait some time
        time.sleep(0.5)

        # read out conversion results
        data = bus.read_i2c_block_data(address, 0x28, 5)

        # calculate pressure
        pressure = data[0] | (data[1] << 8) | (data[2] << 16)
        pressure = (pressure ^ 0x800000) - 0x800000
        pressure = pressure / 40960

        # calculate temperature
        temperature = data[3] | (data[4] << 8)
        temperature = (temperature ^ 0x8000) - 0x8000
        temperature = temperature / 100

        # print out result
        print('Temperature: {:0.2f} °C, Pressure: {:0.3f} kPa '.format(temperature, pressure))

except KeyboardInterrupt:
        pass

