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
import sys

vcc = 3.3#Volt. DAC can be used at 2.7V to 5.5V
# device address
address = 0x60
dest_dac = 0x40
dest_eeprom = 0x20


bus = SMBus()

# Read out DAC register and EEPROM data
rdata = bus.read_i2c_block_raw(address, 5)
print("DAC register and EEPROM data readout:",[hex(b) for b in list(rdata)])
dac = (rdata[1]<<4) + (rdata[2]>>4)
eeprom =(rdata[3]<<8) + rdata[4]
volt = dac * vcc /((1<<12)-1)
print(f"12 bit DAC at {hex(dac)} renders {volt:.2f} Volts")
volt = eeprom * vcc /((1<<12)-1)
print(f"12 bit EEPROM at {hex(eeprom)} renders {volt:.2f} Volts")

print("Set DAC and EEPROM to 0V")
bus.write_i2c_block_raw(address, [dest_dac+dest_eeprom, 0, 0, dest_dac+dest_eeprom, 0, 0])

# Give some time to measure voltage on connected multimeter
time.sleep(5)

print("Set DAC to maximum")
bus.write_i2c_block_raw(address, [dest_dac, 0xff, 0xff, dest_dac, 0xff, 0xff])

# Give some time to measure voltage on connected multimeter
time.sleep(5)

# Set DAC value to voltage

volt = 2.24
dacvalue = int(min(volt/vcc,1.0) * ((1<<12)-1))
print(f"Set DAC value {dacvalue:3x}" )
bus.write_i2c_block_raw(address, [dest_dac, dacvalue>>4  & 0xff, dacvalue<<4  & 0xff, dest_dac, dacvalue>>4  & 0xff, dacvalue<<4  & 0xff])
