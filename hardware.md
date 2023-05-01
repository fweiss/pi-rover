# Hardware

## PCA9685 16-channel servo driver

https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf

## Canakit UK1122 dual motor control

Jumper J1

- Recommended position "A" supplies the LM298 with internal regulator power.
- Position "B" uses offboard power +5 V and disables the internal regulator.

> With 6 AA batteries, the onboard regulator cannot supply steady +5 V
> when the motors are activated. See Issues.

## Motor chassis
Raspberry Pi Zero
Canakit UK1122
motors
switch
battery pack

UK1122 - Wire - RPIZ - GPIO - FW
--------------------------------
GND - BLK - 6
+5  - RED - 2
IN1 - ORG - 37 - (26) - PIN_FWD_A
ENA - YEL - 35 - (19) PWM1 - PIN_PWM_A
IN2 - GRN - 33 - (13) - PIN_REV_A
CSA - NC
IN3 - VIO - 16 - (23) - PIN_REV_B
ENB - GRY - 12 - (18) PWM0 - PIN_PWM_B
IN4 - WHT - 18 - (24) - PIN_FWD_B
CSB - NC

- Note RPIZ pin 1 nearest HDMI
- Outer - even, inner - odd
- Note REV/FWD reversed on channel B, as the motors are 180 degrees
- Channel A left motors, channel B right motors

## TT motor
https://www.adafruit.com/product/3777

Operating voltage: 3V to 12V DC (recommended operating voltage of about 6 to 8V)
Maximum torque: 800gf cm min (when it is 3V)
No-load speed: 1:48 (when it is 3V)
Load current: 70mA (250mA MAX) (when it is 3V)
This motor with EMC, anti-interference ability. SCM is a non-interference. EMC contrast with the general Canadian EMC\'s current is too large, the impact of robot operation, the MCU does not often work.

## Issues

### no connect/other flakiness
- 5 V to RPI was dropping below 3.3 V
- battery was 6.88 V no load
- battery dropped below 5 V under load
- fresh batteries, solid 8 V

## Preserved

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

> The linearity of these cheap servos is very poor.

### PCA9685 specs
Designed for LED PWM control, but can be used for servo, for 16 output channels.
PWM control for each channel is 12-bit (4096 steps).

Drive capability at 5 V:
- 25 mA sink open drain/totem pole
- 10 mA source totem pole

Internal 25 MHz oscillator.
Power on reset sets output to LOW.

