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

situation = {
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
    return config.Meta[HTML["main"]]


@route("/flip_meta_state")
def set_state_mode():
    controller[get_meta()].flip_master()
    return get_html()


@route("/set/<mode>/<nr>")
def set_state(mode, nr):
    nr = int(nr)
    ctl = get_meta()

    # controller mono
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
                controller[ctl].unify_group(config.ControllerConfig[mode][nr])
        elif mode == "PinsInUse":
            if HTML["main"] in ["dc", "fq"]:
                controller[ctl].set_config_group(config.ControllerConfig[HTML["main"]],
                                                 situation["tmp_value"],
                                                 HTML["main"])
            else:
                controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])

    # singleThread and Lightshowpi controller
    elif ctl == 1 or ctl == 3:
        if mode == "pin":
            controller[ctl].flip_single(nr)
        elif mode in ["stripe", "color"]:
            controller[ctl].unify_group(config.ControllerConfig[HTML["main"]][nr])
        elif mode == "PinsInUse":
            controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])

    # group Thread controller
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
    return get_html()


@route("/save_tmp_value/<value>")
def save_tmp_value(value):
    situation["tmp_value"] = float(value)
    return get_html()


@route("/select_profile/<nr>")
def select_profile(nr):
    controller[get_meta()].select_profile(int(nr))
    return get_html()


#################################################################################
#                           HTML
#################################################################################
@route("/set_config_values/<input>")
def set_config_values(input):
    ctrl = get_meta()
    blacklist = ["timestamp", "name"]

    # each value is loaded to the next parameter
    for values in input.split("&"):
        for name, value in controller[ctrl].configuration["profiles"][controller[ctrl].configuration["selected_profile"]].items():
            if name not in blacklist:
                blacklist.append(name)
                if values is not "":
                    controller[ctrl].configuration["profiles"][controller[ctrl].configuration["selected_profile"]][name] = float(values)
                break
    return get_html()

@route("/")
def web():
    return load_html("standard")


@route("/select/<cur>")
def load_html(cur):
    if cur in ["standard", "ThreadSingle", "ThreadGroup", "lsp"]:
        HTML["main"] = cur
        HTML["assist"] = ""
    else:
        HTML["assist"] = cur
    return get_html()


def get_html_style():
    # add styles
    result = ""
    for key in config.html_formation["style"][HTML["main"]][HTML["assist"]]:
        result += config.html["styles"][key]
    return result


def get_html_head():
    result = ""
    for key in config.html_formation["head"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["head"][key]
        # edit header, current selected controller is green
        if key == 0:
            tmp = tmp.replace("xXx" + HTML["main"] + "xXx", "border_green")
        # edit controller header state, depends on current master state
        elif key == "master_conf" and controller[get_meta()].configuration["master_state"]:
            tmp = tmp.replace("red", "green")
        # edit profile selection, current selected is green
        elif key == "profiles":
            nr = str(controller[get_meta()].configuration["selected_profile"])
            tmp = tmp.replace("xxxxxxProfile" + nr, "border_green")
        # edit pwm mode, current selected mode is green (fq or dc)
        elif key == "pwm":
            tmp = tmp.replace("xxxxxx" + HTML["assist"] + " red", "border_green")

        # for ThreadGroup
        # current select mode is green (select or adjust)
        elif key == "group":
            tmp = tmp.replace("xxxxxx" + HTML["assist"] + " border_red", "green")
        result += tmp
    return "<table>" + result + "</table>"


def get_html_body():
    result = ""
    for key in config.html_formation["body"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["body"][key]

        # generate a value input table for each attribute in controller.configuration["profiles"][current]
        if key == "table_row_value_input":
            content = ""
            idCount = 0
            for name, value in controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]].items():
                if name not in ["timestamp", "name"]:
                    content += tmp.replace("ID_A" , "input" + str(idCount)).replace("NAME_B", "current value: " + str(value)).replace("LABEL_C", name)
                    idCount += 1

            # generate single button to transmit all values
            tmp = config.html["body"]["set_button"]
            href = ""
            for id in range(idCount):
                href += " + input" + str(id) + ".value + '&'"
            tmp = tmp.replace("IDS", href)

            tmp += content

        elif key == "mode_selection":
            name = controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]]["name"]
            tmp = tmp.replace("_" + name + " border_red", "green")
            content = config.html["body"][name]
            for name, value in controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]].items():
                content = content.replace("_" + name, str(value))
            tmp += content
        elif key == "config_lsp":
            for name, value in controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]].items():
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
    # parts from config.html_formation are added and edited
    result = config.html["blueprint"]
    result = result.replace("xxxxxxSTYLExxxxxx", get_html_style())
    result = result.replace("yyyyyyHEADyyyyyy", get_html_head())
    return result.replace("zzzzzzBODYzzzzzz", get_html_body())


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
    run(host=config.HOST, port=config.PORT)
