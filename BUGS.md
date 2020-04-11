# Bugs

## python3gattlib

## Hard to read bitbake color output
My eyes hurt trying to read red or blue text on a black background.

Prepend the bitbake command with TERM=xterm-mono

Note that xterm-mono made vi cursors not work.

ERROR: core-image-base-1.0-r0 do_rootfs: The postinstall intercept hook 'update_icon_cache' failed, details in 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/temp/log.do_rootfs
ERROR: core-image-base-1.0-r0 do_rootfs: Function failed: do_rootfs
ERROR: Logfile of failure stored in: /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/temp/log.do_rootfs.7804
ERROR: Task (/vagrant/sources/poky/meta/recipes-core/images/core-image-base.bb:do_rootfs) failed with exit code '1'

gdk-pixbuf-query-loaders: not found

fd7189c5621/update_icon_cache: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native//gdk-pixbuf-2.0/gdk-pixbuf-query-loaders: not found