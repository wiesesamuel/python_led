from time import sleep, time
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO
from bottle import route, run
from .Helper import *
from .Controller import CTRL, CtrlMaster
import config

controller = CTRL

temp = {
    "tmp_value": 1.0,
}

HTML = {
    "main": "standard",
    "assist": "",
}


#################################################################################
#                           controller
#################################################################################
def get_meta():
    return config.Meta[HTML["main"]]


@route("/flip_meta_state")
def flip_meta_state_controller():
    CtrlMaster.flip_master(get_meta())
    return get_html()


@route("/set/<mode>/<nr>")
def set_state(mode, nr):
    nr = int(nr)
    ctl = get_meta()

    # controller mono
    if ctl == 0:
        # set single pin
        if mode == "pin":
            # adjust config
            if HTML["assist"] in ["dc", "fq"]:
                controller[ctl].set_config_single(nr, temp["tmp_value"], HTML["assist"])
            # change state
            else:
                CtrlMaster.flip_single(ctl, nr)

        # set group
        elif mode in ["stripe", "color"]:
            # adjust config
            if HTML["assist"] in ["dc", "fq"]:
                controller[ctl].set_config_group(config.ControllerConfig[mode][nr],
                                                 temp["tmp_value"],
                                                 HTML["assist"]
                                                 )
            # change state
            else:
                CtrlMaster.unify_group(ctl, config.ControllerConfig[mode][nr])

        # set all pins
        elif mode == "PinsInUse":
            # adjust config
            if HTML["assist"] in ["dc", "fq"]:
                controller[ctl].set_config_group(config.ControllerConfig[mode],
                                                 temp["tmp_value"],
                                                 HTML["assist"]
                                                 )
            # change state
            else:
                CtrlMaster.unify_group(ctl, config.ControllerConfig[mode])

    # singleThread, groupThread and Lightshowpi controller
    elif ctl in [1, 2, 3]:
        if mode == "pin":
            CtrlMaster.flip_single(ctl, nr)
        elif mode in ["stripe", "color"]:
            CtrlMaster.unify_group(ctl, config.ControllerConfig[mode][nr])
        elif mode == "PinsInUse":
            CtrlMaster.unify_group(ctl, config.ControllerConfig[mode])

    return get_html()


@route("/save_tmp_value/<value>")
def save_tmp_value(value):
    temp["tmp_value"] = float(value)
    return get_html()


@route("/select_profile/<nr>")
def change_profile(nr):
    CtrlMaster.change_profile(get_meta(), int(nr))
    return get_html()


#nononononono
@route("/select_mode/<mode>")
def select_mode(mode):
    # load current profile with default settings
    controller[get_meta()].update_profile(controller[get_meta()].configuration["default"][mode])
    return get_html()


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

    controller[ctrl].update_all()
    return get_html()


#################################################################################
#                           HTML
#################################################################################
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

        # generate selection buttons and edit current selected selection
        elif key == "selection":
            content = ""
            current = controller[get_meta()].configuration["selected"]
            for nr in range(config.ControllerConfig["SelectionCount"]):
                if nr == current:
                    content += tmp.replace("_NR_", str(nr)).replace("_VALUE_", str(nr)).replace("_SELECTED_", "border_green")
                else:
                    content += tmp.replace("_NR_", str(nr)).replace("_VALUE_", str(nr))

            tmp = "<tr>" + content + "</tr>"

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
    ctrl = get_meta()
    current = controller[ctrl].configuration["selected"]

    for key in config.html_formation["body"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["body"][key]

        # generate a value input table for each attribute from current selection
        if key == "table_row_value_input":
            content = ""
            idCount = 0
            for name, value in controller[ctrl].configuration["selection"][current].items():
                if name not in ["timestamp", "name"]:
                    content += tmp.replace("ID_A", "input" + str(idCount))\
                        .replace("NAME_B", "current value: " + str(value))\
                        .replace("LABEL_C", name)
                    idCount += 1

            # generate single button to transmit all values
            tmp = config.html["body"]["set_button"]
            href = ""
            for id in range(idCount):
                href += " + input" + str(id) + ".value + '&'"
            tmp = tmp.replace("IDS", href)

            tmp += content

        # for ThreadGroup
        elif key == "mode_selection":
            name = controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]]["name"]
            tmp = tmp.replace("_" + name + " border_red", "green")
            content = config.html["body"][name]
            for name, value in controller[get_meta()].configuration["profiles"][controller[get_meta()].configuration["selected_profile"]].items():
                content = content.replace("_" + name, str(value))
            tmp += content

        # edit pin table, each pin in use gets a full colored button
        elif key == "pin_table":
            if config.Settings["generate_table"]:
                pass
                # implement
            else:
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
            if target in ["save-json", "load-json", "generate_table"]:
                v0, v1 = get_boolean(c)
                if v0:
                    config.Settings[target] = v1
            target = ""

        if c[0] == "-":

            # set action
            if c == "-h" or c == "--help":
                print(config.helpPage)
            elif c == "-v" or c == "--verbose":
                config.Settings["verbose"] = 1

            # set target
            elif c == "-sj" or c == "--save-json":
                target = "save-json"
            elif c == "-lj" or c == "--load-json":
                target = "load-json"
            elif c == "-gt" or c == "--generate_table":
                target = "generate_table"


def led_main(command):
    setCommands(command)

    #try:
     #   run(server=config.SERVER, host=config.HOST, port=config.PORT)
    #except Exception:
    run(host=config.HOST, port=config.PORT)
