# yocto

Learning how to build an embedded Linux image for Raspberry Pi

## Steps
Vagrant bento/ubuntu

vagrant up
vagrant ssh
sudo /vagrant/bootstrap

### geeric 
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
started in VM on MBP @14:00 end @20:30

## Links and references

https://www.yoctoproject.org/

https://hackaday.io/project/152729-8bitrobots-module/log/145981-setting-up-yocto-for-raspberry-pi-zero

https://www.yoctoproject.org/docs/2.6.1/brief-yoctoprojectqs/brief-yoctoprojectqs.html



