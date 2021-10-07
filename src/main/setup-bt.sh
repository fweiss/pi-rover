#! /bin/sh

# this ought to be done during system startup
# goal is the have hci0
/usr/bin/hciattach /dev/serial1 bcm43xx 921600 noflow -
hciconfig hci0 up
