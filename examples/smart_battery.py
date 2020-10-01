#!/usr/bin/env python

# Example: I2C_MP_USB reads smart battery data of notebook battery
#          (tested with Li-Ion 84Wh pack for ThinkPad X201)
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# Smart Battery Data Specification:
#     http://sbs-forum.org/specs/sbdat110.pdf

from i2c_mp_usb import I2C_MP_USB as SMBus

address = 0x0b

bus = SMBus()

temperature = bus.read_word_data(address, 0x08)
temperature = temperature / 10 - 273.15

voltage = bus.read_word_data(address, 0x09)
voltage = voltage / 1000

current = bus.read_word_data(address, 0x0a)
relativeStateOfCharge = bus.read_word_data(address, 0x0d)

print('Temperature (°C):          ', temperature)
print('Voltage (V):               ', voltage)
print('Current (mA):              ', current)
print('RelativeStateOfCharge (%): ', relativeStateOfCharge)

