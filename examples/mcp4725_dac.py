#!/usr/bin/env python

# Example: I2C_MP_USB communicates with DAC MCP4725.
#     Read DAC register and EEPROM data, set some DAC voltage levels.
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# MCP4725:
#     https://www.microchip.com/wwwproducts/en/en532229


from i2c_mp_usb import I2C_MP_USB as SMBus
import time

# device address 
address = 0x60

bus = SMBus()

# Read out DAC register and EEPROM data
rdata = bus.read_i2c_block_raw(address, 5)
print("DAC register and EEPROM data readout:")
print(rdata)

print("Set DAC to 0V")
bus.write_i2c_block_raw(address, [0x00, 0x00])

# Give some time to measure voltage on connected multimeter
time.sleep(5)

print("Set DAC to maximum")
bus.write_i2c_block_raw(address, [0x0f, 0xff])

# Give some time to measure voltage on connected multimeter
time.sleep(5)

# Set any DAC value
dacvalue = int(0xfff / 3);
print("Set DAC value ", dacvalue)
bus.write_i2c_block_raw(address, [(dacvalue >> 8) & 0xff, dacvalue & 0xff])


