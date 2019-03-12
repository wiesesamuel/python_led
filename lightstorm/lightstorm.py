import sys


def main():

    # run script
    from .web_interface import led_main
    led_main(sys.argv)
