#!/usr/bin/python
import os
import sys
from shutil import copyfile

if __name__ == "__main__":

    # copy config defaults
    if not os.path.exists("./config.py"):
        copyfile("./defaults.py", "./config.py")

    # run script
    from led import led_main
    led_main(sys.argv)
