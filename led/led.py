from time import sleep, time
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO
from bottle import route, run
from .Helper import *
from .Controller import CtrlMono, CtrlSingle, CtrlGroup, CtrlLsp
import config

controller = [CtrlMono, CtrlSingle, CtrlGroup, CtrlLsp]

lsp_profile = {
    1: None,
    2: None,
    3: None,
    4: None,
}
situation = {
    # global state
    "standard": 0,
    "ThreadSingle": 0,
    "ThreadGroup": 0,
    "lsp": 0,

    "tmp_value": 1.0,
}

HTML = {
    "main": "",
    "assist": "",
}

'''
@route("/set_lsp_conf/<module>/<value>")
@route("/set_lsp_profile/<nr>")
@route("/set_tg_conf/<module>/<value>")
@route("/set_tg_profile/<nr>")
@route("/set_tg_mode/<mode>")
@route("/reset_pwm")
'''


#################################################################################
#                           controller
#################################################################################
def get_meta():
    if HTML["main"] == "standard":
        return 0
    elif HTML["main"] == "ThreadSingle":
        return 1
    elif HTML["main"] == "ThreadGroup":
        return 2
    elif HTML["main"] == "lsp":
        return 3
    raise ValueError("ERROR HTML['main']:" + HTML["main"] + " is not implemented")


@route("/flip_meta_state")
def set_state_mode():
    controller[get_meta()].flip_master()


@route("/set/<mode>/<nr>")
def set_state(mode, nr):
    nr = int(nr)
    ctl = get_meta()
    if ctl == 0:
        if mode == "pin":
            if HTML["main"] in ["dc", "fq"]:
                controller[ctl].set_config_single(nr, situation["tmp_value"], HTML["main"])
            else:
                controller[ctl].flip_single(nr)
        elif mode in ["stripe", "color"]:
            if HTML["main"] in ["dc", "fq"]:
                controller[ctl].set_config_group(config.ControllerConfig[HTML["main"]][nr],
                                                 situation["tmp_value"],
                                                 HTML["main"])
            else:
                controller[ctl].unify_group(config.ControllerConfig[HTML["main"]][nr])
        elif mode == "PinsInUse":
            if HTML["main"] in ["dc", "fq"]:
                controller[ctl].set_config_group(config.ControllerConfig[HTML["main"]],
                                                 situation["tmp_value"],
                                                 HTML["main"])
            else:
                controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])

    elif ctl == 1 or ctl == 3:
        if mode == "pin":
            controller[ctl].flip_single(nr)
        elif mode in ["stripe", "color"]:
            controller[ctl].unify_group(config.ControllerConfig[HTML["main"]][nr])
        elif mode == "PinsInUse":
            controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])

    elif ctl == 2:
        if HTML["assist"] == "adjust":
            # implement
            controller[ctl].update_single(0)
        else:
            if mode == "pin":
                controller[ctl].flip_single(nr)
            elif mode in ["stripe", "color"]:
                controller[ctl].unify_group(config.ControllerConfig[HTML["main"]][nr])
            elif mode == "PinsInUse":
                controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])


@route("/save_tmp_value/<value>")
def save_tmp_value(value):
    situation["tmp_value"] = float(value)


@route("/select_profile/<nr>")
def select_profile(nr):
    controller[get_meta()].select_profile(int(nr))


#################################################################################
#                           HTML
#################################################################################
@route("/")
def web():
    return load_html("standard")


@route("/select/<cur>")
def load_html(cur):
    if cur in ["mono", "single", "group", "lsp"]:
        HTML["main"] = cur
        HTML["assist"] = ""
    else:
        HTML["assist"] = cur


def get_html_style():
    result = ""
    for key in config.html_formation["style"][HTML["main"]][HTML["assist"]]:
        result += config.html["style"][key]
    return result


def get_html_head():
    result = ""
    for key in config.html_formation["head"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["head"][key]
        if key == 0:
            tmp = tmp.replace("xXx" + HTML["main"] + "xXx", "border_green")
        elif key == "master_conf" and controller[get_meta()].configuration["master_state"]:
            tmp = tmp.replace("red", "green")
        elif key == "profiles":
            tmp = tmp.replace("xxxxxxProfile" + controller[get_meta()].configuration["selected_profile"])
        elif key == "pwm":
            tmp = tmp.replace("xxxxxx" + HTML["assist"] + " red", "border_green")
        elif key == "group":
            tmp = tmp.replace("xxxxxx" + HTML["assist"] + " border_red", "green")
        result += tmp
    return "<table>" + result + "</table>"


def get_html_body():
    result = ""
    for key in config.html_formation["body"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["body"][key]
        if key == "mode_selection":
            name = controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]]["name"]
            tmp = tmp.replace("_" + name + " border_red", "green")
            content = config.html["body"][name]
            for name, value in controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]].items():
                content = content.replace("_" + name, str(value))
            tmp += content
        elif key == "config_lsp":
            for name, value in controller[get_meta()].configuration["profile"][controller[get_meta()].configuration["selected_profile"]].items():
                tmp = tmp.replace("_" + name, str(value))
        elif key == "pin_table":
            ctrl = get_meta()
            for pinNr in range(config.ControllerConfig["PinCount"]):
                if controller[ctrl].configuration["state"][pinNr]:
                    tmp = tmp.replace("PIN" + str(pinNr) + "_", "")
                else:
                    tmp = tmp.replace("PIN" + str(pinNr) + "_", "border_")
        result += tmp
    return "<table>" + result + "</table>"


def get_html():
    result = config.html["blueprint"]
    result = result.replace("xxxxxxSTYLExxxxxx", get_html_style())
    result = result.replace("yyyyyyHEADyyyyyy", get_html_head())
    return result.replace("zzzzzzBODYzzzzzz", get_html_head())


#################################################################################
#                           /HTML
#################################################################################

def setCommands(command):
    target = ""
    for c in command:

        # get value from previous command
        if len(target) > 0:
            if target == "save-json" or target == "load-json":
                v0, v1 = get_boolean(c)
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
    run(host=HOST, port=PORT)
