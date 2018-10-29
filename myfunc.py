#!/usr/bin/python

filename = "./config/build_lsdk_internal.cfg"

def enEdge():
    file_data = ""
    with open(filename, "r") as f:
        for line in f:
            if "EDGESCALE=n" in line:
                line = line.replace("EDGESCALE=n", "EDGESCALE=y")
            file_data += line
    with open(filename, "w") as f:
        f.write(file_data)

if __name__ == '__main__':
    enEdge()
