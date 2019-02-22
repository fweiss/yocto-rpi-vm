#!/bin/bash
apt-get update

# ubuntu 18.04 already has python 3.6.7
# apt-get install -y python python3 python3-pip python3-pexpect

# essential packages
apt-get install -y gawk wget git-core diffstat unzip texinfo gcc-multilib \
     build-essential chrpath socat cpio  \
     xz-utils debianutils iputils-ping libsdl1.2-dev xterm \
     gcc-multilib g++-multilib
