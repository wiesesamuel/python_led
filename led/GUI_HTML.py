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
                <input type=button onClick="location.href='/select/standard'" class="head _standard" value="MSR">
                <input type=button onClick="location.href='/select/ThreadSingle'" class="head _ThreadSingle" value="SGL">
                <input type=button onClick="location.href='/select/ThreadGroup'" class="head _ThreadGroup" value="GRP">
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

   "ThreadSingle_extension_profiles":
        """
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/set_ts_profile/0'" class="button _tsProfile0" value="P0">
                <input type=button onClick="location.href='/set_ts_profile/1'" class="button _tsProfile1" value="P1">
                <input type=button onClick="location.href='/set_ts_profile/2'" class="button _tsProfile2" value="P2">
                <input type=button onClick="location.href='/set_ts_profile/3'" class="button _tsProfile3" value="P3">
            </td>
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
            .black {
                background-color: black;
                color: white;
            }
            .border_black {
                background-color: white;
                color: black;
                border: 2px solid black;
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
                <input type=button onClick="location.href='/set/all'" class="button reset" value="All"></td>
            <td>
                <input type=button onClick="location.href='/set/color/0'" class="button red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/color/1'" class="button green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/color/2'" class="button blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/4'" class="button" value="Tisch"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/12'" class="button PIN12_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/13'" class="button PIN13_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/14'" class="button PIN14_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/2'" class="button" value="Schrank L"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/6'" class="button PIN6_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/7'" class="button PIN7_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/8'" class="button PIN8_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/0'" class="button" value="Spiegel 0"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/0'" class="button PIN0_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/1'" class="button PIN1_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/2'" class="button PIN2_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/3'" class="button" value="Spiegel 1"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/9'" class="button PIN9_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/10'" class="button PIN10_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/11'" class="button PIN11_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/1'" class="button" value="Schrank R"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/3'" class="button PIN3_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/4'" class="button PIN4_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/5'" class="button PIN5_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/7'" class="button" value="Tuer"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/24'" class="button PIN24_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/25'" class="button PIN25_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/26'" class="button PIN26_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/5'" class="button" value="Dach"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/27'" class="button PIN27_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/19'" class="button PIN19_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/20'" class="button PIN20_blue" value="Blue"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/set/stripe/6'" class="button" value="Bett"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/21'" class="button PIN21_red" value="Red"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/22'" class="button PIN22_green" value="Green"></td>
            <td>
                <input type=button onClick="location.href='/set/pin/23'" class="button PIN23_blue" value="Blue"></td>
        </tr>
""",

    "pwm":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/reset_pwm'" class="button reset" value="Reset"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/select/config'" class="button" value="Config"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/save_tmp_value/' + t.value"
                       class="button border_green" value="Save"></td>
            <td>
                <input type="text" name="text" id="t" placeholder=" > 0 " size="3"></td>
            <td>
                <input type=button onClick="location.href='/select/dc'"
                       class="button _dc" value="DC"></td>
            <td>
                <input type=button onClick="location.href='/select/fq'"
                       class="button _fq" value="FQ"></td>
        </tr>
""",

    "standard_config": """
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/select/dc'" class="button reset" value="PWM">
            </td>
        </td>
        <tr>
            <td colspan="4">
                <input type="text" name="text" id="text" maxlength="5" placeholder="minutes">
                <label for="text"> Value for Timer</label>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/set_timer/' + text.value" class="button head black"
                       value="Set Timer">
            </td>
            <td colspan="2">
                <input type=button onClick="location.href='/kill_timer'" class="button reset"
                       value="Kill Timer">
            </td>
        </tr>
    
        <tr>
            <td colspan="4">
            <!-- Trigger/Open The Modal -->
                <button id="myBtn">Info</button>
    
                <!-- The Modal -->
                <div id="myModal" class="modal">
    
                  <!-- Modal content -->
                  <div class="modal-content">
                    <span class="close">&times;</span>
                    <p>
                        Only one Alarm at the time!
                        <br>d = 0 today
                        <br>d = 1 tomorrow...
                        <br>d = d1 day 1 in this month
                        <br>d = d2 day 2 in this month...</p>
                  </div>
    
                </div>
    
                <script>
                // Get the modal
                var modal = document.getElementById('myModal');
    
                // Get the button that opens the modal
                var btn = document.getElementById("myBtn");
    
                // Get the <span> element that closes the modal
                var span = document.getElementsByClassName("close")[0];
    
                // When the user clicks the button, open the modal 
                btn.onclick = function() {
                    modal.style.display = "block";
                }
    
                // When the user clicks on <span> (x), close the modal
                span.onclick = function() {
                    modal.style.display = "none";
                }
    
                // When the user clicks anywhere outside of the modal, close it
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                }
                </script>
    
                <input type="text" name="text" id="t_alarm0" maxlength="3" placeholder="d" size="2">
                <input type="text" name="text" id="t_alarm1" maxlength="2" placeholder="hh" size="2">
                <input type="text" name="text" id="t_alarm2" maxlength="2" placeholder="mm" size="2">
                <label> Value for Alarm</label>
    
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <input type=button
                       onClick="location.href='/set_alarm/' + t_alarm0.value + '/' + t_alarm1.value + '/' + t_alarm2.value"
                       class="button head black"
                       value="Set Alarm">
            </td>
            <td colspan="2">
                <input type=button onClick="location.href='/kill_alarm'" class="button reset" value="Kill Alarm">
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/hard_reset'" class="button reset" value="Hard Reset">
            </td>
            <td colspan="2">
                <input type=button onClick="location.href='/select/hack'" class="button reset"
                       value="Hack Raspberry">
            </td>
        </tr>
""",

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

    "pinMonitor": [[0], [0], [0]] * ControllerConfig["PinCount"],
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
        HTML["assist"] = None
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
        table_head = html["table_head"].replace("_" + main, "border_green")
        head += "<table>" + table_head + "</table>"
        # body
        if main == "standard":
            body += "<table>" + html[main + "_" + assist] + "</table>"
        elif main == "ThreadSingle":
            config = html["ThreadSingle_extension_profiles"].replace("_tsProfile" + str(controller["ThreadSingleProfile"]), "border_green")
            config += html["ThreadSingle_extension_config"].replace("_" + thread_group_profile[controller["ThreadSingleProfile"]]["mode"], "border_green")
            content = html["ThreadSingle_config_" + thread_group_profile[controller["ThreadSingleProfile"]]["mode"]]
            for name, value in thread_group_profile[controller["ThreadSingleProfile"]].items():
                content = content.replace("_" + name, str(value))
            config += content
            body += "<table>" + config + "</table>"
        elif main == "ThreadGroup":
            config = html["ThreadGroup_extension_profiles"].replace("_tgProfile" + str(controller["ThreadGroupProfile"]), "border_green")
            config += html["ThreadGroup_extension_config"].replace("_" + thread_group_profile[controller["ThreadGroupProfile"]]["mode"], "border_green")
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
        table_head += html["ThreadSingle_extension_profiles"].replace("_tsProfile" + str(controller["ThreadSingleProfile"]), "border_green")
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
        table_head += html["ThreadGroup_extension_profiles"].replace("_tgProfile" + str(controller["ThreadGroupProfile"]), "border_green")
        table_head += html["ThreadGroup_extension_set"].replace("_" + assist, "border_green")
        head += "<table>" + table_head + "</table>"
        # pin table
        body += pin_table(2)

    elif main == "lsp":
        # style
        style += html["style"]
        # head + extension
        table_head = html["table_head"].replace("_" + main, "border_green")
        table_extension = html["table_head_extension"]
        if controller[main]:
            table_extension = table_extension.replace("button red", "button green")
        table_head += table_extension
        # main specific extension
        table_head += html["lsp_extension"].replace("_lspProfile" + str(controller["lspProfile"]), "border_green")
        head += "<table>" + table_head + "</table>"

        # pin table
        if assist == "lsp_pins":
            table = html["pin_table"]
            for pin in ControllerConfig["PinInUse"]:
                if pin in lsp_profile[controller["lspProfile"]]["pins"]:
                    table = table.replace("PIN" + str(pin) + "_", "")
                else:
                    table = table.replace("PIN" + str(pin) + "_", "border_")
            body += table

    result = result.replace("STYLE", style)
    result = result.replace("HEAD", head)
    result = result.replace("BODY", body)
    return result


def pin_table(cur):
    table = html["pin_table"]
    for pin in ControllerConfig["PinInUse"]:
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
