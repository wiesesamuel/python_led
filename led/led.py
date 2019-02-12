try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO
from bottle import route, run
from .Helper import *
from .Controller import CTRL, CtrlMaster
import config

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
    ctrl = get_meta()

    # controller mono
    if ctrl == 0:
        # set single pin
        if mode == "pin":
            # adjust config
            if HTML["assist"] in ["dc", "fq"]:
                CTRL[ctrl].set_config_single(nr, temp["tmp_value"], HTML["assist"])
                CtrlMaster.update_single(nr)
            # change state
            else:
                CtrlMaster.flip_single(ctrl, nr)

        # set group
        elif mode in ["stripe", "color"]:
            # adjust config
            if HTML["assist"] in ["dc", "fq"]:
                for nr in config.ControllerConfig[mode][nr]:
                    CTRL[ctrl].set_config_single(nr, temp["tmp_value"], HTML["assist"])
                    CtrlMaster.update_single(nr)
            # change state
            else:
                CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode][nr])

        # set all pins
        elif mode == "PinsInUse":
            # adjust config
            if HTML["assist"] in ["dc", "fq"]:
                for nr in config.ControllerConfig[mode]:
                    CTRL[ctrl].set_config_single(nr, temp["tmp_value"], HTML["assist"])
                    CtrlMaster.update_single(nr)
            # change state
            else:
                CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode])

    # singleThread controller
    elif ctrl == 1:
        if HTML["assist"] == "adjust":
            if mode == "pin":
                CTRL[ctrl].set_configuration_single(nr)
            elif mode in ["stripe", "color"]:
                CTRL[ctrl].set_configuration_group(config.ControllerConfig[mode][nr])
            elif mode == "PinsInUse":
                CTRL[ctrl].set_configuration_group(config.ControllerConfig[mode])

        else:
            if mode == "pin":
                CtrlMaster.flip_single(ctrl, nr)
            elif mode in ["stripe", "color"]:
                CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode][nr])
            elif mode == "PinsInUse":
                CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode])

    # group controller
    elif ctrl == 2:
        if HTML["assist"] == "adjust":
            if mode == "pin":
                CTRL[ctrl].add_member_to_current_group(nr)
            elif mode in ["stripe", "color"]:
                CTRL[ctrl].add_members_to_current_group(config.ControllerConfig[mode][nr])
            elif mode == "PinsInUse":
                CTRL[ctrl].add_members_to_current_group(config.ControllerConfig[mode])
        else:
            if mode == "pin":
                CtrlMaster.flip_single(ctrl, nr)
            elif mode in ["stripe", "color"]:
                CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode][nr])
            elif mode == "PinsInUse":
                CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode])

    # lsp controller
    elif ctrl == 3:
        if mode == "pin":
            CtrlMaster.flip_single(ctrl, nr)
        elif mode in ["stripe", "color"]:
            CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode][nr])
        elif mode == "PinsInUse":
            CtrlMaster.unify_group(ctrl, config.ControllerConfig[mode])

    save_json(CTRL[ctrl].configuration, ctrl)
    return get_html()


@route("/save_tmp_value/<value>")
def save_tmp_value(value):
    temp["tmp_value"] = float(value)
    return get_html()


@route("/select_profile/<nr>")
def change_profile(nr):
    CtrlMaster.change_profile(get_meta(), int(nr))
    return get_html()


# only callable by Thread Group
@route("/select_group/<nr>")
def change_group(nr):
    CTRL[get_meta()].select_group(int(nr))
    return get_html()


@route("/select_light_mode/<nr>")
def select_pro(nr):
    CTRL[get_meta()].select_pro(int(nr))
    if HTML["main"] == "ThreadGroup":
        CTRL[get_meta()].set_configuration_current_group()
    return get_html()


@route("/set_config_values/<input>")
def set_config_values(input):
    ctrl = get_meta()
    CTRL[ctrl].set_config_values(input)
    CTRL[ctrl].update_instances_with_current_profile()
    save_json(CTRL[ctrl].configuration, ctrl)
    return get_html()


@route("/reset_profile")
def reset_profile():
    ctrl = get_meta()
    CTRL[ctrl].configuration["profile"][CTRL[ctrl].configuration["pro"]] = \
        dict(config.CONFIGURATION[HTML["main"]]["profile"][CTRL[ctrl].configuration["pro"]])
    save_json(CTRL[ctrl].configuration, ctrl)
    return get_html()


@route("/reset_profiles")
def reset_profiles():
    CTRL[get_meta()].configuration["profile"] = dict(config.CONFIGURATION[HTML["main"]]["profile"])
    save_json(CTRL[get_meta()].configuration, get_meta())
    return get_html()


#################################################################################
#                           HTML
#################################################################################
@route("/")
def web():
    return load_html("standard")


@route("/select/<cur>")
def load_html(cur):
    if cur in config.Meta:
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
    ctrl = get_meta()
    result = ""
    for key in config.html_formation["head"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["head"][key]

        # edit header, current selected controller is green
        if key == 0:
            tmp = tmp.replace("xXx" + HTML["main"] + "xXx", "border_green")

        # edit controller header state, depends on current master state
        elif key == "master_conf" and CtrlMaster.configuration["master_state"][get_meta()]:
            tmp = tmp.replace("red", "green")

        # add config selection buttons and mark current selected
        elif key == "selection":
            content = ""
            current = CTRL[ctrl].configuration["selected"]
            for nr in range(config.ControllerConfig["SelectionCount"]):

                # get style
                style = "blocked_red"
                if nr == current:
                    if CtrlMaster.configuration["master_state"][get_meta()]:
                        style = "green"
                    else:
                        style = "blocked_green"

                # add button
                content += tmp.replace("_NR_", str(nr))\
                    .replace("_VALUE_", str(nr + 1))\
                    .replace("_SELECTED_", style)

            tmp = "<tr>" + content + "</tr>"

        # generate light-mode buttons and mark current selected
        elif key == "light_modes":
            content = ""
            current = CTRL[ctrl].configuration["pro"]
            for nr in range(len(CTRL[ctrl].configuration["profile"])):

                # use defined name if one is set
                try:
                    name = CTRL[ctrl].configuration["profile"][nr]["name"]
                except Exception:
                    name = "P" + str(nr + 1)

                # get style
                style = "blocked_red"
                if nr == current:
                    if CtrlMaster.configuration["master_state"][get_meta()]:
                        style = "green"
                    else:
                        style = "blocked_green"

                # add button
                content += tmp.replace("_NR_", str(nr))\
                    .replace("_VALUE_", name)\
                    .replace("_SELECTED_", style)

            tmp = "<tr>" + content + "</tr>"

        # generate light-mode colored buttons and mark current selected
        elif key == "light_modes_colored":
            content = ""
            current = CTRL[ctrl].configuration["pro"]
            for nr in range(len(CTRL[ctrl].configuration["profile"])):

                # use defined name if one is set
                try:
                    name = CTRL[ctrl].configuration["profile"][nr]["name"]
                except Exception:
                    name = "P" + str(nr)

                if nr == current:
                    content += tmp.replace("_NR_", str(nr))\
                        .replace("_VALUE_", name)\
                        .replace("_SELECTED_", "border_green")\
                        .replace("_BACKGROUND_", config.random_hex_group_colors[nr])
                else:
                    content += tmp.replace("_NR_", str(nr))\
                        .replace("_VALUE_", name)\
                        .replace("_BACKGROUND_", config.random_hex_group_colors[nr])

            tmp = "<tr>" + content + "</tr>"

        # edit pwm mode, current selected mode is green (fq or dc)
        elif key == "pwm":
            tmp = tmp.replace("xxxxxx" + HTML["assist"] + " red", "border_green")

        # select and adjust button
        elif key == "sel_ad":
            tmp = tmp.replace("xxxxxx" + HTML["assist"] + " blocked_red", "green").replace("_META_", HTML["main"])

        # generate colored select buttons for each group
        elif key == "colored_groups":
            row_count = 0
            content = ""

            for nr in range(config.ControllerConfig["GroupCount"]):
                if nr != CTRL[ctrl].configuration["group"]:
                    content += tmp.replace("_NR_", str(nr)) \
                        .replace("_VALUE_", "G" + str(nr + 1)) \
                        .replace("_BACKGROUND_", config.random_hex_group_colors[nr])
                else:
                    content += tmp.replace("_NR_", str(nr)) \
                        .replace("_VALUE_", "G" + str(nr + 1)) \
                        .replace("_BACKGROUND_", config.random_hex_group_colors[nr]).replace("xxx", "")

                # add row breaks
                row_count += 1
                if row_count > 3:
                    content += "<tr></tr>"
                    row_count = 0

            tmp = content

        # generate select buttons for each group
        elif key == "groups":
            row_count = 0
            content = ""

            for nr in range(config.ControllerConfig["GroupCount"]):
                if nr == CTRL[ctrl].configuration["group"]:
                    content += tmp.replace("_NR_", str(nr))\
                        .replace("_VALUE_", "G" + str(nr + 1))\
                        .replace("_SELECTED_", "border_green")
                else:
                    content += tmp.replace("_NR_", str(nr))\
                        .replace("_VALUE_", "G" + str(nr + 1))

                # add row breaks
                row_count += 1
                if row_count > 3:
                    content += "<tr></tr>"
                    row_count = 0

            tmp = content
        result += tmp
    return "<table>" + result + "</table>"


def get_html_body():
    result = ""
    ctrl = get_meta()

    for key in config.html_formation["body"][HTML["main"]][HTML["assist"]]:
        tmp = config.html["body"][key]

        # generate a value input table for each attribute from current selection
        if key == "table_row_value_input":
            current = CTRL[ctrl].configuration["pro"]
            content = ""
            id_count = 0
            for name, value in CTRL[ctrl].configuration["profile"][current].items():
                if name not in ["timestamp", "id"]:
                    content += tmp.replace("ID_A", "input" + str(id_count))\
                        .replace("NAME_B", "value: " + str(value))\
                        .replace("LABEL_C", name)
                    id_count += 1

            # generate single button to transmit all values
            tmp = config.html["body"]["set_button"]
            href = ""
            for id in range(id_count):
                href += " + input" + str(id) + ".value + '&'"
            tmp = tmp.replace("IDS", href)

            tmp += content

        # for ThreadGroup
        elif key == "mode_selection":
            name = CTRL[get_meta()].configuration["profiles"][
                    CTRL[get_meta()].configuration["selected_profile"]]["name"]
            tmp = tmp.replace("_" + name + " border_red", "green")
            content = config.html["body"][name]
            for name, value in CTRL[get_meta()].configuration["profiles"][
                    CTRL[get_meta()].configuration["selected_profile"]].items():
                content = content.replace("_" + name, str(value))
            tmp += content

        # edit pin table, each pin in use gets a full colored button
        elif key == "pin_table":
            # generate input field
            if config.Settings["generate_table"]:
                content = ""
                count = 0

                for part in config.pin_table_build_plan["head"]:
                    # add reset button
                    if part == "PinsInUse":
                        content += config.html["body"]["table_reset_button"]
                    # generate color button
                    if part == "color":
                        for member in config.pin_table_build_plan[part]:
                            content += config.html["body"]["table_set_button"]\
                                .replace("_MODE_", part)\
                                .replace("_NR_", str(count))\
                                .replace("_CLASS_", str(member))\
                                .replace("_VALUE_", str(member))
                            count += 1
                        count = 0

                # add new line
                content = "<tr>" + content + "</tr>"

                # generate table
                table = ""
                count_stripe = 0
                for stripe in config.ControllerConfig["stripe"]:
                    table += "<tr>"
                    # add stripe button
                    table += config.html["body"]["table_set_button"] \
                        .replace("_MODE_", "stripe") \
                        .replace("_NR_", str(count_stripe)) \
                        .replace("_VALUE_", config.pin_table_build_plan["stripe"][count_stripe])
                    count_stripe += 1
                    count = 0

                    # add pin buttons

                    # colored table
                    if HTML["assist"] == "adjust":

                        # color by membership
                        if HTML["main"] == "ThreadGroup":
                            for pinNr in stripe:
                                if pinNr >= 0:
                                    table += config.html["body"]["table_set_button"] \
                                        .replace("_MODE_", "pin") \
                                        .replace("_NR_", str(pinNr)) \
                                        .replace("_BACKGROUND_", config.random_hex_group_colors[
                                                          CTRL[ctrl].get_membership(pinNr)])\
                                        .replace("_VALUE_", config.pin_table_build_plan["color"][count])
                                else:
                                    table += "<td></td>"
                                count += 1
                            table += "</tr>"

                        # color by light mode
                        if HTML["main"] == "ThreadSingle":
                            for pinNr in stripe:
                                if pinNr >= 0:
                                    table += config.html["body"]["table_set_button"] \
                                        .replace("_MODE_", "pin") \
                                        .replace("_NR_", str(pinNr)) \
                                        .replace("_BACKGROUND_", config.random_hex_group_colors[
                                                        CTRL[ctrl].configuration["selection"]
                                                        [CTRL[ctrl].get_selected()]["mode"][pinNr]["id"][1]]) \
                                        .replace("_VALUE_", config.pin_table_build_plan["color"][count])
                                else:
                                    table += "<td></td>"
                                count += 1
                            table += "</tr>"

                    # standard table
                    else:
                        for pinNr in stripe:
                            if pinNr >= 0:

                                # change class typ
                                adjust = ""
                                on, in_use = CtrlMaster.get_single_state(ctrl, pinNr)
                                if on:
                                    if not in_use:
                                        adjust = "blocked_"
                                else:
                                    adjust = "border_"

                                table += config.html["body"]["table_set_button"] \
                                    .replace("_MODE_", "pin") \
                                    .replace("_NR_", str(pinNr)) \
                                    .replace("_CLASS_", adjust + config.pin_table_build_plan["color"][count]) \
                                    .replace("_VALUE_", config.pin_table_build_plan["color"][count])
                            else:
                                table += "<td></td>"
                            count += 1
                        table += "</tr>"

                tmp = content + table

            else:
                # colored table
                if HTML["assist"] == "adjust":
                    # color by membership
                    if HTML["main"] == "ThreadGroup":
                        for pinNr in range(config.ControllerConfig["PinCount"]):
                            tmp = tmp.replace("""class="button PIN""" + str(pinNr) + "_", """style="background:""" +
                                              config.random_hex_group_colors[CTRL[ctrl].get_membership(pinNr)] +
                                              """" class="button """)
                    # color by light mode
                    if HTML["main"] == "ThreadSingle":
                        for pinNr in range(config.ControllerConfig["PinCount"]):
                            tmp = tmp.replace("""class="button PIN""" + str(pinNr) + "_", """style="background:""" +
                                              config.random_hex_group_colors[CTRL[ctrl].configuration["selection"][CTRL[ctrl].get_selected()]["mode"][pinNr]["id"][1]] +
                                              """" class="button """)
                # normal pin table
                else:
                    for pinNr in range(config.ControllerConfig["PinCount"]):
                        on, in_use = CtrlMaster.get_single_state(ctrl, pinNr)
                        if on:
                            # pin is currently in use
                            if in_use:
                                tmp = tmp.replace("PIN" + str(pinNr) + "_", "")
                            # pin is on but blocked
                            else:
                                tmp = tmp.replace("PIN" + str(pinNr) + "_", "blocked_")
                        # pin is off
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


def set_commands(command):
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
    set_commands(command)
    if len(config.SERVER):
        try:
            run(server=config.SERVER, host=config.HOST, port=config.PORT)
        except Exception:
            print(str(config.SERVER) + " is not supported.")
    else:
        run(host=config.HOST, port=config.PORT)
