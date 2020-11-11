#!/usr/bin/env python

# Example: I2C_MP_USB reads Würth Elektronik humidity sensor WSEN-HIDS
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# WSEN-HIDS Humidity Sensor with integrated Temperature Sensor
#     https://www.we-online.de/katalog/en/WSEN-HIDS
#     Sensor: 2525020210001
#     Eval board: 2525020210091


from i2c_mp_usb import I2C_MP_USB as SMBus
import time

# read 16-bit value and convert it into signed value (2's complement)
def readS16(bus, address, register):
    w = bus.read_word_data(address, register | 0x80)
    return (w ^ 0x8000) - 0x8000

# device address 
address = 0x5F

bus = SMBus()

# read and check device id 
deviceId = bus.read_byte_data(address, 0x0f)

if deviceId != 0xbc:
    raise OSError('Sensor not found')

# read humidity calibration values
H0_rH_x2 = bus.read_byte_data(address, 0x30)
H1_rH_x2 = bus.read_byte_data(address, 0x31)

H0_rH = H0_rH_x2 / 2
H1_rH = H1_rH_x2 / 2

H0_T0_OUT = readS16(bus, address, 0x36)
H1_T0_OUT = readS16(bus, address, 0x3A)

# read temperature calibration values
T0_degC_x8 = bus.read_byte_data(address, 0x32)
T1_degC_x8 = bus.read_byte_data(address, 0x33)
T1_T0 = bus.read_byte_data(address, 0x35)
T0_degC_x8 = T0_degC_x8 | ((T1_T0 & 0x3) << 8)
T1_degC_x8 = T1_degC_x8 | ((T1_T0 & 0xC) << 6)
T0_degC = T0_degC_x8 / 8
T1_degC = T1_degC_x8 / 8

T0_OUT = readS16(bus, address, 0x3C)
T1_OUT = readS16(bus, address, 0x3E)


# setup: enable operation mode, enable BDU, data rate 7 Hz
bus.write_byte_data(address, 0x20, 0x86)


try:
    while True:

        # wait some time
        time.sleep(0.5)

        # read out raw humidity
        H_T_OUT = readS16(bus, address, 0x28)

        # calculate humidity
        humidity = ((H1_rH - H0_rH) * (H_T_OUT - H0_T0_OUT)) / (H1_T0_OUT - H0_T0_OUT)
        humidity = humidity + H0_rH

        # read raw temperature value
        T_OUT = readS16(bus, address, 0x2A)

        # calculate temperature
        temperature = ((T1_degC - T0_degC) * (T_OUT - T0_OUT)) / (T1_OUT - T0_OUT)
        temperature = temperature + T0_degC

        # print out result
        print('Temperature: {:0.2f} °C, Humidity: {:0.2f} % '.format(temperature, humidity))


except KeyboardInterrupt:
        pass

