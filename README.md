# pi-rover

A POC for robotic vehicle on Rasperry Pi Zero and Python

## Pi Zero W basics
Login via ssh:

``ssh pi:raspberry@raspberry.local``

## File sharing
In order to use IntelliJ on Mac, set up a share.

In Mac File Sharing > Options, need to:
 - allow RPI filder to be shared
 - allow user for Windows File Sharing

Tip: copy the following to /home/pi/connect-mac:

sudo mount -t cifs //Franks-MacBook-Pro.local/RPI Projects/RPI -o user=frankw,uid=pi

Determine OS X hostname: ``hostname -a``

Then on Pi, ls ~/Projects/RPI will show empty directories.

Then cd ~/Projects/RPI/pi-rover and the project directory.

Then python src/main/pan-tilt.py

## Hardware
- Raspberry Pi Zero W V1.1
- Kingston SDC4/16GB Micro SD card
- Sparkfun Pi Servo Shield - DEV-14328
- Pan-tilt kit
- Tower Pro Micro Servo SG90 9 g

### SG90 specs
5 V
20 ms (50 Hz) PWM base
Pulse width encoding:
1.0 ms: -90 degrees CCW (left)
1.5 ms: 0 degrees (middle)
2.0 ms: 90 degrees CW (right)

Note: The linearity of these cheap servos is very poor.

### PCA9685 specs
Designed for LED PWM control, but can be used for servo, for 16 output channels.
PWM control for each channel is 12-bit (4096 steps).

Drive capability at 5 V:
- 25 mA sink open drain/totem pole
- 10 mA source totem pole

Internal 25 MHz oscillator.
Power on reset sets output to LOW.


## Running pi-gpio
This is the gpio version.

Update on pi:

scp -r ./src pi@192.168.1.116:/home/pi/Projects/pi-rover

Shell into the pi
cd /home/pi/Projects/pi-rover
sudo pigpiod
python src/main/pi-pigpio.py

To stop: ctrl+c

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

http://www.techradar.com/how-to/computing/use-a-raspberry-pi-to-remotely-watch-your-home-1314466

https://raspberrypi.stackexchange.com/questions/23182/how-to-stream-video-from-raspberry-pi-camera-and-watch-it-live

v4l2-ctl --list-formats
Failed to open /dev/video0: No such file or directory

https://hackernoon.com/spy-your-pet-with-a-raspberry-pi-camera-server-e71bb74f79ea
http://192.168.1.1:8081/

uncomment:
/tmp/motion.log
error opening file /var/lib/motion/01-20180103043953.avi 
sudo chmod 777 /var/lib/motion
works, choppy, dies after a while

take 2 (motion)

sudo modprobe bcm2835-v4l2
sudo service motion start .
http://raspberrypi:8081

~1 fps
~2 sec lag

## Pan and tilt servos
sudo apt install python-smbus

sudo vi /boot/config.txt
sudo raspi-config
peripherals, enable i2c

http://www.instructables.com/id/How-to-share-files-between-Mac-OSX-and-Raspberry-P/

PWM prescale of 121 results in 54.6 Hz

## Bluetooth
Got a linux image with BT support baked with the yocto-pi-vm project.
Haven't been able to get hci0 up during startup, so added a script ``setup-bt.sh`` to run manually after boot.

The ``dbus-bt.py`` script successfully advertises, but not much else yet.

> The name is "TESTADVERTISEMENT"


## Notes

Not remote: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera

https://stackoverflow.com/questions/41351514/leadvertisingmanager1-missing-from-dbus-objectmanager-getmanagedobjects

https://github.com/luetzel/bluez/blob/master/test/example-advertisement

Get bluez version: ``bluetoothctl --version``, currently 5.5.0

Get example code, including python/dbus, from the bluez repo in kernel.org: https://git.kernel.org/pub/scm/bluetooth/bluez.git
