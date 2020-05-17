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
- not copied correctly
- bad VM image (bento/ubuntu-16.04)

try manually copying:

```
cp -r /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0 /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native
cp -r /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0 /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib
mkdir -p /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache
```

then 

```
547b34fba6aa80fd7189c5621/update_pixbuf_cache: 
cannot create /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/../loaders.cache: 
Directory nonexis
tent
```

### Do we really need it?
- look for disable flags
- try core-image-minimal - nope, still ``gdk-pixbuf-query-loaders: not found``
- use a headless raspberry pi zero w layer

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

## Redux
Let's try this again and break it down. It's trying to run ``gdk-pixbuf-query-loaders``

```
NOTE: Running intercept scripts:
NOTE: > Executing update_icon_cache intercept ...
NOTE: Exit code 127. Output:
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_icon_cache: 
6: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_icon_cache: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native//gdk-pixbuf-2.0/gdk-pixbuf-query-loaders: 
not found
```

The ``update_icon_cache`` is generated and consists of:

```sbtshell
#!/bin/sh

set -e

# update native pixbuf loaders
$STAGING_DIR_NATIVE/${libdir_native}/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders --update-cache

for icondir in $D/usr/share/icons/*/ ; do
    if [ -d $icondir ] ; then
        gtk-update-icon-cache -fqt  $icondir
    fi
done
```

Whose template is ``.\sources\poky\scripts\postinst-intercepts\update_pixbuf_cache``

So it's expecting the pixbuf application in

``/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native/``

But it's at

``/usr/lib/x86_64-linux-gnu``

So maybe it got the path wrong, or it's expecting it to have been copied. Or multiarch issue?
Is gdk-pixbuf-2.0 only used to build or it it also deployed?

In ``update_icon_cache``

``lib_native='''`` this explains the '//' in the bum path.

Hard wiring the path in ``update_icon_cache`` fixes the exec problem, but next is a directory problem:

```sbtshell
NOTE: > Executing update_pixbuf_cache intercept ...
NOTE: Exit code 2. Output:
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_pixbuf_cache: 
8: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_pixbuf_cache: 
cannot create /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/../loaders.cache: 
Directory nonexistent
```

So in this case this does exist: ``/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib``

But the directory ``gdk-pixbuf-2.0`` doesn't.

Suspect there's a bad path or a copy/move that's missing or not working.

Doctored up ``update_icon_cache`` with:

```
cp -r /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0 $STAGING_DIR_NATIVE/${libdir_native}
mkdir -p /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders
```
then

```
NOTE: Running intercept scripts:
NOTE: > Executing update_icon_cache intercept ...
NOTE: ============================/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/recipe-sysroot-native
Failed to create file '/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache.ICL3I0': Permission denied
```

## Clean
Try a dead simple build.

```sbtshell
source /vagrant/sources/poky/oe-init-build-env build_qemux86
bitbake core-image-minimal
```

then out of disk space on / only 64 GB, but hey, was able to build rpi before

Fresh VM, then same ``gdk-pixbuf-query-loaders: not found``

Maybe bad VM?

## Bad VM?
- switch to 32 bit Ubuntu
- use warrior
- increase disk to 64 GB
- add additional packages

using "bento/ubuntu-16.04" is 64-bit:

``Linux vagrant 4.4.0-173-generic #203-Ubuntu SMP Wed Jan 15 02:55:01 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux``

Let's try 32-bit

then 2 errors

```
checking target system type... i686-pc-linux-gnu
configure: error: internal configure error for the platform triplet, please file a bug report
```

try updating sources

VM seemed to crash

also

``sudo apt-get install libgdk-pixbuf2.0-0``

or maybe this:

``sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib build-essential chrpath socat cpio python python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping libsdl1.2-dev xterm make xsltproc docbook-utils fop dblatex xmlto python-git   libxml2-utils language-pack-en live-build rsync``

but that's a lotta SHIT

still fails:

```sbtshell
NOTE: > Executing update_gtk_immodules_cache intercept ...
NOTE: > Executing update_pixbuf_cache intercept ...
NOTE: Exit code 2. Output:
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_pixbuf_cache: 
8: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_pixbuf_cache: 
cannot create /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/../loaders.cache: 
Directory nonexistent
```

```sbtshell
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/intercept_scripts-2ebd9c7b3b38bf73f0a2cb90a178f2fdd4f4ea4547b34fba6aa80fd7189c5621/update_pixbuf_cache: 
line 8: 
/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/../loaders.cache: 
No such file or directory
```

``/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/../loaders.cache`` no such file or directory

``/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache`` no such file or directory

``ls -l /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib`` OK

``mkdir -p /home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders``

but bitbake wipes it out, so need to add it into the recipes somewhere.

``find . -name 'gdk-pixbuf-2.0' -print`` NADA

``find . -name 'gdk-pixbuf-2.0' -print`` -> ``/usr/lib/i386-linux-gnu/gdk-pixbuf-2.0``

So ether bad path or missing copy. Actually, suspect bad path, since the i386 wouldn't work on the RPI

so can this be stripped from the path? ``/home/vagrant/build-rover/tmp/work/raspberrypi0_wifi-poky-linux-gnueabi/core-image-base/1.0-r0/rootfs``

how about here: ``sources/poky/meta/classes/pixbufcache.bbclass:20``

same error, so it's not the exec path, but the data path

may look here: ``/vagrant/sources/poky/scripts/postinst-intercepts/update_pixbuf_cache``

## Smoking gun
OK, just some brute force commenting out code:
- update_pixbuf_cache
- update_icon_cache
- update_font_chache.

Now  let's find a blank sdcard and see if it works!

## OK, now VM is hanging
Rebuild VM and bitbake OK
Vagrant ssh error
Although, there have been VBManager errors before when trying to destroy...

```
DEBUG subprocess: Waiting for process to exit. Remaining to timeout: 32000
DEBUG subprocess: Exit status: 0
DEBUG virtualbox_6_1:   - [1, "ssh", 2222, 22, "127.0.0.1"]
 INFO subprocess: Starting process: ["C:\\HashiCorp\\Vagrant\\embedded\\usr\\bin/ssh.EXE"]
DEBUG subprocess: Selecting on IO
DEBUG subprocess: stderr: usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
           [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
           [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
           [-i identity_file] [-J [user@]host[:port]] [-L address]
           [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
           [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
           [-w local_tun[:remote_tun]] destination [command]
DEBUG subprocess: Waiting for process to exit. Remaining to timeout: 32000
DEBUG subprocess: Exit status: 255
 INFO ssh: Invoking SSH: 
C:\HashiCorp\Vagrant\embedded\usr\bin/ssh.EXE [
"vagrant@127.0.0.1", 
"-p", "2222", 
"-o", "LogLevel=FATAL", 
"-o", "Compression=yes", 
"-o", "DSAAuthentication=yes", 
"-o", "IdentitiesOnly=yes", 
"-o", "StrictHostKeyChecking=no", 
"-o", "UserKnownHostsFile=/dev/null", 
"-i", "E:/Projects/RPI/yrv/.vagrant/machines/default/virtualbox/private_key"]
DEBUG safe_exec: Converting command and arguments to common UTF-8 encoding for exec.
DEBUG safe_exec: Command: `
"C:\\HashiCorp\\Vagrant\\embedded\\usr\\bin/ssh.EXE"` Args: `["vagrant@127.0.0.1", "-p", "2222", "-o", "LogLevel=FATAL", "-o", "Compression=yes", "-o", "DSAAuthentication=ye
s", "-o", "IdentitiesOnly=yes", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-i", "E:/Projects/RPI/yrv/.vagrant/machines/default/virtualbox/private_key"]`
DEBUG safe_exec: Converted - Command: `"C:\\HashiCorp\\Vagrant\\embedded\\usr\\bin/ssh.EXE"` Args: `["vagrant@127.0.0.1", "-p", "2222", "-o", "LogLevel=FATAL", "-o", "Compression=yes", "-o", "DSAAuthe
ntication=yes", "-o", "IdentitiesOnly=yes", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-i", "E:/Projects/RPI/yrv/.vagrant/machines/default/virtualbox/private_key"]`
```

## Now cannot access the sdcard

try
sudo apt-get install --reinstall udisks2

Still a bit janky, maybe the OS image (ubuntu/xenial32)

## rootfs untar
bunch of issues, including read-only file system

## Revert to old OS
