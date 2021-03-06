# yocto-rpi-vm

Learning how to build an embedded Linux image for Raspberry Pi

## Goals
- create a bootable SD card for Raspberry Pi Zero W from scratch
- no GUI, no manual package installation on the RPI
- be able to ssh into the RPI easily via USB (no wifi setup)
- use a simple Yocto recipe to create the SD card
- use a VM to run Yocto
- be able to run Yocto in VM on Windows host
- be able to write SD card image on Windows from VM

Maybe learn about device drivers.

## Prerequisites
The following applications need to be installed to use this project:

- [VirtualBox](https://www.virtualbox.org) - a free, widely used hypervisor
- [Vagrant](https://www.vagrantup.com) - a free tool for building and configuring VMs

The following hardware is required:

- a Raspberry Pi, preferably a Zero or Zero W
- host machine with SD Card reader
- spare SD Card 8 GB or greater
- micro USB cable

You'll also need a fast internet connection, as there are many downloads.

## Updating Git working tree
This Git project uses submodules to pull in the Yocto meta projects.
After you've cloned this project, use the following in bring in the submodules:

``git submodule update --init --recursive``

> You can repeat this later on the bring in subsequent updates to the "meta" projects.

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

> Run vagrant box update to make sure the vm image is up to date

Run ``vagrant up`` to create and provision the VM. This requires an internet connection and may take several minutes.

Run ``vagrant ssh`` to access a shell on the VM. You will run the Yocto build and SD Card utilities from this shell.

## Setting up the yocto build environment
The yocto build environment will be setup in the VM as follows:

- /vagrant/source - the yocto source and layers
- /home/vagrant/build-rover - the build workspace

Run the following to setup the Yocto build environment:

```
TEMPLATECONF=/vagrant/conf source /vagrant/sources/poky/oe-init-build-env build-rover
```

> This will change the current directory to "build".

> Tip: the template doesn't overwrite existing conf files. You may ned to ``rm build-rover/conf/*``

Building the image will take place in the build-rover directory. 
The sources directory is only used to update the yocto tool chain.

## Building the image
Before building the image with the "bitbake" command, check the build parameters.

- ./conf/bblayers.conf - specifies the modules that will go into the image
- ./conf/local.conf - has the desired machine, e.g. "raspberrypi0"

The conf/local.conf file should have:

```
MACHINE ?= "raspberrypi0-wifi"
ENABLE_I2C = "1"
```
> Machine can also be "raspberrypi-wifi" for use with RPIWZ.

Now run 
``bitbake core-image-base``

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

Run ``/vagrant/scripts/partition-sd.py``

Create a mount point ``sudo mkdir /media/card``. 

TODO: make the media/card part of VM 

### Write the image to the SD Card
This step prepares an SD Card that the RPI can boot.

> Look at the source code for an overview of what it does.

Run ``/vagrant/scripts/write-sd-image.py``

When the process is successful, you should see a message like "Finished write of image raspberrypi0".

## Access the RPI via ssh over USB
After inserting the SD card into the Raspberry Pi Zero W and booting, you should be able to get a remote shell.

Connect a USB cable between your desktop or laptop and the Raspberry Pi Zero W.

On Mac/Linux, start the remote shell with this command:

``ssh root@raspberrypi0-wifi.local``

On Windows, start the remote shell with this command:

``putty root@raspberrypi0-wifi.local``

Tips:
- on the RPI0, plug micro USB into the USB, not the PWR IN connector
- wait for the OS to finish boot - the green LED should flicker and then go solid
- you may need to clear the RSA fingerprint from ~/.shh/known_hosts

You can of course use the other related ssh commands to perform file copy and remote exec.
On Mac, there's even a way to mount a remote directory over ssh. This can be very handy when you have
an RPI application that you are developing. You can edit the application on your host computer with
an IDE and SCM using the full resources of your host.

## Debugging the image
Debugging the image on Raspberry Pi Zero/Zero W:

- use a monitor with HDMI input, use an HDMI mini cable or adapter
- USB micro to USB A adapter to connect USB keyboard
- power via the power USB micro connector
- for RPI GUI, add a mouse with a cheap USB hub and Micro-USB adator

> When LED flashes seven times, that indicates missing kernel.img

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

## Windows access SD Card via VirtualBox
There's some setup required to be able to access the SD Card from the VM.
Once this is done, you'll be able to see the inserted SD Card inside the VM with the ``lsblk`` command.

> Note: It seems to be better to halt and start the VM with the vagrant commands ``vagrant halt`` and ``vagrant up``.
> Vagrant seems to get a bit confused when you do this directly from VirtualBox GUI.

### VirtualBox Extension Pack

- Insert SD card in reader on Windows host machine
- Install the VirtualBox Extension Pack
- Restart VM

> Only needs to be done once after VirtualBox is installed.
> If you've upgrdaed vb, update the ext as well, using File > Prefences > Extensions, etc

### Enable USB in VM settings

- Halt the VM ``vagrant halt``
- Open VirtualBox Manager
- Select the ``yocto-rpi-vm`` VM
- Select Settings > USB
- Enable USB Controller
- Click the "+" tool button
- Select the host USB device for the CD card reader
- Start the VM
- Wait a while, and the SD card will appear with ``lsblk`` in the VM

> Only needs to be done when a new VM is created with Vagrant.

> Note: the following was useful. It required running cmd and VBox as admin, but still access errors. 
> https://scribles.net/accessing-sd-card-from-linux-virtualbox-guest-on-windows-host/

## Connect via ssh over USB
One of the goals of this project is to be able to ssh into the RPI via a USB cable.
The advantage of this over WiFi is that it requires no WiFi network nor access credentials.
This would be especially useful in some demo situations, which may be hindered by lack of or 
difficulty of establishing WiFi connectivity.

https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/

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

- [dropbear](https://matt.ucc.asn.au/dropbear/dropbear.html) - lightweight ssh service
- [openssh](https://www.openssh.com) - open source, widely used suite for secure connectivity

Dropbear is a light-weight implementation.

(need to add to recipe)

> The following are taken care of by yocto, correct?

In the /boot/cmdline.tx file add the following at the end after rootwait: ``modules-load=dwc2,g_ether``

In the /boot/config.txt file, add the following at the end: ``dtoverlay=dwc2``

### Transfering files over ssh
It's handy to have sftp server on the RPI, so that you can easily upload files
without having to setup full internet connection.

Supposed to be handled with openssh

> Just use scp, instead!

### Debugging the connection
It was very helpful to just connect the RPI via HDMI and USB keyboard to debug the boot process,
look at log files, and test some assumptions.

## GPIO
A further goal is to run an app on the RPI that interacts with the hardware.
An example is to drive a two-axis, servo-controlled arm.
For expandability a servo hat was used.
The RPI communicates with the servo hat via I2C.

### I2C
The yocto overlays support I2C. The following should be added to ~/build/conf/local.conf:

```
ENABLE_I2C = "1"
```

This setting will add the following to boot:/config.txt:

```
dtparam=i2c1=on
dtparam=i2c_arm=on
```

> There were some problems with the yocto-generated boot:/config.txt.
> Still using a short one from /vagrant/boot.

> But still need to ``modprobe i2c_dev`` after boot to get /dev/i2c-1 to appear

It seems there's something missing in /etc/init.d, or in /etc/modprobe.d, or in thr udev configuration.

The solution is to  add ``i2c_dev`` to /etc/modules. because i2c is not in the device tree, unlike SPI.
This is taken care of by the sd card script, but ought to be in a Yocto recipe.

The /dev/i2c-1 file exists, but its permissions are ``600 root root``. Need to create an "i2c" group so that a 
non-root process can access it.

- create i2c group
- add udev rule to set the group and permissions on /dev/i2c-1 (see below)
- add any application users (such as "pi" or "rover") to the i2c group)

The udev rule can be created along the lines of ``echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c"' >> /etc/udev/rules.d/10-local_i2c_group.rules``

## Loose ends
Some things left to explore:

- ``RPI_USE_UBOOT``
- remove dtoverlay=dwc2 from config.txt
- test VM and tooling on Mac
- be able to access the Pi Zero W as a Bluetooth peripheral
- which Ubuntu for VM, 16.04 or 18.04

## Related projects
This yocto-rpi-vm project only builds an embedded linux image for the Raspberry Pi suitable for adding
an embedded application.

I have a fledging robotic application which I plan to run. The main focus would be to control the 
two-axis servo arm from a smart phone via bluetooth.

## About the host platform
This project was developed and testing on the following platform:

### Windows 7 Professional

- Windows 7 Professional
- Intel Xeon E3-1270 V2 @ 3.50 GHz
- 16 GB memory
- SSD main drive
- SATA 2 TB data drive

On this platform, the build took about 2 hr 45 min.

### MacBook Pro

- MBP Core i7 @ 2.7 GHz
- macOS High Sierra 10.13.6
- 16 GB memory

## About Raspberry Pi Zero W
The MCU is marked Elpida B4432BBPA. Supposed to be BCM2835?

ARM1176JZF-S

BCM43438/CYW43438 radio, connected via SDIO

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

[Detailed description of RPI Device Trees and Overlays](https://www.raspberrypi.org/documentation/configuration/device-tree.md)

https://github.com/raspberrypi/linux/tree/rpi-4.14.y/drivers/net/wireless/broadcom/b43

http://linuxgizmos.com/the-best-way-to-build-with-yocto-project-and-bitbake/

[Setup with Zeus 3.0.2](https://www.yoctoproject.org/docs/3.0.2/brief-yoctoprojectqs/brief-yoctoprojectqs.html
)


