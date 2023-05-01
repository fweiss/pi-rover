import sys
import signal
import RPi.GPIO as GPIO
import time

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    left = LeftMotor()
    right = RightMotor()

    dir = 0
    while 1:
        left.direction(dir)
        right.direction(dir)
        for x in range(30):
            left.speed(x)
            right.speed(x)
            time.sleep(0.1)
        for x in range(30):
            left.speed(30-x)
            right.speed(30-x)
            time.sleep(0.1)
        dir = 0 if dir else 1

class Motor:
    def __init__(self):
        GPIO.setup(self.pwm, GPIO.OUT)
        GPIO.setup(self.fwd, GPIO.OUT)
        GPIO.setup(self.rev, GPIO.OUT)

        self.speed_range_low = 20
        self.speed_range_high = 50

        self.p = GPIO.PWM(self.pwm, 1000)
        self.p.start(0)
    def direction(self, rev):
        GPIO.output(self.fwd, GPIO.LOW if rev else GPIO.HIGH)
        GPIO.output(self.rev, GPIO.HIGH if rev else GPIO.LOW)
    def speed(self, speed):
        dc = self.speed_range_low + (speed / 100) * (self.speed_range_high - self.speed_range_low)
        self.p.ChangeDutyCycle(20 + speed)
        
class LeftMotor(Motor):
    def __init__(self):
        self.pwm = 19
        self.fwd = 26
        self.rev = 13
        super().__init__()

class RightMotor(Motor):
    def __init__(self):
        self.pwm = 18
        self.fwd = 24
        self.rev = 23
        super().__init__()

def interrupted(a, b):
    GPIO.cleanup()
    sys.exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, interrupted)
    main()
