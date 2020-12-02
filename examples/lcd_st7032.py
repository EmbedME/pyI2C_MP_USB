#!/usr/bin/env python

# Example: I2C_MP_USB controls 8x2 LCD with ST7032 controller
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# 8x2 character display ERC802FS-1
#     https://www.buydisplay.com/serial-cog-8x2-lcd-module-i2c-character-display-st7032-black-on-white


from i2c_mp_usb import I2C_MP_USB as SMBus
import time

address = 0x3e
bus = SMBus()

def lcd_init():
   # initialize display for 5V (sequence comes from the manufacturer's demo code)
   bus.write_i2c_block_data(address, 0x80, [0x38, 0x80, 0x39, 0x80, 0x1c, 0x80, 0x78, 0x80, 0x53, 0x80, 0x6c, 0x80, 0x0c, 0x80, 0x01, 0x80, 0x06, 0x80, 0x02])
   return

def lcd_putch(c):
   bus.write_byte_data(address, 0xc0, ord(c))
   return

def lcd_puts(s):
   for c in s:
       lcd_putch(c)
   return

def lcd_goto(adr):
   bus.write_byte_data(address, 0x80, 0x80 + adr)
   return


lcd_init()
lcd_goto(0)
lcd_puts("I2CMPUSB")
lcd_goto(0x40)
lcd_puts("  Demo  ")


