#!/bin/bash

# write the system image to the sd card

export OETMP=~/rpi/build/tmp
export MACHINE=raspberrypi0-wifi

cd ~/rpi/meta-rpi/scripts
./copy_boot.sh sdf
