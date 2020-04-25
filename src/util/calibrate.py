#!/usr/bin/python3

import sys
sys.path.insert(0, '.')

from robby.pan_tilt import PanTilt

import time
import smbus
import threading
import tty

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

    task = threading.Thread(target=run, args=(adapter,))
    # task.start()
    # time.sleep(2)

    calibrate(adapter)

    x.join()

def calibrate(adapter):
    #     adapter.setBias([ 200, 200 ])
    print("use WASD keys to move arm")
    while True:
        #         cmd = input("{},{}:".format(pan, tilt))
        (pan, tilt) = adapter.bias
        print("bias: {},{}:".format(pan, tilt))
        cmd = getChr()
        print("\n")
        if cmd == "w":
            tilt -= 1
        if cmd == "a":
            pan -= 1
        if cmd == "s":
            tilt += 1
        if cmd == "d":
            pan += 1
        adapter.setBias([ pan, tilt ])
        adapter.moveTo(0, 0)

def run(adapter):
    while True:
        tilt = 0
        adapter.moveTo(-150, tilt)
        time.sleep(2)
        adapter.moveTo(0, tilt)
        time.sleep(2)
        adapter.moveTo(150, tilt)
        time.sleep(2)

def getChr():
    tty.setraw(sys.stdin.fileno())
    chr = sys.stdin.read(1)
    sys.stdout.write("\r")
    if ord(chr) == 3: # ETX
        exit(1)
    return chr

if __name__ == '__main__':
    main()

