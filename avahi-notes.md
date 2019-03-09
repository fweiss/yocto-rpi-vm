# Avahi Notes

## Bare build

/var/log/messages

raspberrypi0.daemon.info
avahi-daemon
- found user avahi, group avahi
- dropped root
- starting up
- called chroot
- dropped remaining
- load service file sftp-ssh
- load service file ssh
- network interface enumeration
- server startup host raspberrypi0.local
- service ssh started
- service sftp-ssh started

dwc_otg host mode

## Modify cmdline.txt, config.txt
Added dwc2, g_ether

lsmod does show dwc2

/var/dmesg

dwc2 usb supply uusb_d not found, using dummy regulator
dwc2 usb supply uusb_a not found, using dummy regulator

maybe conflict with dwc-otg?

should be enumerating usb with:
[257696.847231] usb 1-4: New USB device found, idVendor=0525, idProduct=a4a2
[257696.847240] usb 1-4: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[257696.847247] usb 1-4: Product: RNDIS/Ethernet Gadget
[257696.847252] usb 1-4: Manufacturer: Linux 4.18.0-rc8-rockchip64 with ff580000.usb

but only enumerating
- DWC OTG Controller
- HP USB Multimedia Keyboard

https://git.yoctoproject.org/cgit.cgi/poky/plain/meta/recipes-bsp/usbinit/usbinit/usb-gether

But this appears to be missing from the layers: https://lists.yoctoproject.org/pipermail/yocto/2012-March/005038.html

modprobe g_ether

this gets something going, and lsmod now shows g_ether and others

however, rndis does not connect, ifconfig only lo

ifup usb0

now raspberryp0.local resolves 192.168.7.2, but port 22 connection refused

no sshd running

## sshd
dropbear or openssh?

poky/meta/recipes-connectivity/openssh

poky/meta/recipes-core/dropbear - has init



