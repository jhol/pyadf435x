#!/usr/bin/env python3

import usb.core

dev = usb.core.find(idVendor=0x0456, idProduct=0xb40d)

if dev is None:
    raise ValueError('Device not found')

dev.set_configuration()

dev.ctrl_transfer(bmRequestType=0x40, bRequest=221, wValue=0, wIndex=0,
        data_or_wLength=[0x00, 0x00, 0x32, 0x00])
