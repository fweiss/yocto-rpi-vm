#!/usr/bin/python3

#  burn an sd card with the RPI image after 'bitbake core-image-base'

# TODO run the whole script as sudo to avoid the embedded sudo and allow use of shutil
# TODO use the rpi-sdimg with dd?

import os
import sys
import subprocess
import glob

MACHINE = "raspberrypi0-wifi"
PACKAGE = "core-image-base"

IMAGE_DIR = "tmp/deploy/images/{}".format(MACHINE)
MOUNT_DIR = "/media/card"
DEVICE_PATH = "/dev/sdf"

BOOT_FILES_PATH = "./{}/bcm2835-bootfiles".format(IMAGE_DIR)
KERNEL_IMAGE_PATH = "./{}/zImage".format(IMAGE_DIR)
ROOTFS_PATH = "./{}/{}-{}.tar.bz2".format(IMAGE_DIR, PACKAGE, MACHINE)

def main():
    try:
        check_mount_dir()
        check_device_path()
        check_image_paths()
        check_kernel_image_file()
        
        print("starting write of image {}".format(MACHINE))
        
        on_mount(partition(1), format_vfat, [ copy_boot_files, copy_kernel_image, copy_overlays, copy_custom_boot_files ])
        on_mount(partition(2), format_ext4, [ copy_rootfs, copy_etc_modules ])
        
        print("finished write of image {}".format(MACHINE))
        
    except Exception as err:
        print("FAIL: {}".format(err))
        sys.exit(1);

############## checking the parameters
        
def check_mount_dir():
    if not os.path.isdir(MOUNT_DIR):
        raise Exception("required MOUNT_DIR '{}' is missing or not a directory".format(MOUNT_DIR))
        
def check_device_path():
    if  not os.path.exists(DEVICE_PATH):
        raise Exception("required DEVICE_PATH '{}' is not found".format(DEVICE_PATH))

# are all the image files available
# assumes cwd is build/tmp/deploy/images
def check_image_paths():
    if not os.path.isdir(IMAGE_DIR):
        raise Exception("image path '{}' not found".format(IMAGE_DIR))
    if not os.path.exists(ROOTFS_PATH):
        raise Exception("rootfs tarball '{}' not found".format(ROOTFS_PATH))

def check_kernel_image_file():
    if not os.path.exists(KERNEL_IMAGE_PATH):
        raise Exception("kernel image file '{}' not found".format(KERNEL_IMAGE_PATH))

############ subprocess helper function

# run a subprocess with the given args and no shell
# check return code and if not zero, raise exception with given message
def run_and_check(args, fail_message):
    proc = subprocess.run(args, shell=False)
    if proc.returncode != 0:
        raise Exception(fail_message, proc)
    
############ filesytem helper functions

def partition(partition):
    return "{}{}".format(DEVICE_PATH, partition)
    
def format_null(part):
    print("no format for {}".format(part))

def format_vfat(part):
    print("vfat format for {}".format(part))
    args = [ "sudo", "mkfs.vfat", "-F", "32", part, "-n", "BOOT" ]
    run_and_check(args, "could not format vfat on {}".format(part))

def format_ext4(part):
    print("ext4 format for {}".format(part))
    args = [ "sudo", "mkfs.ext4", "-F", "-q", "-L", "ROOT", part ]
    run_and_check(args, "could not format ext4 on {}".format(part))
    
########### file copy functions

# an alternative would be to use shutil to copy files, 
# but that would require running the entire python script as su

def copy_boot_files():
    print("copying boot loader files")
    for boot_file in os.listdir(BOOT_FILES_PATH):
        full_file_name = os.path.join(BOOT_FILES_PATH, boot_file)
        if os.path.isfile(full_file_name):
            args = [ "sudo", "cp", full_file_name, MOUNT_DIR ]
            run_and_check(args, "could not copy boot loader files")

def copy_kernel_image():
    print("copying kernel image")
    args = [ "sudo", "cp", KERNEL_IMAGE_PATH, "{}/kernel.img".format(MOUNT_DIR) ]
    run_and_check(args, "could not copy kernel image")

def copy_overlays():
    print("copying device tree overlays")
    args = [ "sudo", "mkdir", "{}/overlays".format(MOUNT_DIR) ]
    run_and_check(args, "could not mkdir 'overlays'")
    dtbos = glob.glob("./{}/*{}.dtbo".format(IMAGE_DIR, MACHINE))
    for dtbo in dtbos:
        # strip machine name from destination filenames
        bare_dtbo = dtbo.replace("-{}".format(MACHINE), "").replace("/{}/".format(IMAGE_DIR), "/")
        args = [ "sudo", "cp", dtbo, "{}/overlays/{}".format(MOUNT_DIR, bare_dtbo) ]
        run_and_check(args, "could not copy dtbo {}".format(dtbo))
    dtbs = [ "bcm2708-rpi-0-w.dtb", "bcm2708-rpi-b.dtb", "bcm2708-rpi-b-plus.dtb", "bcm2708-rpi-cm.dtb" ]
    for dtb in dtbs:
        args = [ "sudo", "cp", "./{}/{}".format(IMAGE_DIR, dtb), MOUNT_DIR ]
        run_and_check(args, "could not copy dtb {}".format(dtb))

def copy_custom_boot_files():
    print("copying custom boot files")
    args = [ "sudo", "cp", "/vagrant/boot/config.txt", MOUNT_DIR ]
    run_and_check(args, "could not copy config.txt")

def copy_rootfs():
    # TODO copy (optional) urandom, interfaces, wpa supplicant
    print("copying rootfs")
    args = [ "sudo", "tar", "--numeric-owner", "-C", MOUNT_DIR, "-xjf", ROOTFS_PATH ]
    run_and_check(args, "could not copy rootfs")

def copy_etc_modules():
    # insert the i2c module to make /dev/i2c-1
    print("copying /etc/modules")
    args = [ "sudo", "cp", "/vagrant/root/etc/modules", "{}/etc/modules".format(MOUNT_DIR)]
    run_and_check(args, "could not copy /etc/modules")
    # N.B. prevent the file from getting zeroed during boot
    args = [ "sudo", "chmod", "400", "{}/etc/modules".format(MOUNT_DIR)]
    run_and_check(args, "could not chmod /etc/modules")

############## file system mount wrapper

# perform the given list of functions on the given filesystem
# TODO check device path
def on_mount(device, format_part, fns):
    format_part(device)
    print("mounting {} on {}".format(device, MOUNT_DIR))
    args = [ "sudo", "mount", device, MOUNT_DIR ]
    run_and_check(args, "could not mount {} on {}".format(device, MOUNT_DIR))

    try:    
        for fn in fns:
            fn()
        
    finally:
        print("umounting {} from {}".format(device, MOUNT_DIR))
        args = [ "sudo", "umount", device ]
        run_and_check(args, "could not umount {}".format(device));

if __name__ == "__main__":
    main()
    