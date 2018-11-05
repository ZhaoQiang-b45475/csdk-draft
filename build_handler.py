import time
from getpass import getuser
import os

from myfunc import *

osusername = getuser()
buildpdir = "/home/" + osusername + "/work/"
builddir = buildpdir + "flexbuild/"
buildconf = "buildconf"

def build_handler():
    count = 0
    while True:
        count += 1
        time.sleep(10)
        print "=========count = %d" % count
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
    print "=============run build"
    os.system(command)
    print "=============finish build"
    mksolution()
    print "=============finish tar"

if __name__ == '__main__':
    build_handler()
