bluez is the standard bluetooth stack for linux

two kinds of stacks?
- /dev/rfcomm
- dbus

Python code

## Setting up RPIZW
goal: advertise

install some dependencies?

use bluetoothctl

> list
controller address name MISSING
> agent on
> default-agent
> version
Version 5.43

also hciconfig does not list anything, expecting hci0



Or hcitool?

### Jessie
hook up via hdmi/usb
ssh in wireless

> hciconfig
hci0: Type primary bus uart
bd address: B8:27:EB:CB:10:BB
> rfkill list
phy0, hci0

> hcitool -i hci0 cmd 0x08 0x0008 12 11 07 9E CA DC 24 0E E5 A9 E0 93 F3 A3 B5 01 00 40 8E 00 00 00 00 00 00 00 00 00 00 00 00 00
> hcitool -i hci0 cmd 0x08 0x0006 00 08 00 08 00 00 00 00 00 00 00 00 00 07 00
> hcitool -i hci0 cmd 0x08 0x000A 01

verify with nrf connect - works "BlueZ 5.43"

### yocto wifi
Success with simple advertising

> rfkill
phy0

> hciattach -l
many, including bcm43xx
but I think we're looking for a SDIO, not UART path

> /usr/bin/hciattach /dev/serial1 bcm43xx 921600 noflow -
this seems to hang, but works
flash /lib/firmware/brcm/BCM43430A1.hcd
rfcomm socket layer initialized
> hciconfig hci0 up
> hciconfig
hci0: etc
but I think g_ether, etc, still bunk

> hciconfig
hci0: Type primary bus uart
bd address: B8:27:EB:CB:10:BB
> rfkill list
phy0, hci0
> hcitool scan
Some nearby devices, less than what my phone sees

> hcitool -i hci0 cmd 0x08 0x0008 12 11 07 9E CA DC 24 0E E5 A9 E0 93 F3 A3 B5 01 00 40 8E 00 00 00 00 00 00 00 00 00 00 00 00 00
> hcitool -i hci0 cmd 0x08 0x0006 00 08 00 08 00 00 00 00 00 00 00 00 00 07 00
> hcitool -i hci0 cmd 0x08 0x000A 01

verify with nrf connect - works "BlueZ 5.43"

## Checking the system clock
This was supposed to relate to the Broadcom chip. Ultimately, it was a non-issue.
``cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`` gives 700000 instead of 1000000

## Links and references

This uses btpycom. It it based on serial data stream. Includes Android code sample.

http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/bluetooth.inc.php

https://medium.com/@andrewlr/raspberry-pi-zero-w-setup-ab16f89d8120

https://blog.iamlevi.net/2017/05/control-raspberry-pi-android-bluetooth/

https://github.com/JonnoFTW/rpi-can-logger
