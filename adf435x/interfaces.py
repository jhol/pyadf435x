#!/usr/bin/env python3

import usb.core

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
