#!/usr/bin/python3

import time
import smbus
import tty
import sys

I2C_BUS_NUMBER = 1

# with none of the 6 address jumpers closed, base address is
# 1 0 0 0 0 0 0 W
# except that library manages W bit
addr = 0x40

bus = smbus.SMBus(I2C_BUS_NUMBER)

def main():
    try: 
        adapter = PanTilt(bus, addr)
        adapter.initialize_channels()

        #     interactive(adapter)
        # steps(adapter)
        sweep(adapter)
    #     calibrate(adapter)
    except KeyboardInterrupt as err:
        bus.write_byte_data(addr, MODE2, 0) # hi-z

MODE1 = 0x00
MODE1_LOW_POWER = 0x10
MODE1_AUTO_INCREMENT = 0x20

MODE2 = 0x01
MODE2_OUT_TOTEM = 0x04

# 0xFE = ~18 ms
PRE_SCALE = 0xfe

# PCA9685 "LED" registers
PAN_REG_ON = 0x06
PAN_REG_OFF = 0x08
TILT_REG_ON = 0x0a
TILT_REG_OFF = 0x0c

PWM_200HZ = 30
PWM_50HZ = 121 # (25000000 / (4096 * 50)) - 1

# for SC90, the PWM values are:
#  -90 1.0 ms 1.0*4096/20 205
#    0 1.5 ms 1.5*4096/20 307
#  +90 2.0 ms 2.0*4096/20 410

class PanTilt:
    def __init__(self, bus, addr):
        self.bus = bus
        self.addr = addr
#         self.bias = [ 250, 300 ]
        self.bias = [ 190, 357 ]
#         self.bias = [ 0, 357 ]
#         self.bias = [ 210, 128 ]
    def setBias(self, bias):
        self.bias = bias
    def writeWord(self, register, value):
        self.bus.write_word_data(self.addr, register, value)
    def moveTo(self, pan, tilt):
        global PAN_REG_OFF, PAN_REG_ON, TILT_REG_ON, TILT_REG_OFF
        print("move: {} {}".format(pan, tilt))
        self.writeWord(PAN_REG_ON, 0)
        self.writeWord(PAN_REG_OFF, self.mapPan(pan))
        self.writeWord(TILT_REG_ON, 0)
        self.writeWord(TILT_REG_OFF, self.mapTilt(tilt))
    def mapPan(self, pan):
        return pan + self.bias[0];
    def mapTilt(self, tilt):
        return tilt + self.bias[1]
    def initialize_channels(self):
        print(bus.read_byte_data(addr, MODE1))
        print(bus.read_byte_data(addr, MODE2))

        bus.write_byte_data(addr, MODE1, 0x10)
        bus.write_byte_data(addr, PRE_SCALE, PWM_50HZ)
        bus.write_byte_data(addr, MODE1, MODE1_AUTO_INCREMENT) # because we'll be using bus.write.word_data

        print(bus.read_byte_data(addr, MODE1))

        bus.write_byte_data(addr, MODE2, MODE2_OUT_TOTEM)

def pulse_width(off):
    start = bus.read_word_data(addr, PAN_REG_ON)
    stop = bus.read_word_data(addr, PAN_REG_OFF)
    duty = (stop - start) / 4096.0
    prescale = bus.read_byte_data(addr, PRE_SCALE)
    osc_clock = 25000000.0
    pwm_freq = osc_clock / 4096.0 / (1.0 + prescale)
    pulse_width_ms = duty / pwm_freq * 1000.0
    return pulse_width_ms

def interactive(adapter):
    while True:
        cmd = input("Enter pan, tilt (0-4095): ")
        [ pan, tilt ] = map(int, cmd.strip().split(","))
        adapter.moveTo(pan, tilt)

def calibrate(adapter):
#     adapter.setBias([ 200, 200 ])
    pan = 0
    tilt = 0
    print("use WASD keys to move arm")
    while True:
        adapter.moveTo(pan,tilt)
#         cmd = input("{},{}:".format(pan, tilt))
        print("{},{}:".format(pan, tilt))
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
#         adapter.setBias([ pan, tilt ])
        
def steps(adapter):
#     adapter.setBias([ 0, 0 ])
    path = [ 
        [ 220, 320 ], 
        [ 300, 400 ], 
        [ 400, 400 ], 
        [ 500, 300 ], 
        [ 300, 320 ], 
        [ 120, 380 ], 
        [ 650, 380 ], 
        [ 400, 320 ] 
    ]
    path0 = [
        [ -30, 20 ], 
        [ 50, 10 ], 
        [ 150, 100 ], 
        [ 250, 0 ], 
        [ 50, 20 ], 
        [ -130, 80 ], 
        [ 400, 80 ], 
        [ 150, 20 ] 
    ]
    path4 = [
        [ 0, 0 ],
        [ -100, 0 ],
        [ 100, 0 ],
        [ 0, 100 ],
        [ 0, -100 ]
    ]
    while True:
        for (pan, tilt) in path0:
            adapter.moveTo(pan, tilt)
            time.sleep(.4)

# 0.336 ms = 75 ticks
# 1.336 ms = 299
def sweep(adapter):
    interval = 0.001
    adapter.setBias([ 225, 0 ])
    base = 18.28 / 4096 # ms/tick
    def servoRange(min, max):
        return range(int(min / base), int(max / base))
    # panRange = servoRange(0.336, 1.336)
    # panRange = range(75-225, 375-225)
    panRange = range(-150, 150)
    # panRange = range( -150, 150 )
    tiltRange = servoRange(0, 2)
    def sweepRange(r):
        for pan in r:
            adapter.moveTo(pan, 0)
            time.sleep(interval)
        for pan in reversed(r):
            adapter.moveTo(pan, 0)
            time.sleep(interval)

    while True:
        sweepRange(panRange)

def getChr():
    tty.setraw(sys.stdin.fileno())
    chr = sys.stdin.read(1)
    sys.stdout.write("\r")
    if ord(chr) == 3: # ETX
        exit(1)
    return chr

if __name__ == '__main__':
    main()

