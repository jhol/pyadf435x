#!/usr/bin/env python3

import adf435x.interfaces
from adf435x import calculate_regs, make_regs
import time

intf = adf435x.interfaces.FX2()

while True:
    for freq in range(50, 100):
        INT, MOD, FRAC, output_divider, band_select_clock_divider = \
                calculate_regs(freq=freq)
        regs = make_regs(INT=INT, MOD=MOD, FRAC=FRAC,
                output_divider=output_divider,
                band_select_clock_divider=band_select_clock_divider)
        intf.set_regs(regs[::-1])
        print('%0.1fMHz' % freq)
        time.sleep(0.1)
