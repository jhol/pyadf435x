#
## This file is part of the pyadf435x project.
##
## Copyright (C) 2017 Joel Holdsworth <joel@airwebreathe.org.uk>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##
import logging
import struct
import usb.core


logger = logging.getLogger(__name__)


class FX2:
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x0456, idProduct=0xb40d)

        if self.dev is None:
            raise ValueError('Device not found')

        self.dev.set_configuration()


    def set_regs(self, regs):
        for reg in regs:
            self.dev.ctrl_transfer(bmRequestType=0x40, bRequest=0xDD, wValue=0, wIndex=0,
                data_or_wLength=[(reg >> (8 * b)) & 0xFF for b in range(4)])


class BusPirate:
    """This interface communicates via serial port using the pyBusPirateLite
    module and translate the command in native SPI."""

    def __init__(self, device='/dev/ttyUSB0', baudrate=115200):
        """Initialize the interface for the Bus Pirate using "device"
        with the given "baudrate"."""
        from pyBusPirateLite.SPI import SPI

        self.spi = SPI(device, baudrate)

        # speed = 30kHz
        # polarity = idle low (default)
        # output clock edge = active to idle (default)
        # input sample phase = middle (default)
        # CS = /CS (default)
        # output type = normal

        self.spi.pins = SPI.PIN_POWER | SPI.PIN_CS | SPI.PIN_AUX
        self.spi.config = SPI.CFG_PUSH_PULL | SPI.CFG_CLK_EDGE
        self.spi.speed = '30kHz'

    def write_data(self, data):
        """Write a single integer value (4 bytes) into the SPI bus."""
        data = struct.pack('>I', data)
        logger.debug(['%02x' % d for d in data])
        self.spi.cs = True
        self.spi.transfer(data)
        self.spi.cs = False

    def set_regs(self, regs):
        for reg in regs:
            self.write_data(reg)
