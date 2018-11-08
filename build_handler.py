import time
from getpass import getuser
import os
import fcntl

from myfunc import *

osusername = getuser()
buildpdir = "/home/" + osusername + "/work/"
builddir = buildpdir + "flexbuild/"
buildconf = "buildconf"
csdkdir = os.getcwd()

def build_handler():
    count = 0
    while True:
        count += 1
        time.sleep(5)
        os.chdir(csdkdir)
        with open(buildconf, "r") as f:
            for line in f:
                if "EDGEBUILD=1" in line:
                    realbuild()

def realbuild():
    if not os.path.exists(builddir):
        os.chdir(buildpdir)
        os.system("git clone ssh://git@bitbucket.sw.nxp.com/dash/flexbuild.git")
    os.chdir(builddir)
    enEdge()
    command = "source ./setup.env && flex-builder -m ls1043ardb -a arm64"
    ret = os.system(command)
    if not ret:
        mksolution()
        modifyfile(csdkdir+"/"+buildconf, "EDGEBUILD=1", "EDGEBUILD=4")
    else:
        modifyfile(csdkdir+"/"+buildconf, "EDGEBUILD=1", "EDGEBUILD=3")

if __name__ == '__main__':
    build_handler()
