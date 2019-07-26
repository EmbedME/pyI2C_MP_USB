# This file is part of the pyI2C_MP_USB project.
#
# Copyright(c) 2019 Thomas Fischl (https://www.fischl.de)
# 
# pyI2C_MP_USB is free software: you can redistribute it and/or modify
# it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyI2C_MP_USB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
# along with pyI2C_MP_USB.  If not, see <http://www.gnu.org/licenses/>

import libusb1
import usb1

CMD_ECHO = 0
CMD_GET_FUNC = 1
CMD_SET_DELAY = 2
CMD_GET_STATUS = 3
CMD_I2C_IO = 4
CMD_I2C_IO_BEGIN = 1
CMD_I2C_IO_END = 2
CMD_START_BOOTLOADER = 0x10
CMD_SET_BAUDRATE = 0x11

I2C_M_RD = 0x01

I2C_MP_USB_VID = 0x0403
I2C_MP_USB_PID = 0xc631

class I2C_MP_USB(object):

    def __init__(self, serialnumber = None):
        """
        Initialize and open connection to I2C_MP_USB.
        :param serialnumber: USB serial number
        :type serialnumber: string
        """

        self.usbdev = self.get_usb_device(serialnumber)
        if self.usbdev is None:
            raise I2C_MP_USBNotFoundException()

        self.usbhandle = self.usbdev.open()
        self.usbhandle.claimInterface(0)

    def get_usb_device(self, serialnumber = None):
        """
        Get USB device matching VID and PID and if given also check the USB serial number.
        :rtype: USBDeviceHandle
        :param serialnumber: USB serial number
        :type serialnumber: string       
        """
        ctx = usb1.LibUSBContext()

        for device in ctx.getDeviceIterator():
            if device.getVendorID() == I2C_MP_USB_VID and device.getProductID() == I2C_MP_USB_PID:
                if serialnumber is None:
                    return device
                elif device.getSerialNumber() == serialnumber:
                    return device        

    def read_byte(self, i2c_addr):
        """
        Read a single byte from a device.
        :rtype: int
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :return: Read byte value
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN, 0, i2c_addr, [])
            data = self.usbhandle.controlRead(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_END, I2C_M_RD, i2c_addr, 1)
            return data[0]
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()


    def read_byte_data(self, i2c_addr, register):
        """
        Read a single byte from a designated register.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param register: Register to read
        :type register: int
        :return: Read byte value
        :rtype: int
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN, 0, i2c_addr, [register])
            data = self.usbhandle.controlRead(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_END, I2C_M_RD, i2c_addr, 1)
            return data[0]
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()


    def read_word_data(self, i2c_addr, register):
        """
        Read a single word (2 bytes) from a given register.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param register: Register to read
        :type register: int
        :return: 2-byte word, little endian
        :rtype: int
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN, 0, i2c_addr, [register])
            data = self.usbhandle.controlRead(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_END, I2C_M_RD, i2c_addr, 2)
            return data[0] | (data[1] << 8)
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()


    def read_i2c_block_data(self, i2c_addr, register, length):
        """
        Read a block of byte data from a given register.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param register: Start register
        :type register: int
        :param length: Desired block length
        :type length: int
        :return: List of bytes
        :rtype: list
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN, 0, i2c_addr, [register])
            data = self.usbhandle.controlRead(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_END, I2C_M_RD, i2c_addr, length)
            return data
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()



    def write_byte(self, i2c_addr, value):
        """
        Write a single byte to a device.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param value: value to write
        :type value: int
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN + CMD_I2C_IO_END, 0, i2c_addr, [value])
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()


    def write_byte_data(self, i2c_addr, register, value):
        """
        Write a byte to a given register.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param register: Register to write to
        :type register: int
        :param value: Byte value to transmit
        :type value: int
        :rtype: None
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN + CMD_I2C_IO_END, 0, i2c_addr, [register, value])
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()

    def write_word_data(self, i2c_addr, register, value):
        """
        Write a byte to a given register.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param register: Register to write to
        :type register: int
        :param value: Word value to transmit, little endian
        :type value: int
        :rtype: None
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN + CMD_I2C_IO_END, 0, i2c_addr, [register, value & 0xff, (value >> 8) & 0xff])
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()


    def write_i2c_block_data(self, i2c_addr, register, data):
        """
        Write a block of byte data to a given register.
        :param i2c_addr: i2c address
        :type i2c_addr: int
        :param register: Start register
        :type register: int
        :param data: List of bytes
        :type data: list
        :rtype: None
        """
        try:
            self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_I2C_IO + CMD_I2C_IO_BEGIN + CMD_I2C_IO_END, 0, i2c_addr, [register] + data)
        except usb1.USBErrorPipe:
            raise I2C_MP_USBTransmitException()


    def set_baudrate(self, baudrate):
        """
        Set I2C baudrate in kHz
        :param baudrate: I2C clock frequency in kHz
        :type period: int
        """
        self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_SET_BAUDRATE, baudrate, 0, [])        

    def start_bootloader(self):
        """
        Jump to bootloader.
        """
        self.usbhandle.controlWrite(libusb1.LIBUSB_TYPE_CLASS, CMD_START_BOOTLOADER, 0x5237, 0, [])        


class I2C_MP_USBException(Exception):
    def __init__(self):
        Exception.__init__(self)

class I2C_MP_USBNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self)

class I2C_MP_USBTransmitException(Exception):
    def __init__(self):
        Exception.__init__(self)

