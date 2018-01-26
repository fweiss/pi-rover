https://github.com/Multibit-Legacy/trezorj/wiki/Configuring-Intellij-to-use-Python-and-deploy-to-the-Raspberry-Pi

RPi.GPIO uses software PWM

https://rpitips.com/python-libraries-pigpio/

## Wiring
On Pi Zero, the two outermost pins near the SD card are +5V

CK1122 to Pi Zero

| GND | BLACK  | GND06  |
| +5V | RED    | 5V02   |
| IN1 | ORANGE | GPIO26 |
| ENA | YELLOW | GPIO19 |
| IN2 | GREEN  | GPIO13 |
| CSA | BLUE   | NC     |
| IN3 | VIOLET | GPIO23
| ENB | GRAY   | GPIO18 |
| IN4 | WHITE  | GPIO24 |
| CSB | BROWN  | NC     |

## Running pi-gpio
sudo pigpiod
python src/main/pi-rover.py

## Raspberry Pi
Well, it's kind of neat to have a full OS, but there are some downsides:

- long boot time (not really long, but too many seconds)
- not a real time OS (maybe there are variants)
- hardware PWM may require low-level language support

## Motors with PWM
I got generic motors, but they look like DAGU

The gear train is a bit noisy.

### PWM frequncies
Initally tried 100 Hz with python pigpio.

| 100 | maybe a bit of dwell at low, can hear the buzz at low values, some glitches |
| 1000 | high pitched, doesn't reach full speed |
| 500 | like 1000 |
| 27 | rough, glitched are more pronounced |
| 200 | like 100 |

## Camera

Not remote: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera

http://www.techradar.com/how-to/computing/use-a-raspberry-pi-to-remotely-watch-your-home-1314466

https://raspberrypi.stackexchange.com/questions/23182/how-to-stream-video-from-raspberry-pi-camera-and-watch-it-live

v4l2-ctl --list-formats
Failed to open /dev/video0: No such file or directory

https://hackernoon.com/spy-your-pet-with-a-raspberry-pi-camera-server-e71bb74f79ea
http://192.168.1.1:8081/

With motion, do get a frame after sudo modprobe bcm2835-v4l2, but then motion crashes. No log messages.

uncomment:
/tmp/motion.log
error opening file /var/lib/motion/01-20180103043953.avi 
sudo chmod 777 /var/lib/motion
works, choppy, dies after a while
