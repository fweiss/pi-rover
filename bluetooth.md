bluetoothctl

On Jessie

hciconfig
shows the info for hci0

then
sudo hcitool -i hci0 cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 00 00 c5 00 00 00 00 00 00 00 00 00 00 00 00 00

or truncated

then sudo hciconfig hci0 leadv 0

then android scan blue1 shows

B8:27:eb:cb:10:bb: bcm43438a1

also note
lsmod: rfcomm, hci_uart, btbcm, etc

there's no /dev/rfcomm
