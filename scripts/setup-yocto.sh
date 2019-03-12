mkdir ~/sources
cd ~/sources

git clone -b thud git://git.yoctoproject.org/poky
git clone -b thud git://git.openembedded.org/meta-openembedded
git clone -b thud git://git.yoctoproject.org/meta-raspberrypi

cd ~
source ~/sources/poky/oe-init-build-env build

cp /vagrant/conf/bblayers.conf ~/build/conf
