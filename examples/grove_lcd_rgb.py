#!/usr/bin/env python

# Example: I2C_MP_USB with Grove LCD-RGB
#
# I2C_MP_USB:
#     https://www.fischl.de/i2c-mp-usb/
# Grove - LCD RGB Backlight:
#     https://www.seeedstudio.com/Grove-LCD-RGB-Backlight.html

from i2c_mp_usb import I2C_MP_USB as SMBus
import time

REG_RED = 0x04
REG_GREEN = 0x03
REG_BLUE = 0x02     

REG_MODE1 = 0x00
REG_MODE2 = 0x01
REG_OUTPUT = 0x08

LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_FUNCTIONSET = 0x20
LCD_DISPLAYCONTROL =0x08
LCD_SETLINE2 = 0xC0

LCD_2LINE = 0x08

LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

bus = SMBus()

def lcd_command(command):
    bus.write_byte_data(0x3e, 0x80, command)

def lcd_write(value):
    bus.write_byte_data(0x3e, 0x40, value)

def lcd_setReg(address, value):
    bus.write_byte_data(0x62, address, value)

def lcd_setRGB(r, g, b):
    lcd_setReg(REG_RED, r)
    lcd_setReg(REG_GREEN, g)
    lcd_setReg(REG_BLUE, b)

def lcd_init():
    lcd_command(LCD_FUNCTIONSET | LCD_2LINE)
    time.sleep(0.1)
    lcd_command(LCD_FUNCTIONSET | LCD_2LINE)
    time.sleep(0.1)
    lcd_command(LCD_FUNCTIONSET | LCD_2LINE)

    lcd_command(LCD_FUNCTIONSET | LCD_2LINE)
    lcd_command(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF)
    lcd_command(LCD_CLEARDISPLAY)
    lcd_command(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT)


    lcd_setReg(REG_MODE1, 0)
    lcd_setReg(REG_OUTPUT, 0xFF)
    lcd_setReg(REG_MODE2, 0x20)
    lcd_setRGB(0x00, 0x00, 0x00)

    lcd_command(LCD_RETURNHOME);

def lcd_setLineText(text, line):

    if line == 2:
        lcd_command(LCD_SETLINE2)
    else:
        lcd_command(LCD_RETURNHOME)

    for c in text:
        lcd_write(ord(c))

def lcd_setText(text):
    lines = text.split("\n", 2)
    if len(lines) >= 1:
        lcd_setLineText(lines[0] + ' ' * (16 - len(lines[0])), 1)
    if len(lines) == 2:
        lcd_setLineText(lines[1] + ' ' * (16 - len(lines[1])), 2)

lcd_init()
lcd_setRGB(0x00, 0xFF, 0x00)
lcd_setText('Grove - LCD RGB\nwith I2C_MP_USB')
