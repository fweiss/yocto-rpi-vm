# yocto-pi-vm

Learning how to build an embedded Linux image for Raspberry Pi

## Goals
- create a bootable SD card for Raspberry Pi Zero W from scratch
- be able to ssh into the RPI easily via USB (no wifi setup)
- use a VM to run Yocto
- find or create a simple Yocto recipe
- be able to run Yocto in VM on Windows host
- be able to write SD card image on Windows from VM

Maybe learn about device drivers.

## Basic VM
Vagrant bento/ubuntu

- vagrant up
- vagrant ssh
- sudo /vagrant/bb.sh (some dos line-end issues need to be cleared up)

## Barebones
https://git.yoctoproject.org/cgit/cgit.cgi/meta-raspberrypi/about/

mkdir bare-source
cd bare-source
git clone -b thud git://git.yoctoproject.org/poky
git clone -b thud git://git.openembedded.org/meta-openembedded
git clone -b thud git://git.yoctoproject.org/meta-raspberrypi
cd ..
source bare-source/poky/oe-init-build-env bare-build
vi conf/bblayers.conf: ``cp /vagrant/conf/bblayers.conf conf``
vi conf/local.conf: add ``MACHINE ?= "raspberrypi0"`` 
bitbake core-image-base

copy kernel and rootfs

rename zImage

In the /boot/cmdline.tx file add the following at the end after rootwait: ``modules-load=dwc2,g_ether``

In the /boot/config.txt file, add the following at the end: ``dtoverlay=dwc2``

### Files
The cmdline.txt and conf.txt files are in ``~/bare-build/tmp/deploy/images/raspberrypi0/bcm2835-bootfiles``

Produced a zimage file instead of kernel.img. LED flashes seven time, indicating missing kernel.img.

Rename zImge to kernel.img gets console output, but cannot find the root fs.

Comparing cmsdine.txt to working Jessie image, there's root=/dev/mmcblk0p2 instead of root=PARTUUID=03e791ca-02.

Trying to add ROOT_VM = "root=PARTUUID=${DISK_SIGNATURE}-02" to conf/conf.txt

Solution: need to run modified meta-rpi/scriptsd/copy_roofs.sh

## New toolchain
https://jumpnowtek.com/rpi/Raspberry-Pi-Systems-with-Yocto.html

cd ~
source jumpnowtek.sh

in local.conf, add ``ENABLE_DWC2_PERIPHERAL = "1"``

cd ~
source poky-thud/oe-init-build-env ~/rpi/build
bitbake console-image

### Images
~/rpi/meta-rpi/images

ap-image: iot-image
iot-image: console-basic-image
audio-image: >image
console-basic-image: >core-image
console-image: >image
flask-image: console-basic-image

### Config
~/rpi/build/conf/local.conf

## Old toolchain

### generic 
git clone git://git.yoctoproject.org/poky
cd poky
git checkout tags/yocto-2.6.1 -b my-yocto-2.6.1
source oe-init-build-env

### RPI
cd /vagrant - bitbake won't work on shared folder!


mkdir -p ~/rpi/sources
source /vagrant/sources.sh
cd ~/rpi
source sources/poky/oe-init-build-env rpi-build

now in build directory

cp ~/rpi/sources/meta-8bitrobots/example-config/bblayers.conf conf/bblayers.conf
cp ~/rpi/sources/meta-8bitrobots/example-config/local.conf conf/local.conf

add meta-rust to bblayers.conf

bitbake rpi-hwup-image
started in VM on MBP @14:00 end @20:30 (error)
started in VMN on Xeon @10:52

### Build bugs
missing "bits/c++config.h": sudo apt-get install gcc-multilib g++-multilib
nodejs compile error: remove nodejs, etc from bblayers.conf
bitbake command not found: source oe-init-build-env

## About bitbake
Target image bb files are in rpi/meta-rpi/images.

Target SD card images ``ls -l ~/rpi/build/tmp/deploy/images/raspberrypi0-wifi``

## SDcard from VM on Windows
https://scribles.net/accessing-sd-card-from-linux-virtualbox-guest-on-windows-host/

This requires runnind cmd and VBox as admin, but still access errors.

WORKING:
- Insert SD card in reader on Windows
- Install the VirtualBox Extension Pack
- Restart VM
- In machine settings, enable USB
- Add a USB filter, there will be a drop down showing the available host USB devices
- Restart the VM
- Wait a while, and the SD card will appear with lsblk in the VM

## Image the SD Card
Format it (only needed on fresh or currupted card):

``cd ~/rpi/meta-rpi/scripts
~/rpi/meta-rpi/scripts$ sudo ./mk2parts.sh sdb``

sudo mkdir /media/card

``source /vagrant/write_sd.sh``

## USB/Ethernet Gadget configuration
(need to add to recipe)

In the /boot/cmdline.tx file add the following at the end after rootwait: ``modules-load=dwc2,g_ether``

In the /boot/config.txt file, add the following at the end: ``dtoverlay=dwc2``


## Connect via ssh over USB
https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/

### debugging the connection
using a mac host

with jessie:
- ssh works @raspberrypi.local
- the RNDIS/Ethernet Gadget is connected self-assigned 169.254.19.59

with yocto meta-pi
- raspberrypi.local does not resolve
- the RNDIS/Ethernet Gadget does not connect

Perhaps the avahi daemon is not running?

## About Raspberry Pi Zero W
The MCU is marked Elpida B4432BBPA. Supposed to be BCM2835?

## Links and references

https://www.yoctoproject.org/

https://hackaday.io/project/152729-8bitrobots-module/log/145981-setting-up-yocto-for-raspberry-pi-zero

https://www.yoctoproject.org/docs/2.6.1/brief-yoctoprojectqs/brief-yoctoprojectqs.html

https://blog.gbaman.info/?p=791 Ethernet over USB

https://media.readthedocs.org/pdf/meta-raspberrypi/latest/meta-raspberrypi.pdf

http://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/

https://elinux.org/Bitbake_Cheat_Sheet

