#!/usr/bin/python

import os
import shutil
import fcntl
from getpass import getuser

buildpdir = "/home/" + getuser() + "/work/"
builddir = buildpdir + "flexbuild/"
flexconfig = "./configs/build_lsdk.cfg"
flexdir = "./configs/build_lsdk.cfg"
imagedir = "/home/zhaoqiang/work/flexbuild/build/images/"
soluname = "edgescale-solution.tgz"
firmware = "firmware_ls1043ardb_uboot_sdboot.img"
bootpartition = "bootpartition_arm64_lts_4.9.tgz"
rootfs = "rootfs_ubuntu_bionic_arm64.tgz"
downdir = "/home/zhaoqiang/work/python/csdk-draft/download/"

def readstrfromfile(filename, string):
    with open(filename, "r") as f:
        for line in f:
            if string in line:
                return True
        f.close()

def modifyfile(filename, oldstring, newstring):
    file_data = ""
    with open(filename, "r") as f:
        for line in f:
            if oldstring in line:
                line = line.replace(oldstring, newstring)
            file_data += line
        f.close()
    with open(filename, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(file_data)
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

def enEdge():
    modifyfile(builddir + flexconfig, "EDGESCALE=n", "EDGESCALE=y")

def mksolution():
    os.chdir(imagedir)
    commandtar = "tar -czvf " + soluname + " " + os.readlink(bootpartition) + \
            " " + firmware + " " + os.readlink(rootfs)
    os.system(commandtar)
    destpath = downdir + soluname
    if os.path.exists(destpath):
        os.remove(destpath)
    shutil.move(soluname, downdir)

if __name__ == '__main__':
    mksolution()
