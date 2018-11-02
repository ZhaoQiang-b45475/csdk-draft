#!/usr/bin/python

import os
import shutil

filename = "./configs/build_lsdk.cfg"
imagedir = "/home/zhaoqiang/work/flexbuild/build/images/"
soluname = "edgescale-solution.tgz"
firmware = "firmware_ls1043ardb_uboot_sdboot.img"
bootpartition = "bootpartition_arm64_lts_4.9.tgz"
rootfs = "rootfs_ubuntu_bionic_arm64.tgz"
downdir = "/home/zhaoqiang/work/python/csdk-draft/download/"

def enEdge():
    file_data = ""
    with open(filename, "r") as f:
        for line in f:
            if "EDGESCALE=n" in line:
                line = line.replace("EDGESCALE=n", "EDGESCALE=y")
            file_data += line
    with open(filename, "w") as f:
        f.write(file_data)

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
