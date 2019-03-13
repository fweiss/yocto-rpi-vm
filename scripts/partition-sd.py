#!/usr/bin/python3

import os
import subprocess

# partition a fresh SD Card to make in bootable
# assume sfdisk v2.31.1, because this runs in the VM we built

DEVICE_PATH = "/dev/sdf"

def main():
    try:
        check_device()
        partition()
    except Exception as err:
        print("ERROR: {}".format(err))
        exit(1)

def check_device():
    if not os.path.exists(DEVICE_PATH):
        raise Exception("could not device {}".format(DEVICE_PATH))
    if DEVICE_PATH.endswith("sda"):
        raise Exception("won't partition {}".format(DEVICE_PATH))

def partition():
    args = [ "sudo", "sfdisk", DEVICE_PATH ]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, shell=False)
    proc.stdin.write("start=        8192, size=      131072, type=c,   bootable\n".encode());
    proc.stdin.write("start=      139264, type=83\n".encode());
    proc.stdin.close()
    while proc.returncode is None:
        proc.poll()
    if proc.returncode != 0:
        raise Exception("could not partition: {}".format(proc))
    
main()
