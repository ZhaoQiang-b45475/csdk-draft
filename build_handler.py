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
        print "=========count = %d" % count
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
    print "=============run build"
    ret = os.system(command)
    print "============ret = ", ret
    print "=============finish build"
    if not ret:
        mksolution()
    print "=============finish tar"
    os.chdir(csdkdir)
    file_data = ""
    with open(buildconf, "r") as f:
        for line in f:
            if "EDGEBUILD=1" in line:
                line = line.replace("EDGEBUILD=1", "EDGEBUILD=0")
            file_data += line
        f.close()
    with open(buildconf, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(file_data)
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

if __name__ == '__main__':
    build_handler()
