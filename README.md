# yocto

Learning how to build an embedded Linux image for Raspberry Pi

## Basic VM
Vagrant bento/ubuntu

- vagrant up
- vagrant ssh
- sudo /vagrant/bb.sh (some dos line end issuse need to be cleared up)

## New toolchain
https://jumpnowtek.com/rpi/Raspberry-Pi-Systems-with-Yocto.html

cd ~
source jumpnowtek.sh

cd ~
source poky-thud/oe-init-build-env ~/rpi/build
bitbake console-image

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
Target image bb files are in meta-rpi/images.

Target SD card images ``ls -l ~/rpi/build/tmp/deploy/images/raspberrypi0-wifi``

## SDcard from VM on Windows
https://scribles.net/accessing-sd-card-from-linux-virtualbox-guest-on-windows-host/

This requires runnin cmd and VBox as admin, but still access errors.

WORKING:
- Insert SD card in reader on Windows
- Install the VirtualBox Extension Pack
- Restart VB
- In machine settings, enable USB
- Add a USB filter, there will be a drop down showing the available host SUB devices
- Restart the VM
- Wait a while, and the SD card will appear with lsblk in the VM

## Image the SD Card
Format it (only needed on fresh or currupted card):

``cd ~/rpi/meta-rpi/scripts
~/rpi/meta-rpi/scripts$ sudo ./mk2parts.sh sdb``

sudo mkdir /media/card

``source /vagrant/write_sd.sh``


## Links and references

https://www.yoctoproject.org/

https://hackaday.io/project/152729-8bitrobots-module/log/145981-setting-up-yocto-for-raspberry-pi-zero

https://www.yoctoproject.org/docs/2.6.1/brief-yoctoprojectqs/brief-yoctoprojectqs.html



