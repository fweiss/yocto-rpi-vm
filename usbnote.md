orig
config.txt
dwc_otg.lpm_enable=0
console=serial0,115200
console=tty1
...
rootwait
modules-load=dwc2,g_ether

cmdline.txt
...
dtoverlay=dwc2


yocto
config.txt
...
dtoverlay=dwc2

cmdline.txt
dwc_otg,lpm_enable=0
console-serial0,115200
...
rootwait
modules-load=dwc2,g_ether

## Avahi

poky-thud/meta/receipes-connectivity/avahi

./meta/recipes-core/packagegroups/packagegroup-base.bb
./meta/recipes-connectivity/avahi/files/initscript.patch
./meta/lib/oeqa/runtime/cases/systemd.py
./meta/recipes-kernel/systemtap/systemtap_git.bb
./meta/recipes-connectivity/avahi/files/0001-Fix-opening-etc-resolv.conf-error.patch

## Later notes g_ether
Added to conf/local.conf:
ENABLE_DWC2_PERIPHERAL = "1"
no change to boot:/cmdline.txt
then ls mode shows several related g_ether
but no ifup usb0


## Later notes i2c
Added to conf/local.conf:

then 
but need modprobe i2c_dev to get /dev/i2c-1

