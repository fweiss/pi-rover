import sys
import signal
import time
import pigpio

pi = pigpio.pi()

PIN_PWM_A = 19
PIN_FWD_A = 26
PIN_REV_A = 13

pi.set_mode(PIN_PWM_A, pigpio.OUTPUT)
pi.set_mode(PIN_FWD_A, pigpio.OUTPUT)
pi.set_mode(PIN_REV_A, pigpio.OUTPUT)

def interrupted(a, b):
    pi.set_mode(PIN_PWM_A, pigpio.INPUT)
    pi.set_mode(PIN_FWD_A, pigpio.INPUT)
    pi.set_mode(PIN_REV_A, pigpio.INPUT)
    pi.stop()
    sys.exit()

signal.signal(signal.SIGINT, interrupted)

def direction(fwd):
    pi.write(PIN_FWD_A, 1 if fwd else 0)
    pi.write(PIN_REV_A, 0 if fwd else 1)

pi.set_PWM_frequency(PIN_PWM_A, 200)
dir = 1

while True:
    direction(dir)
    dir = 0 if dir else 1
    for i in range(5, 100, 5):
        pi.set_PWM_dutycycle(PIN_PWM_A, i)
        time.sleep(0.1)
    for i in range(100, 5, -5):
        pi.set_PWM_dutycycle(PIN_PWM_A, i)
        time.sleep(0.1)
