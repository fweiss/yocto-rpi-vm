#!/bin/bash

cd ~
git clone -b thud git://git.yoctoproject.org/poky.git poky-thud

cd ~/poky-thud
git clone -b thud git://git.openembedded.org/meta-openembedded
git clone -b thud https://github.com/meta-qt5/meta-qt5
git clone -b thud git://git.yoctoproject.org/meta-raspberrypi

mkdir -p ~/rpi
cd ~/rpi
git clone -b thud git://github.com/jumpnow/meta-rpi

source ~/poky-thud/oe-init-build-env build
cd ~/rpi
cp meta-rpi/conf/local.conf.sample build/conf/local.conf
cp meta-rpi/conf/bblayers.conf.sample build/conf/bblayers.conf
