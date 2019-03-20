#!/usr/bin/python3

import time
import smbus

I2C_BUS_NUMBER = 1

# with none of the 6 address jumpers closed, base address is
# 1 0 0 0 0 0 0 W
# except that library manages W bit
addr = 0x40

bus = smbus.SMBus(I2C_BUS_NUMBER)

def main():  
    initialize_channels()
    adapter = PanTilt(bus, addr)
    
    interactive(adapter)
#     steps(adapter)
#     sweep(adapter)


MODE1 = 0x00
MODE1_LOW_POWER = 0x10
MODE1_AUTO_INCREMENT = 0x20

MODE2 = 0x01
MODE2_OUT_TOTEM = 0x04

PRE_SCALE = 0xfe

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
    def moveTo(self, pan, tilt):
        global PAN_REG_OFF, PAN_REG_ON, TILT_REG_ON, TILT_REG_OFF
        self.bus.write_word_data(self.addr, PAN_REG_ON, 0)
        self.bus.write_word_data(self.addr, PAN_REG_OFF, self.mapPan(pan))
        self.bus.write_word_data(self.addr, TILT_REG_ON, 0)
        self.bus.write_word_data(self.addr, TILT_REG_OFF, self.mapTilt(tilt))
    def mapPan(self, pan):
        return pan + 260;
    def mapTilt(self, tilt):
        return tilt + 350

def initialize_channels():
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

def steps(adapter):
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
    while True:
        for (pan, tilt) in path:
#             print("{}: {}".format(pan, tilt))
            adapter.moveTo(pan, tilt)
            time.sleep(.2)
            
def sweep(adapter):
    while True:
        for pan in range(80, 320):
            print("pan: {}".format(pan))
            adapter.moveTo(pan, 0)
            time.sleep(.1)
        for tilt in range(200,450):
            print("tilt: {}".format(pan))
            adapter.moveTo(0, tilt)
            time.sleep(.1)

main()
