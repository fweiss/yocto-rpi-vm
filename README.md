# yocto-pi-vm

Learning how to build an embedded Linux image for Raspberry Pi

## Goals
- create a bootable SD card for Raspberry Pi Zero W from scratch
- be able to ssh into the RPI easily via USB (no wifi setup)
- find or create a simple Yocto recipe
- use a VM to run Yocto
- be able to run Yocto in VM on Windows host
- be able to write SD card image on Windows from VM

Maybe learn about device drivers.

## Basic VM
By using a VM, all the required yocto tools are installed and updated.
No worries about interference with other project toolchains.
One shortcoming is that builds are reportedly about half as fast, but with a fast host processor, this is not a big issue.

This was developed and tested on Windows 7, but should work on Windows 10, Mac and Linux as well.

### VagrantFile
The Vagrant file specifies:

- the guest OS, bento/ubuntu-18.04
- the guest VM memory (4096 KB) and number of cores (4)
- the Chef provisioning recipe for the Yocto prerequisites

The Vagrant file and the Chef cookbook may be be modified to suit the circumstances.

### Creating and accessing the VM
Run ``vagrant up`` to create and provision the VM. This may take several minutes and requires an internet connection.

Run ``vagrant ssh`` to access a shell on the VM. You will run the Yocto build and SD Card utilities from this shell.

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

## SSHD/USB/Ethernet Gadget configuration
One of the goals of this project is to be able to ssh into the RPI via a USB cable.
The advantage of this over WiFi is that it requires no WiFi network nor access credentials.
This would be especially useful in some demo situations, which may be hindered by lack of or 
difficulty of establishing WiFi connectivity.

### Key points
During the course of getting this to work, I learned the following:

- the "ethernet gadget" module tunnels an ethernet IP link over USB
- the [avahi](https://www.avahi.org) daemon and Bonjour service provide for ad-hoc DNS lookup
- the ssh daemon is not configured by default on RPI

### Mac observations
On a Mac, the following should be observed:

- in System Preferences > Network, the RNDIS/Ethernet Gadget should have connected status and an IP address
- ``ping raspberrypi0.local`` should resolve
- ``ssh root@raspberrypi0.local`` should open a shell on the RPI

### RPI observations
On the RPI, the following should be observed:

- the avahi-daemon is running (two processes)
- the dropbear daemon is running (see note below)
- the g_ether module should appear in ``lsmod`` (there are a few other associated ones, as well)
- the usb0 network interfacew should appear in ``ifconfig``

### dropbear ssh daemon
The are two options on RPI for ssh service:

- [dropbear](https://matt.ucc.asn.au/dropbear/dropbear.html)
- [openssh](https://www.openssh.com)

Dropbear is a light-weight implementation.


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

## Loose ends
Some things left to explore:

- ``RPI_USE_UBOOT``
- remove dtoverlay=dwc2 from config.txt
- test VM and tooling on Mac

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

