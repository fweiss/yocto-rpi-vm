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

## Checking the system
``cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`` gives 700000 instead of 1000000


