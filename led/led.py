import json
from time import sleep, time
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO
import os
from bottle import route, run
import config
from .Helper import *
from Instance_Generator import Instance
CurrentMode = 0

@route("/setCurrentView/<nr>")
def setCurrentView(nr):
    global CurrentMode
    CurrentMode = int(nr)


# only callable for PinInstance and PinThread
@route("/set/<mode>/<nr>")
def set_mode_nr(mode, nr):
    nr = int(nr)
    if mode == "Stripes" or mode == "Colors":
        if nr < len(config.ControllerConfig[mode][nr]):
            on = 1
            for pin in config.ControllerConfig[mode][nr]:
                if config.States[CurrentMode][pin]:
                    on = 0
                    break
            for pin in config.ControllerConfig[mode][nr]:
                config.States[CurrentMode][pin] = on
                if config.InstanceStates[CurrentMode]:
                    set_instance(nr, on)
                    #Instance[Current_HTML][nr].set_state(on)
        else:
            println("""Error @ "/set/<mode>/<nr>" with mode: """ + mode + ", nr: " + str(nr) + " > " +
                            str(len(config.ControllerConfig[mode][nr])))
    elif mode == "pin":
        config.States[CurrentMode][nr] = not config.States[CurrentMode][nr]
        if config.InstanceStates[CurrentMode]:
            set_instance(nr, config.States[CurrentMode][nr])
            #Instance[Current_HTML][nr].set_state(config.States[Current_HTML][nr])
    else:
        println("""Undefined Call @ "/set/<mode>/<nr>" with mode: """ + mode + " nr: " + str(nr))


# only callable for StripeThread and ColorThread
@route("/set/<nr>")
def set_nr(nr):
    nr = int(nr)
    config.States[CurrentMode][nr] = not config.States[CurrentMode][nr]
    if config.InstanceStates[CurrentMode]:
        set_instance(nr, config.States[CurrentMode][nr])
        #Instance[Current_HTML][nr].set_state(config.States[Current_HTML][nr])


def set_instance(nr, value):
    if CurrentMode == 2:
        pins = get_list_of_ControllerConfig("Stripes", nr)
    elif CurrentMode == 3:
        pins = get_list_of_ControllerConfig("Color", nr)
    set = 1
    for i in range(config.InstancesCount, 0, -1):
        i -= 1
        if i > CurrentMode and config.InstanceStates[i]:
            if i > 1:
            for pins in get_list_of_ControllerConfig(config.InstancesNames[i], nr):
                if pins == nr:
                    return




def get_list_of_ControllerConfig(listName, nr):
    return config.ControllerConfig[listName][nr]


def setCommands(command):
    target = ""
    for c in command:

        # get value from previous command
        if len(target) > 0:
            if target == "save-json" or target == "load-json":
                v0, v1 = getBoolean(c)
                if v0:
                    config.Settings[target] = v1
            target = ""

        if c[0] == "-":
            if c == "-h" or c == "--help":
                print(config.helpPage)
            elif c == "-sj" or c == "--save-json":
                target = "save-json"
            elif c == "-lj" or c == "--load-json":
                target = "load-json"
            elif c == "-v" or c == "--verbose":
                config.Settings["verbose"] = 1


def led_main(command):
    setCommands(command)

    #try:
     #   run(server=config.SERVER, host=config.HOST, port=config.PORT)
    #except Exception:
    run(host=config.HOST, port=config.PORT)
