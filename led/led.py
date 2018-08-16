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

    # current
    "lspProfile": 0,
    "ThreadSingleProfile": 0,
    "ThreadGroupProfile": 0,

    "tmp": None,
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
            if HTML["main"] == "dc" or HTML["main"] == "fq":
                controller[ctl].set_config_single(nr, situation["tmp_value"], HTML["main"])
            else:
                controller[ctl].flip_single(nr)
        elif mode == "stripe" or mode == "color":
            if HTML["main"] == "dc" or HTML["main"] == "fq":
                controller[ctl].set_config_group(config.ControllerConfig[HTML["main"]], situation["tmp_value"], HTML["main"])
            else:
                controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])

    elif ctl == 1:
        if mode == "pin":
            controller[ctl].flip_single(nr)
        elif mode == "stripe" or mode == "color":
            controller[ctl].unify_group(config.ControllerConfig[HTML["main"]])


@route("/save_tmp_value/<value>")
def save_tmp_value(value):
    situation["tmp_value"] = float(value)


@route("/select_profile/<nr>")
def select_profile(nr):
    controller[get_meta()].select_profile(int(nr))

#################################################################################
#                           LightShowPi
#################################################################################


@route("/set_lsp_profile/<p>")
def set_lsp_profile(p):
    situation["lsp"] = int(p)
    master.controller[3].set_config(dict(lsp_profile[situation["lsp"]]))
    getHtml()


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
        # style
        style += html["style"] + html["style_extension"]
        # head
        table_head = html["head_selection"].replace("_" + main, "border_green")
        profile = ""
        # body
        if main == "standard":
            body += "<table>" + html[main + "_" + assist] + "</table>"
        elif main == "ThreadSingle":
            profile += html["thread_profiles"].replace(
                "_tProfile" + str(situation["ThreadSingleProfile"]), "border_green")
            config = html["Thread_mode_selection"].replace(
                "_" + thread_single_profile[situation["ThreadSingleProfile"]]["mode"], "border_green")
            content = html["Thread_mode_" + thread_single_profile[situation["ThreadSingleProfile"]]["mode"]]
            for name, value in thread_single_profile[situation["ThreadSingleProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "ThreadGroup":
            profile += html["thread_profiles"].replace(
                "_tProfile" + str(situation["ThreadGroupProfile"]), "border_green")
            config = html["Thread_mode_selection"].replace(
                "_" + thread_group_profile[situation["ThreadGroupProfile"]]["mode"], "border_green")
            content = html["Thread_mode_" + thread_group_profile[situation["ThreadGroupProfile"]]["mode"]]
            for name, value in thread_group_profile[situation["ThreadGroupProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "lsp":
            profile += html["lsp_extension"].replace("_lspProfile" + str(situation["lspProfile"]), "border_green")
            content = html["lsp_config"]
            for name, value in lsp_profile[situation["lspProfile"]].items():
                content = content.replace("_" + name, str(value))
            body += "<table>" + content + "</table>"
        table_head += profile
        head += "<table>" + table_head + "</table>"

    elif main == "standard":
        # style
        style += html["style"]
        # head + extension
        table_head = html["head_selection"].replace("_" + main, "border_green")
        if assist == "dc" or assist == "fq":
            table_extension = html["pwm"]
            table_head += table_extension.replace("_" + assist, "green")
        else:
            table_extension = html["head_selection_extension"]
            if situation[main]:
                table_extension = table_extension.replace("button red", "button green")
            table_head += table_extension
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(0)

    elif main == "ThreadSingle":
        # style
        style += html["style"]
        # head + extension
        table_head = html["head_selection"].replace("_" + main, "border_green")
        table_extension = html["head_selection_extension"]
        if situation[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["thread_profiles"].replace(
            "_tProfile" + str(situation["ThreadSingleProfile"]), "border_green")
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(1)

    elif main == "ThreadGroup":
        # style
        style += html["style"]
        # head + extension
        table_head = html["head_selection"].replace("_" + main, "border_green")
        table_extension = html["head_selection_extension"]
        if situation[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["thread_profiles"].replace(
            "_tProfile" + str(situation["ThreadGroupProfile"]), "border_green")
        table_head += html["ThreadGroup_extension_set"].replace("_" + assist, "border_green")
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(2)

    elif main == "lsp":
        # style
        style += html["style"]
        # head + extension
        table_head = html["head_selection"].replace("_" + main, "border_green")

        if assist == "lsp_table":
            table = html["pin_table"]
            for pin in ControllerConfig["PinsInUse"]:
                if pin in lsp_profile[situation["lspProfile"]]["pins"]:
                    table = table.replace("PIN" + str(pin) + "_", "")
                else:
                    table = table.replace("PIN" + str(pin) + "_", "border_")
            body += "<table>" + table + "</table>"
        else:
            table_extension = html["head_selection_extension"]
            if situation[main]:
                table_extension = table_extension.replace("button red", "button green")
            table_head += table_extension
        # main specific extension
        table_head += html["lsp_extension"].replace("_lspProfile" + str(situation["lspProfile"]), "border_green")
        head += "<table>" + table_head + "</table>"

    result = result.replace("STYLE", style)
    result = result.replace("HEAD", head)
    result = result.replace("BODY", body)
    return result


def pin_table(cur):
    table = html["pin_table"]
    for pin in ControllerConfig["PinsInUse"]:
        # mark blocked pins black
        if situation["lsp"] and pin in lsp_profile[situation["lspProfile"]]["pins"]:
            if situation["pinMonitor"][pin][cur]:
                table = table.replace("PIN" + str(pin) + "_", "black PIN" + str(pin) + "_")
            else:
                table = table.replace("PIN" + str(pin) + "_", "border_black PIN" + str(pin) + "_")
        elif situation["pinMonitor"][pin][cur]:
            table = table.replace("PIN" + str(pin) + "_", "")
        else:
            table = table.replace("PIN" + str(pin) + "_", "border_")
    return "<table>" + table + "</table>"


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

def initialize():
        situation[0].


def led_main(command):
    setCommands(command)

    #try:
     #   run(server=config.SERVER, host=config.HOST, port=config.PORT)
    #except Exception:
    run(host=HOST, port=PORT)
