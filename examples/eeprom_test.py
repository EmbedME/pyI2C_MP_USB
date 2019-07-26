#!/usr/bin/env python

import time
from i2c_mp_usb import I2C_MP_USB as SMBus

bus = SMBus()

# Set 100kHz baudrate
bus.set_baudrate(100)

# Write one byte to address 0x10 of an EEPROM 24C02
bus.write_byte_data(0x50, 0x10, 0xA5)

# Give the EEPROM time to flash the written value
time.sleep(0.1)

# Read one byte from address 0x10 of an EEPROM 24C02
data = bus.read_byte_data(0x50, 0x10)

print(hex(data))
