#!/bin/sh

TARGET=root@raspberrypi0-wifi.local

ssh $TARGET mkdir robby util
scp -p src/main/*.py src/main/setup-bt.sh $TARGET:
scp -p src/main/robby/*.py $TARGET:robby
scp -p src/util/*.py $TARGET:util
