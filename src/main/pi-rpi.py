import RPi.GPIO as gpio
import time

gpio.setwarnings(False)

gpio.setmode(gpio.BCM)
gpio.setup(19, gpio.OUT)

p = gpio.PWM(19, 1000)
p.start(50)

while 1:
    for x in range(50):
        p.ChangeDutyCycle(x)
        print(x)
        time.sleep(0.1)
    for x in range(50):
        p.ChangeDutyCycle(50-x)
        print(50-x)
        time.sleep(0.1)
