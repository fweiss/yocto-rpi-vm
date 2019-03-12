# GOAL: install the prerequisites for running yocto

apt_update

# ubuntu 18.04 already has python 3.6.7
# apt-get install -y python python3 python3-pip python3-pexpect

apt_package 'gawk'
apt_package 'wget'
apt_package 'git'
apt_package 'diffstat'
apt_package 'unzip'
apt_package 'texinfo'
apt_package 'gcc-multilib'
apt_package 'build-essential'
apt_package 'chrpath'
apt_package 'socat'
apt_package 'cpio'
apt_package 'xz-utils'
apt_package 'debianutils'
apt_package 'iputils-ping'
apt_package 'libsdl1.2-dev'
apt_package 'xterm'
apt_package 'gcc-multilib'
apt_package 'g++-multilib'
