from bottle import route
from config import ControllerConfig


html = {
    "structure":
        """
        <html>
        <head>
        <meta name="viewport" content="width=device-width"/>
        <style>
            body {
                background-color: black;
                color: white;
            }
    STYLE
        </style>
        </head>
        <body>
    HEAD
    BODY
        </body>
        </html>
""",

    "table_head":
        """
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/select/standard'" class="head _standard" value="IO">
                <input type=button onClick="location.href='/select/ThreadGroup'" class="head _ThreadGroup" value="Group">
                <input type=button onClick="location.href='/select/lsp'" class="head _lsp" value="LSP">
            </td>
        </tr>
""",

    "table_head_extension":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/flip_state'" class="button red" value="State"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/select/config'" class="button" value="Config"></td>
        </tr>
""",

    "ThreadGroup_extension_profiles":
        """
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/set_tg_profile/0'" class="button _tgProfile0" value="P0">
                <input type=button onClick="location.href='/set_tg_profile/1'" class="button _tgProfile1" value="P1">
                <input type=button onClick="location.href='/set_tg_profile/2'" class="button _tgProfile2" value="P2">
                <input type=button onClick="location.href='/set_tg_profile/3'" class="button _tgProfile3" value="P3">
                <input type=button onClick="location.href='/set_tg_profile/4'" class="button _tgProfile4" value="P4">
                <input type=button onClick="location.href='/set_tg_profile/5'" class="button _tgProfile5" value="P5">
            </td>
        </tr>
""",

    "ThreadGroup_extension_set":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/select/select'" class="button _select" value="Select"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/select/adjust'" class="button _adjust" value="Adjust"></td>
        </tr>
""",

    "ThreadGroup_extension_config":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/set_tg_mode/noise'" class="button _noise" value="Noise"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/set_tg_mode/sin'" class="button _sin" value="Sin"></td>
        </tr> 
""",

    "ThreadGroup_config_sin":
        """
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="current _min" size="12">
                <label for="c0"> Min.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/min/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="current _max" size="12">
                <label for="c1"> Max.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/max/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _delay size="12">
                <label for="c2">Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _period size="12">
                <label for="c3">Period.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/delay/'+ c3.value" class="button set"
                       value="Set">
            </td>
        </tr>
""",

    "ThreadGroup_config_noise":
        """
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="current _min" size="12">
                <label for="c0"> Min.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/min/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="current _max" size="12">
                <label for="c1"> Max.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/max/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _delay size="12">
                <label for="c2">Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c3" maxlength="10" placeholder="current _high" size="12">
                <label for="c3"> High.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/high/'+ c3.value"
                       class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c4" maxlength="10" placeholder="current _factor" size="12">
                <label for="c4"> Factor.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/factor/'+ c4.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c5" maxlength="10" placeholder="current _octave" size="12">
                <label for="c5"> Octave.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/octave/'+ c5.value" class="button set"
                       value="Set">
            </td>
        </tr>
""",

    "lsp_extension":
        """
        <tr>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/0'" class="button _lspProfile0"
                value="P0"></td>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/1'" class="button _lspProfile1"
                value="P1"></td>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/2'" class="button _lspProfile2"
                value="P2"></td>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/3'" class="button _lspProfile3"
                value="P3"></td>
        </tr>
""",

    "lsp_config":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/select/lsp_pins'" class="button head black" 
                        value="Pins LSP"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/lightshowpi_update'" class="button head green"
                       value="Update"></td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="current _pwm_range" size="12">
                <label for="c0"> PWM Value.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/pwm_range/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="current _pin_modes" size="12">
                <label for="c1"> Light Mode.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/pin_modes/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _light_delay" size="12">
                <label for="c2"> Light Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/light_delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c3" maxlength="10" placeholder="current _attenuate_pct" size="12">
                <label for="c3"> Attenuate %.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/attenuate_pct/'+ c3.value"
                       class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c4" maxlength="10" placeholder="current _decay_factor" size="12">
                <label for="c4"> Decay Factor.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/decay_factor/'+ c4.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c5" maxlength="10" placeholder="current _SD_low" size="12">
                <label for="c5"> SD low.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/SD_low/'+ c5.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c6" maxlength="10" placeholder="current _SD_high" size="12">
                <label for="c6"> SD high.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/SD_high/'+ c6.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/set_lsp_conf/reset/99'" class="button reset"
                       value="Reset Configuration">
            </td>
        </tr>
""",

    "style": """            
            .yellow {
                background-color: #FFD800;
            }
            .border_yellow {
                background-color: white;
                color: black;
                border: 2px solid #FFD800;
            }   
            .blue {
                background-color: #000099;
                color: white;
            }
            .border_blue {
                background-color: white;
                color: black;
                border: 2px solid #000099;
            }
            .green {
                background-color: #009900;
                color: white;
            }
            .border_green {
                background-color: white;
                color: black;
                border: 2px solid #009900;
            }
            .red {
                background-color: #cc0000;
                color: white;
            }
            .border_red {
                background-color: white;
                color: black;
                border: 2px solid #cc0000;
            }
    
            .set {
                font-size: 10px;
                margin: 4px 2px;
                border: 2px solid #696969;
                border-radius: 2px;
                background-color: #009900;
            }
    
            .reset {
                background-color: grey;
                color: white;
            }
            .button {
                color: black;
                padding: 4px 8px;
                font-size: 16px;
                margin: 4px 2px;
                width: 100%;
                cursor: pointer;
                display: inline-block;
            }
    
            .head {
                color: black;
                padding: 5px 11px;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                display: inline-block;
                border: 2px solid #696969;
                border-radius: 8px;
                background-color: #e7e7e7e7;
            }
""",

    "style_extension": """
            .active {
                background-color: grey;
            }
            .modal {}
            .popup {}""",

    "pin_table": """
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/99/99'" class="button reset" value="All"></td>
            <td>
                <input type=button onClick="location.href='/set/99/99/0'" class="button red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/99/99/1'" class="button green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/99/99/2'" class="button blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/4/99'" class="button" value="Tisch"></td>
            <td>
                <input type=button onClick="location.href='/set/12/99/99'" class="button PIN12red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/13/99/99'" class="button PIN13green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/14/99/99'" class="button PIN14blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/2/99'" class="button" value="Schrank L"></td>
            <td>
                <input type=button onClick="location.href='/set/6/99/99'" class="button PIN6red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/7/99/99'" class="button PIN7green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/8/99/99'" class="button PIN8blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/0/99'" class="button" value="Spiegel 0"></td>
            <td>
                <input type=button onClick="location.href='/set/0/99/99'" class="button PIN0red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/1/99/99'" class="button PIN1green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/2/99/99'" class="button PIN2blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/3/99'" class="button" value="Spiegel 1"></td>
            <td>
                <input type=button onClick="location.href='/set/9/99/99'" class="button PIN9red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/10/99/99'" class="button PIN10green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/11/99/99'" class="button PIN11blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/1/99'" class="button" value="Schrank R"></td>
            <td>
                <input type=button onClick="location.href='/set/3/99/99'" class="button PIN3red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/4/99/99'" class="button PIN4green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/5/99/99'" class="button PIN5blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/7/99'" class="button" value="Tuer"></td>
            <td>
                <input type=button onClick="location.href='/set/24/99/99'" class="button PIN24red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/25/99/99'" class="button PIN25green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/26/99/99'" class="button PIN26blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/5/99'" class="button" value="Dach"></td>
            <td>
                <input type=button onClick="location.href='/set/27/99/99'" class="button PIN27red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/19/99/99'" class="button PIN19green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/20/99/99'" class="button PIN20blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/99/6/99'" class="button" value="Bett"></td>
            <td>
                <input type=button onClick="location.href='/set/21/99/99'" class="button PIN21red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/22/99/99'" class="button PIN22green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/23/99/99'" class="button PIN23blue" value="Blue"></td>
        </tr>
""",

}
controller = {
    # global state
    "standard": 0,
    "ThreadGroup": 0,
    "lsp": 0,

    # current
    "lspProfile": 0,
    "ThreadGroupProfile": 0,
    "ThreadGroupMode": "sin",

    # access check
    "standardMonitor": [0] * ControllerConfig["PinCount"],
    "ThreadGroupMonitor": [0] * ControllerConfig["PinCount"],
    "lspMonitor": [0] * ControllerConfig["PinCount"],
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
thread_group_profile = {
    0: None,
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
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

@route("/select/<cur>")
def load_html(cur):
    if cur in ["standard", "ThreadGroup", "lsp"]:
        HTML["main"] = cur
        HTML["assist"] = None
    else:
        HTML["assist"] = cur
    return getHtml()


def getHtml():
    main = HTML["main"]
    assist = HTML["assist"]
    result = html["structure"]

    ################################################
    #  edit style, head, extension, pin table
    ################################################
    if assist[0:6] == "config":
        # style
        result = result.replace("STYLE", html["style"] + html["style_extension"])
        # head
        table_head = html["table_head"].replace("_" + main, "border_green")
        result = result.replace("HEAD", "<table>" + table_head + "</table>")
        # config
        if main == "standard":
            return result.replace("BODY", "<table>" + html[main + "_" + assist] + "</table>")
        if main == "ThreadGroup":
            config = html["ThreadGroup_extension_profiles"].replace("_tgProfile" + str(controller["ThreadGroupProfile"]), "border_green")
            config += html["ThreadGroup_extension_config"].replace("_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"], "border_green")
            content = html["ThreadGroup_config_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"]]
            for name, value in thread_group_profile[controller["ThreadGroupProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            return result.replace("BODY","<table>" + config + "</table>")
        if main == "lsp":
            config = html["lsp_extension"].replace("_lspProfile" + str(controller["lspProfile"]), "border_green")
            content = html["lsp_config"]
            for name, value in lsp_profile[controller["lspProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            return result.replace("BODY","<table>" + config + "</table>")

        return result

    if main == "standard":
        # style
        result = result.replace("STYLE", html["style"])
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        table_extension = html["table_head_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        result = result.replace("HEAD", "<table>" + table_head + "</table>")
        # pin table
        # do sth
        return result.replace("BODY", "123")

    if main == "ThreadGroup":
        # style
        result = result.replace("STYLE", html["style"])
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        table_extension = html["table_head_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html ["ThreadGroup_extension_profiles"].replace("_tgProfile" + str(controller["ThreadGroupProfile"]), "border_green")
        table_head += html["ThreadGroup_extension_set"].replace("_" + assist, "border_green")
        result = result.replace("HEAD", "<table>" + table_head + "</table>")
        # pin table
        # do sth
        return result.replace("BODY", "123")

    if main == "lsp":
        # style
        result = result.replace("STYLE", html["style"])
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        table_extension = html["table_head_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["lsp_extension"].replace("_lspProfile" + str(controller["lspProfile"]), "border_green")
        result = result.replace("HEAD", "<table>" + table_head + "</table>")
        # pin table
        # do sth
        return result.replace("BODY", "123")
    ################################################
    #       edit pin table
    ################################################

    # check highest pins first
    for i in range(len(ControllerConfig["PinInUse"]) - 1, -1, -1):
        pin = ControllerConfig["PinInUse"][i]
        if TMP["pwmm_states"][pin]:
            table = table.replace("PIN" + str(pin), "")
        else:
            table = table.replace("PIN" + str(pin), "border_")
    if main == "s"

    return result
