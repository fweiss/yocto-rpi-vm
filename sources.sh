#!/bin/bash

defaultPokySources() {
	cd ~
	git clone git://git.yoctoproject.org/poky
	cd poky
	git checkout tags/yocto-2.6.1 -b my-yocto-2.6.1
}

mkdir -p ~/rpi/sources
cd ~/rpi/sources

git clone -b rocko git://git.yoctoproject.org/poky
git clone -b rocko git://git.openembedded.org/meta-openembedded
git clone -b rocko git://git.yoctoproject.org/meta-raspberrypi
git clone https://github.com/imyller/meta-nodejs.git
git clone https://gitlab.com/8bitrobots/meta-8bitrobots.git
git clone https://github.com/OSSystems/meta-browser.git

git clone https://github.com/meta-rust/meta-rust.git
