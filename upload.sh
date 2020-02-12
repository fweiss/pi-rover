#!/bin/sh

scp -p src/main/*.py src/main/setup-bt.sh root@raspberrypi0-wifi.local:
scp -p src/main/robby/*.py root@raspberrypi0-wifi.local:robby
