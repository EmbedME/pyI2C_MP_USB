#!/usr/bin/env python

# Example: I2C_MP_USB reads adc ADS1015
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# ADS1015:
#     https://www.ti.com/product/ADS1015
# ADS1015 breakout board:
#     https://www.adafruit.com/product/1083


from i2c_mp_usb import I2C_MP_USB as SMBus
import time

# device address 
address = 0x4a # address pin connected to SDA

bus = SMBus()

# config adc: continuous conversion, AIN0, PGA=+/-6.144, 128 SPS
bus.write_i2c_block_raw(address, [0x01, 0x40, 0x00])

try:
    while True:

        # wait some time
        time.sleep(0.5)

        # read out adc result
        result = bus.read_i2c_block_data(address, 0x00, 2)

        # format adc result
        adc_result = (result[1] >> 4) | (result[0] << 4)
        if adc_result & 0x800 != 0:
            adc_result -= 1 << 12
        voltage = adc_result * 0.003  # 3mV @ +/-6.144

        # print out the result
        print('Voltage: {:0.3f} V '.format(voltage))

except KeyboardInterrupt:
        pass

