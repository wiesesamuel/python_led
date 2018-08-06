import json
from time import sleep, time
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO
import os
from bottle import route, run
from .Helper import *
from config import *

controller = {
    # global state
    "standard": 0,
    "ThreadSingle": 0,
    "ThreadGroup": 0,
    "lsp": 0,

    # current
    "lspProfile": 2,
    "ThreadSingleProfile": 0,
    "ThreadGroupProfile": 0,

    # access check [tg][ts][s]
    #   tg  ts  s
    #   0   0   0 = 0
    #   0   0   1 = 1 an
    #   0   1   x = 2 sg an
    #   1   x   x = 4 tg an

    "pinMonitor": [[0, 0, 0]] * ControllerConfig["PinCount"],
}

HTML = {
    "main": "",
    "assist": "",
}

lsp_profile = {
    0: {
        "pins": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "pwm_range": "130",
        "pin_modes": "pwm",
        "decay_factor": "0.02",
        "SD_low": "0.3",
        "SD_high": "0.6",
        "attenuate_pct": "80",
        "light_delay": "0.0",
    },
    1: {
        "pins": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "pwm_range": "150",
        "pin_modes": "pwm",
        "decay_factor": "0.03",
        "SD_low": "0.3",
        "SD_high": "0.75",
        "attenuate_pct": "0",
        "light_delay": "0.0",
    },
    2: {
        "pins": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "pwm_range": "130",
        "pin_modes": "onoff",
        "decay_factor": "0.02",
        "SD_low": "0.5",
        "SD_high": "0.6",
        "attenuate_pct": "0.0",
        "light_delay": "20"
    },
    3: {
        "pins": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "pwm_range": "100",
        "pin_modes": "onoff",
        "decay_factor": "0.05",
        "SD_low": "0.3",
        "SD_high": "0.8",
        "attenuate_pct": "0.0",
        "light_delay": "30"
    }
}

thread_group_mode = {
    "noise": {
        "min": 0,
        "max": 100,
        "delay": 0.1,
        "factor": 3,
        "high": 3,
        "octave": 3,
        "mode": "noise"
    },
    "sin": {
        "min": 0,
        "max": 100,
        "delay": 0.1,
        "period": 3,
        "mode": "sin"
    }
}
thread_group_profile = {
    0: thread_group_mode["noise"],
    1: None,
    2: None,
    3: None,
}
thread_single_profile = {
    0: thread_group_mode["noise"],
    1: None,
    2: None,
    3: None,
}
'''
@route("/set/<mode>/<nr>")
@route("/set_lsp_conf/<module>/<value>")
@route("/set_lsp_profile/<nr>")
@route("/set_tg_conf/<module>/<value>")
@route("/set_tg_profile/<nr>")
@route("/set_tg_mode/<mode>")
@route("/flip_state")
@route("/reset_pwm")
@route("/save_tmp_value/<value>")
'''


#################################################################################
#                           HTML
#################################################################################
@route("/select/<cur>")
def load_html(cur):
    if cur in ["standard", "ThreadSingle", "ThreadGroup", "lsp"]:
        HTML["main"] = cur
        HTML["assist"] = ""
    else:
        HTML["assist"] = cur
    return getHtml()


def getHtml():
    main = HTML["main"]
    assist = HTML["assist"]
    result = html["structure"]
    style = ""
    head = ""
    body = ""

    #########################################################
    #  edit style, head, add extension, edit pin table
    #########################################################
    if assist == "config":
        # stylepytho
        style += html["style"] + html["style_extension"]
        # head
        table_head = html["table_head"].replace("_" + main, "border_green")
        head += "<table>" + table_head + "</table>"
        # body
        if main == "standard":
            body += "<table>" + html[main + "_" + assist] + "</table>"
        elif main == "ThreadSingle":
            config = html["ThreadSingle_extension_profiles"].replace(
                "_tsProfile" + str(controller["ThreadSingleProfile"]), "border_green")
            config += html["ThreadGroup_extension_config"].replace(
                "_" + thread_single_profile[controller["ThreadSingleProfile"]]["mode"], "border_green")
            content = html["ThreadGroup_config_" + thread_single_profile[controller["ThreadSingleProfile"]]["mode"]]
            for name, value in thread_single_profile[controller["ThreadSingleProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "ThreadGroup":
            config = html["ThreadGroup_extension_profiles"].replace(
                "_tgProfile" + str(controller["ThreadGroupProfile"]), "border_green")
            config += html["ThreadGroup_extension_config"].replace(
                "_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"], "border_green")
            content = html["ThreadGroup_config_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"]]
            for name, value in thread_group_profile[controller["ThreadGroupProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "lsp":
            config = html["lsp_extension"].replace("_lspProfile" + str(controller["lspProfile"]), "border_green")
            content = html["lsp_config"]
            for name, value in lsp_profile[controller["lspProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
            print(body)

    elif main == "standard":
        # style
        style += html["style"]
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        if assist == "dc" or assist == "fq":
            table_extension = html["pwm"]
            table_head += table_extension.replace("_" + assist, "green")
        else:
            table_extension = html["table_head_extension"]
            if controller[main]:
                table_extension = table_extension.replace("button red", "button green")
            table_head += table_extension
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(0)

    elif main == "ThreadSingle":
        # style
        style += html["style"]
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        table_extension = html["table_head_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["ThreadSingle_extension_profiles"].replace(
            "_tsProfile" + str(controller["ThreadSingleProfile"]), "border_green")
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(1)

    elif main == "ThreadGroup":
        # style
        style += html["style"]
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        table_extension = html["table_head_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["ThreadGroup_extension_profiles"].replace(
            "_tgProfile" + str(controller["ThreadGroupProfile"]), "border_green")
        table_head += html["ThreadGroup_extension_set"].replace("_" + assist, "border_green")
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(2)

    elif main == "lsp":
        # style
        style += html["style"]
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")

        if assist == "lsp_table":
            table = html["pin_table"]
            print(ControllerConfig["PinsInUse"])
            for pin in ControllerConfig["PinsInUse"]:
                print(pin)
                if pin in lsp_profile[controller["lspProfile"]]["pins"]:
                    table = table.replace("PIN" + str(pin) + "_", "")
                    print("add")
                else:
                    table = table.replace("PIN" + str(pin) + "_", "border_")
                    print("border")
            body += "<table>" + table + "</table>"
        else:
            table_extension = html["table_head_extension"]
            if controller[main]:
                table_extension = table_extension.replace("button red", "button green")
            table_head += table_extension
        # main specific extension
        table_head += html["lsp_extension"].replace("_lspProfile" + str(controller["lspProfile"]), "border_green")
        head += "<table>" + table_head + "</table>"

    result = result.replace("STYLE", style)
    result = result.replace("HEAD", head)
    result = result.replace("BODY", body)
    return result


def pin_table(cur):
    table = html["pin_table"]
    for pin in ControllerConfig["PinsInUse"]:
        # mark blocked pins black
        if controller["lsp"] and pin in lsp_profile[controller["lspProfile"]]["pins"]:
            if controller["pinMonitor"][pin][cur]:
                table = table.replace("PIN" + str(pin) + "_", "black PIN" + str(pin) + "_")
            else:
                table = table.replace("PIN" + str(pin) + "_", "border_black PIN" + str(pin) + "_")
        elif controller["pinMonitor"][pin][cur]:
            table = table.replace("PIN" + str(pin) + "_", "")
        else:
            table = table.replace("PIN" + str(pin) + "_", "border_")
    return "<table>" + table + "</table>"


@route("/")
def web():
    return load_html("standard")


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
    run(host=HOST, port=PORT)
