# yocto-rpi-vm

Learning how to build an embedded Linux image for Raspberry Pi

## Goals
- create a bootable SD card for Raspberry Pi Zero W from scratch
- be able to ssh into the RPI easily via USB (no wifi setup)
- find or create a simple Yocto recipe
- use a VM to run Yocto
- be able to run Yocto in VM on Windows host
- be able to write SD card image on Windows from VM

Maybe learn about device drivers.

## Prerequisites
You'll need the following applications installed to use this project:

- (VirtualBox)[https://www.virtualbox.org]
- (Vagrant)[https://www.vagrantup.com/]

You'l also need:

- a Raspberry Pi, preferably a Zero or Zero W
- host machine with SD Card reader
- spare SD Card 8 GB or greater
- micro USB cable

You'll also need a fast internet connection, as there are many downloads.

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
The yocto build environment will be setup in the VM as follows:

- /home/vagrant/source - the yocto source and layers
- /home/vagrant/build - the build workspace

Run ``source /vagrant/scripts/setup-yocto.sh``

## Building the image
Before building the image with the "bitbake" command, check the build parameters.

- conf/bblayers.conf - specifies the modules that will go into the image
- conf/local.conf - has the desired machine, e.g. "raspberrypi0"

> ``MACHINE ?= "raspberrypi0``
> ``ENABLE_I2C = "1"``

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

> On Windows, there's some setup required to see the SD Card in the VM. See the section "Access SD Card via VirtualBox on Windows" below.

### Partition the SD Card (only needed on fresh or currupted card)
This will create two partitions on the SD Card:

- a smallish 'boot' partition for the bootloader
- a large 'root' partition for the main file system

Run ``/vagrant/scripts/partition.py``

Create a mount point ``sudo mkdir /media/card``. 

TODO: make the media/card part of VM 

### Write the image to the SD Card
This step prepares an SD Card that the RPI can boot.

> Look at the source code for an overview of what it does.

First change the current directory to the images directory

``cd /build/tmp/deploy/images``

Run ``/vagrant/scripts/write-sd-image.py``

When the process is successful, you should see a message like "Finished write of image raspberrypi0".

## Debugging the image
Debugging the image on Raspberry Pi Zero/Zero W:

- use a monitor with switchable HDMI input
- HDMI - HDMI mini cable or adapter
- USB micro to USB A adapter to connect extra keyboard
- power via the power USB micro connector

- LED flashes seven times, indicating missing kernel.img

## About bitbake
Target image bb files are in rpi/meta-rpi/images.

Windows: bitbake won't work on VM shared folder. Something about locking files. 
Kind of a shame, because it would have been nice to use IDE on host system to browse the yocto/poky/oe meta files. 
Might be possible to do a reverse share.

When you see 'bitbake command not found': source oe-init-build-env

Target SD card images ``ls -l ~/rpi/build/tmp/deploy/images/raspberrypi0-wifi``

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

### sftp server
It's handly to have sftp server on the RPI, so that you can easily upload files
without having to setup full internet connection.

Supposed to be handled with openssh


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

## GPIO

### I2C

Add ``i2c_dev`` to /etc/modules. It seems i2c is not in the device tree, unlike SPI.

Although there's supposed to be in later version yocto, adding ``ENABLE_I2C = "1"`` to conf/local.conf.

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
