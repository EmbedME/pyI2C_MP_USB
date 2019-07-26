#!/usr/bin/env python

from i2c_mp_usb import I2C_MP_USB

imu = I2C_MP_USB()
imu.start_bootloader()
