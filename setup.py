# This file is part of the pyI2C_MP_USB project.
#
# Copyright(c) 2019-2021 Thomas Fischl (https://www.fischl.de)
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

from setuptools import setup

def readme():
    with open("README.rst") as f:
        return f.read()

setup(name='i2c_mp_usb',
      version='1.2',
      description='I2C-MP-USB - USB to I2C interface',
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5'
      ],
      url='https://github.com/EmbedME/pyI2C_MP_USB',
      author='Thomas Fischl',
      author_email='tfischl@gmx.de',
      license="LGPL-3.0",
      packages=['i2c_mp_usb'],
      install_requires=[
          'libusb1'
      ],
      zip_safe=False)
