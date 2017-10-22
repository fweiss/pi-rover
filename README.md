https://github.com/Multibit-Legacy/trezorj/wiki/Configuring-Intellij-to-use-Python-and-deploy-to-the-Raspberry-Pi

RPi.GPIO uses software PWM

https://rpitips.com/python-libraries-pigpio/

## Wiring
On Pi Zero, the two outermost pins near the SD card are +5V

| GND | PURPLE | GND39  | GND14  |
| +5V |
| IN1 | GREEN  | GPIO26 | GPIO23 |
| ENA | YELLOW | GPIO19 | GPIO18 |
| IN2 | ORANGE | GPIO13 | GPIO24 |
| CSA |
| IN3 |
| ENB |
| IN4 |
| CSB |

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

