#!/usr/bin/python3

import sys
sys.path.insert(0, '.')

from robby.pan_tilt import PanTilt

import time
import smbus

def main():
    # FIXME move to pan_tilt
    I2C_BUS_NUMBER = 1

    # with none of the 6 address jumpers closed, base address is
    # 1 0 0 0 0 0 0 W
    # except that library manages W bit
    addr = 0x40

    bus = smbus.SMBus(I2C_BUS_NUMBER)

    adapter = PanTilt(bus, addr)
    adapter.initialize_channels()

    path0 = [
        [ -30, 20 ],
        [ 50, 10 ],
        [ 150, 100 ],
        # [ 250, 0 ],
        [ 50, 20 ],
        [ -130, 80 ],
        [ 200, 80 ],
        [ 150, 20 ]
    ]

    while True:
        for (pan, tilt) in path0:
            adapter.moveTo(pan, tilt)
            time.sleep(.4)

if __name__ == '__main__':
    main()

