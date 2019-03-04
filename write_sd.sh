#!/bin/bash

# write the system image to the sd card

#export OETMP=~/rpi/build/tmp
export OETMP=/home/vagrant/bare-build/tmp
export MACHINE=raspberrypi0

cd ~/rpi/meta-rpi/scripts
./copy_boot.sh sdf
