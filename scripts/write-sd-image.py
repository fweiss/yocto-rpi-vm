#!/usr/bin/python3

#  burn an sd card with the RPI image after 'bitbake core-image-base'

import os
import sys
import subprocess
import shutil

MACHINE = "raspberrypi0"
PACKAGE = "core-image-base"

MOUNT_DIR = "/media/card"
DEVICE_PATH = "/dev/sdf"

BOOT_FILES_PATH = "./{}/bcm2835-bootfiles".format(MACHINE)
KERNEL_IMAGE_PATH = "./{}/zImage".format(MACHINE)
ROOTFS_PATH = "./{}/{}-{}.tar.bz2".format(MACHINE, PACKAGE, MACHINE)

def main():
    try:
        check_mount_dir()
        check_device_path()
        check_image_paths()
        check_kernel_image_file()
        print("starting write of image {}".format(MACHINE))
        
        on_mount(partition(1), format_vfat, [ copy_boot_files, copy_kernel_image ])
#        on_mount(partition(2), format_ext4, [ copy_rootfs ])
        
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
    if not os.path.isdir(MACHINE):
        raise Exception("image path '{}' not found".format(MACHINE))
    if not os.path.exists(ROOTFS_PATH):
        raise Exception("rootfs tarball '{}' not found".format(ROOTFS_PATH))

def check_kernel_image_file():
    if not os.path.exists(KERNEL_IMAGE_PATH):
        raise Exception("kernel image file '{}' not found".format(KERNEL_IMAGE_PATH))

############ filesytem helper functions

def partition(partition):
    return "{}{}".format(DEVICE_PATH, partition)
    
def format_null(part):
    print("no format for {}".format(part))

def format_vfat(part):
    print("vfat format for {}".format(part))
    args = [ "sudo", "mkfs.vfat", "-F", "32", part, "-n", "BOOT" ]
    cmd = subprocess.run(args, shell=False)
    if cmd.returncode != 0:
        raise Exception("could not format vfat on {}".format(part))

def format_ext4(part):
    print("ext4 format for {}".format(part))
    # TODO suppress prompt/user interaction, possibly 'yes' command
    args = [ "sudo", "mkfs.ext4", "-q", "-L", "ROOT", part ]
    cmd = subprocess.run(args, shell=False)
    if cmd.returncode != 0:
        raise Exception("could not format")
    
########### file copy functions

def copy_boot_files():
    # TODO
    #copy boot files (cmdline, config.txt)
    #copy boot partition
    #rename_kernel_img
    print("copying boot loader files")
#    args = [ "sudo", "cp", "{}/*".format(BOOT_FILES_PATH), MOUNT_DIR ]
#    cmd = subprocess.run(args, shell=True)
#    if cmd.returncode != 0:
#        raise Exception("could not copy boot loader files")
    for boot_file in os.listdir(BOOT_FILES_PATH):
        full_file_name = os.path.join(BOOT_FILES_PATH, boot_file)
        if os.path.isfile(full_file_name):
#            shutil.copy(full_file_name, MOUNT_DIR)
            args = [ "sudo", "cp", full_file_name, MOUNT_DIR ]
            cmd = subprocess.run(args, shell=False)
            if cmd.returncode != 0:
                raise Exception("could not copy boot loader files")

def copy_kernel_image():
    print("copying kernel image")
    args = [ "sudo", "cp", KERNEL_IMAGE_PATH, "{}/kernel.img".format(MOUNT_DIR) ]
    cmd = subprocess.run(args, shell=False)
    if cmd.returncode != 0:
        raise Ecception("could not copy kernel image")

def copy_rootfs():
    # TODO copy (optibal) urandom, interfaces, wpa supplicant
    print("copying rootfs")
    args = [ "sudo", "tar", "--numeric-owner", "-C", MOUNT_DIR, "-xjf", ROOTFS_PATH ]
    cmd = subprocess.run(args, shell=False)
    if cmd.returncode != 0:
        raise Exception("root fs could not be copied", cmd)

############## file system mount wrapper

# perform the given list of functions on the given filesystem
# TODO check device path
def on_mount(device, format_part, fns):
    format_part(device)
    print("mounting {} on {}".format(device, MOUNT_DIR))
    args = [ "sudo", "mount", device, MOUNT_DIR ]
    cmd = subprocess.run(args, shell=False)
    if cmd.returncode != 0:
        raise Exception("mount", cmd)

    try:    
        for fn in fns:
            fn()
        
    finally:
        print("umounting {} from {}".format(device, MOUNT_DIR))
        args = [ "sudo", "umount", device ]
        cmd = subprocess.run(args, shell=False)
        if cmd.returncode != 0:
            raise Exception("umount", cmd)

main()
    