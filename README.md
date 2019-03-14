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

## Setting up the yocto build environment
The yocto build environment will be setup as follows:

- /home/vagrant/source - the yocto source and layers
- /home/vagrant/build - the build workspace

Run ``source /vagrant/setup-yocto.sh``

## Building the image
Before building the image with the "bitbake" command, check the build parameters.

- conf/bblayers.conf specifies the modules that will go into the image
- conf/local.conf has the desired machine, e.g. "raspberrypi0"

Run ``bitbake core-image-base``

The first time you run bitbake, it will take several hours. It has to do the following:

- download source files and dependencies
- apply patches
- configure the builds
- compile the sources
- package the results

Subsequent builds will be faster, as the build caches intermediate files.

## Image the SD Card
After a new image has been built with bitbake, it's time to put it on the SD Card for the Raspberry Pi.
This process is not as simple as for the usual RPI images, such as Jessie.
First, a blank SD Card needs to be properly partitioned.
Then the files from the build need to be copied into their respective partitions.
These tasks are automated with scripts included in this project.

### Insert the SD Card
Insert the SD card into the host system.

Verify access to the SD Card with the ``lsblk`` command on the VM.

You should see a block device named ``sdf``.

> On Windows, there's some setup required to see the SD Card in the VM. See the section "SD Card from VM on Windows" below.

### Format it (only needed on fresh or currupted card):

``/vagrant/scripts/partition.py``

Create a mount point ``sudo mkdir /media/card``. 

TODO: make the media/card part of VM 

### Write the image to the SD Card
First change the current directory to the images directory

``cd /build/tmp/deploy/images``

Run ``/vagrant/scripts/write-sd-image.py``

When the process is successful, you should see a message like "finished write of image raspberrypi0".

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

## Access SD Card via VirtualBox on Windows
There's some setup required to be able to access the SD Card from the VM.
Once this is done, you'll be able to see the inserted SD Card inside the VM with the ``lsblk`` command.

> Note: It seems to be better to halt and start the VM with the vagrant commands ``vagrant halt`` and ``vagrant up``.
> Vagrant seems to get a bit confused when you do this directly from VirtualBox GUI.

### VirtualBox Extension Pack

- Insert SD card in reader on Windows host machine
- Install the VirtualBox Extension Pack
- Restart VM

### Enable USB in VM settings

- Halt the VM
- In machine settings, enable USB
- Add a USB filter, there will be a drop down showing the available host USB devices
- Start the VM
- Wait a while, and the SD card will appear with ``lsblk`` in the VM

> Note: the following was useful. It required running cmd and VBox as admin, but still access errors. 
> https://scribles.net/accessing-sd-card-from-linux-virtualbox-guest-on-windows-host/

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

## About the host platform
This project was developed and testing on the following platform:

### Windows 7 Professional

- Windows 7 Professional
- Intel XEON E3-1270 V2
- 16 GB ECC memory
- SSD main drive
- SATA 2 TB data drive

On this platform, the build took about 2 hr 45 min.

## About Raspberry Pi Zero W
The MCU is marked Elpida B4432BBPA. Supposed to be BCM2835?

## Links and references

https://www.yoctoproject.org/

https://hackaday.io/project/152729-8bitrobots-module/log/145981-setting-up-yocto-for-raspberry-pi-zero

https://www.yoctoproject.org/docs/2.6.1/brief-yoctoprojectqs/brief-yoctoprojectqs.html

https://github.com/jumpnow/meta-rpi

https://blog.gbaman.info/?p=791 Ethernet over USB

https://media.readthedocs.org/pdf/meta-raspberrypi/latest/meta-raspberrypi.pdf

http://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/

https://elinux.org/Bitbake_Cheat_Sheet

https://www.virtualbox.org/wiki/Downloads
