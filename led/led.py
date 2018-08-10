from time import sleep, time
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO
from bottle import route, run
from .Helper import *
from .Controller import master
from config import *

lsp_profile = {
    1: None,
    2: None,
    3: None,
    4: None,
}
controller = {
    # global state
    "standard": 0,
    "ThreadSingle": 0,
    "ThreadGroup": 0,
    "lsp": 0,

    # current
    "lspProfile": 0,
    "ThreadSingleProfile": 0,
    "ThreadGroupProfile": 0,

    # access check [tg][ts][s]
    #   tg  ts  s
    #   0   0   0 = 0
    #   0   0   1 = 1 an
    #   0   1   x = 2 sg an
    #   1   x   x = 4 tg an

    "pinMonitor": [[0, 0, 0]] * ControllerConfig["PinCount"],
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
    master.flip_master(get_meta())


@route("/set/<mode>/<nr>")
def set_state(mode, nr):
    nr = int(nr)
    if mode == "pin":
        master.flip_single(get_meta(), nr)
    elif mode == "stripe":
        master.unify_group(get_meta(), ControllerConfig["Stripes"][nr])
    elif mode == "color":
        master.unify_group(get_meta(), ControllerConfig["Colors"][nr])


@route("/save_tmp_value/<value>")
def save_tmp_value(value):
    controller["tmp"] = float(value)

#################################################################################
#                           LightShowPi
#################################################################################


@route("/set_lsp_profile/<p>")
def set_lsp_profile(p):
    controller["lsp"] = int(p)
    master.controller[3].set_config(dict(lsp_profile[controller["lsp"]]))
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
                "_tProfile" + str(controller["ThreadSingleProfile"]), "border_green")
            config = html["Thread_mode_selection"].replace(
                "_" + thread_single_profile[controller["ThreadSingleProfile"]]["mode"], "border_green")
            content = html["Thread_mode_" + thread_single_profile[controller["ThreadSingleProfile"]]["mode"]]
            for name, value in thread_single_profile[controller["ThreadSingleProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "ThreadGroup":
            profile += html["thread_profiles"].replace(
                "_tProfile" + str(controller["ThreadGroupProfile"]), "border_green")
            config = html["Thread_mode_selection"].replace(
                "_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"], "border_green")
            content = html["Thread_mode_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"]]
            for name, value in thread_group_profile[controller["ThreadGroupProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "lsp":
            profile += html["lsp_extension"].replace("_lspProfile" + str(controller["lspProfile"]), "border_green")
            content = html["lsp_config"]
            for name, value in lsp_profile[controller["lspProfile"]].items():
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
        table_head = html["head_selection"].replace("_" + main, "border_green")
        table_extension = html["head_selection_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["thread_profiles"].replace(
            "_tProfile" + str(controller["ThreadSingleProfile"]), "border_green")
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(1)

    elif main == "ThreadGroup":
        # style
        style += html["style"]
        # head + extension
        table_head = html["head_selection"].replace("_" + main, "border_green")
        table_extension = html["head_selection_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["thread_profiles"].replace(
            "_tProfile" + str(controller["ThreadGroupProfile"]), "border_green")
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
                if pin in lsp_profile[controller["lspProfile"]]["pins"]:
                    table = table.replace("PIN" + str(pin) + "_", "")
                else:
                    table = table.replace("PIN" + str(pin) + "_", "border_")
            body += "<table>" + table + "</table>"
        else:
            table_extension = html["head_selection_extension"]
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
