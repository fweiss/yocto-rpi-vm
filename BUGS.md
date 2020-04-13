# Bugs

## python3gattlib

## Hard to read bitbake color output
My eyes hurt trying to read red or blue text on a black background.

Prepend the bitbake command with TERM=xterm-mono

Note that xterm-mono made vi cursors not work.

## gdk-pixbuf-query-loaders
Hypothesis
- do we really need these?
- what's wrong with the path?

### Do we really need it?
- look for disable flags
- try core-image-minimal - nope, still ``gdk-pixbuf-query-loaders: not found``

### What's wrong with the path?

ERROR: core-image-base-1.0-r0 do_rootfs: The postinstall intercept hook 'update_icon_cache' failed, details in 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/temp/log.do_rootfs
ERROR: core-image-base-1.0-r0 do_rootfs: Function failed: do_rootfs
ERROR: Logfile of failure stored in: /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/temp/log.do_rootfs.7804
ERROR: Task (/vagrant/sources/poky/meta/recipes-core/images/core-image-base.bb:do_rootfs) failed with exit code '1'

gdk-pixbuf-query-loaders: not found

```
NOTE: Running intercept scripts:
NOTE: > Executing update_icon_cache intercept ...
NOTE: Exit code 127. Output:
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_icon_cache: 
6: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_icon_cache: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native//gdk-pixbuf-2.0/gdk-pixbuf-query-loaders: not found
```

``find . -name 'gdk-pixbuf-query-loaders -print``

nothing found. Is this yocto tooling?

found it here:

``/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders``

the libdir variable is only set in

```
/vagrant/sources/poky/meta/conf/bitbake.conf:export libdir = "${exec_prefix}/${baselib}"
/vagrant/sources/poky/meta/recipes-core/sysfsutils/sysfsutils_2.1.0.bb:export libdir = "${base_libdir}"
```

looks like a bad path in the bb tooling, also not the duplicate '//'

So in ``/vagrant/sources/pokey/meta/conf/bitbake.conf`` the 'baselib' variable comes from the env 

```
# Used by multilib code to change the library paths
baselib = "${BASELIB}"
```

try hardcoding in gdk-icon-cache.bbclass

try ``vagrant@vagrant:~/build-rover$ ln -s /usr/lib/x86_64-linux-gnu /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-
      linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native/gdk-pixbuf-2.0``


in ``/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_icon_cache``
just comment the whole thing out

./sources/poky/scripts/postinst_intercepts/
also ``update_pixbuf_cache``, ``update_font_cache``

try ``sudo apt-get intall qemu``

there's also a --disable-pixbuf-loader somewhere

hardcode all the ${libdir} for ``gdk-pixbuf-2.0/gdk-pixbuf-query-loaders``

then

```
80fd7189c5621/update_pixbuf_cache: 
cannot create /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/../loaders.cache: 
Directory nonexistent
```

