# coding: utf8
import os

PinConfig = {
    # GPIO library only takes values up to 100
    # by using values up to 255 factor has to be 2,55
    # by using values up to 100 factor has to be 1
    "factor": 2.55,
    "brightness": {
        "default": 255,
        "min": 1,
        "max": 255
    },
    "frequency": {
        "default": 200,
        "min": 1,
        "max": 400
    },
    # GPIO library has the BCM mode or the BOARD mode
    "GPIO_mode": "BCM"
}
ControllerConfig = {
    "PinCount": 28,  # has to be the highest pin nr in use +1
    "PinsInUse": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    "Stripes": [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [9, 10, 11],
                [12, 13, 14],
                [27, 19, 20],
                [21, 22, 23],
                [24, 25, 26]
                ],
    "Colors": [[0, 3, 6, 9, 12, 27, 21, 24],   # red
               [1, 4, 7, 10, 13, 19, 22, 25],  # green
               [2, 5, 8, 11, 14, 20, 23, 26]   # blue
               ],
    "BCMtoWPI": [30, 31, 8, 9, 7, 21, 22, 11, 10, 13, 12, 14, 26, 23, 15, 16, 27, 0, 1, 24, 28, 29, 3, 4, 5, 6, 25, 2],
}
Settings = {
    "verbose": 0,
    "load-json": 1,
    "save-json": 0
}
helpPage = (
    "Calling the help page will also start the program! Bad coding, thats life.\n" +
    "\n" +
    "Usage: Operation\n" +
    "-h || --help             prints the help page\n" +
    "-v || --verbose          enables prints at some points\n" +
    "\n" +
    "Usage: Operation [boolean]\n" +
    "-sj || --save-json       sets if you always save the current state in a Json [default=]\n" +
    "-lj || --load-json       sets if you load and set the old state at start from Json [default=]\n"
)
InstanceControll = {
    "InstancesCount": 4,
    "InstancesNames": {
        2: "Stripes",
        3: "Colors",
    },
    "InstanceCount": {
        0: [0] * ControllerConfig["PinCount"],  # Pin Instance
        1: [0] * ControllerConfig["PinCount"],  # Pin Thread instance
        2: [0] * len(ControllerConfig["Stripes"]),  # Stripe Thread instance
        3: [0] * len(ControllerConfig["Colors"]),  # Color Thread instance
    },
    "InstanceStates": [0] * 4
}
#############################################################################################
#                           raspberry configuration
#############################################################################################
SERVER = "bjoern"
HOST = "0.0.0.0"
PORT = 80


#############################################################################################
#                           behavior configuration
#############################################################################################
CONFIG_PATH = os.path.abspath(__file__)
PROJECT_DIR = os.path.split(CONFIG_PATH)[0]
HOME_DIR = os.path.split(PROJECT_DIR)[0]

LSP_DIR_OVERRIDES_FILE = os.path.join(HOME_DIR, "lightshowpi/config/overrides.cfg")

JSON_FILES = {
    "tmp": os.path.join(PROJECT_DIR, "tmp.json"),
    "lsp": os.path.join(PROJECT_DIR, "lsp.json"),
    "pwm": os.path.join(PROJECT_DIR, "pwm.json"),
    "pwmm": os.path.join(PROJECT_DIR, "pwmm.json"),
    "rgb": os.path.join(PROJECT_DIR, "rgb.json"),
    "html": os.path.join(PROJECT_DIR, "html.json"),
    "lsp_profiles": os.path.join(PROJECT_DIR, "lsp_profiles.json"),
}

LSP_STREAM_CONFIG = "mode = stream-in\n" \
                    "stream_command_string = mpg123 --stdout --no-resync -q" \
                    " --timeout 1 --loop -1 " \
                    "http://127.0.0.1:8000/stream.mp3\n" \
                    "input_sample_rate = 48000\n"

LSP_PROFILES_DEFAULT = {
    "0": {
        "PINS": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "PWM_RANGE": "130",
        "PIN_MODES": "pwm",
        "LIGHT_DELAY": "0.0",
        "DECAY_FACTOR": "0.02",
        "SD_LOW": "0.3",
        "SD_HIGH": "0.6",
        "ATTENUATE_PCT": "80"
    },
    "1": {
        "PINS": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "PWM_RANGE": "150",
        "PIN_MODES": "pwm",
        "LIGHT_DELAY": "0.0",
        "DECAY_FACTOR": "0.03",
        "SD_LOW": "0.5",
        "SD_HIGH": "0.75",
        "ATTENUATE_PCT": "0"
    },
    "2": {
        "PINS": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "PWM_RANGE": "130",
        "PIN_MODES": "onoff",
        "LIGHT_DELAY": "0.0",
        "DECAY_FACTOR": "0.02",
        "SD_LOW": "0.5",
        "SD_HIGH": "0.6",
        "ATTENUATE_PCT": "20"
    },
    "3": {
        "PINS": [23, 11, 10, 8, 13, 14, 21, 6, 2, 4],
        "PWM_RANGE": "100",
        "PIN_MODES": "onoff",
        "LIGHT_DELAY": "0.0",
        "DECAY_FACTOR": "0.05",
        "SD_LOW": "0.3",
        "SD_HIGH": "0.8",
        "ATTENUATE_PCT": "30"
    }
}
PWM_SETTINGS_DEFAULT = {
    "dc": 100,
    "fq": 200
}
PWMM_SETTINGS_DEFAULT = {
    "dim": {
        "timestamp": 0,
        "min": 1,
        "max": 99,
        "delay": 0.1,
        "periode": 0.35,
            },
    "glow": {
        "timestamp": 0,
        "min": 30,
        "max": 60,
        "delay": 0.3,
        "periode": 0.35,
             },
    "sin": {
        "timestamp": 0,
        "min": 1,
        "max": 99,
        "delay": 0.1,
        "periode": 0.35,
            },
    "cos": {
        "timestamp": 0,
        "min": 1,
        "max": 99,
        "delay": 0.1,
        "periode": 0.35,
    },
    "noise": {
        "min": 0,
        "max": 100,
        "high": 3,
        "timestamp": 0,
        "factor": 0.2,
        "octave": 2,
        "delay": 0.1,
    }
}
RGB_FADE = {
    "delay": [0.15, 0.14, 0.13],
    "steps_raise": [2, 2, 2],
    "steps_lower": [-2, -2, -2],
    "red": {
        "min": 20,
        "max": 200,
    },
    "green": {
        "min": 20,
        "max": 200,
    },
    "blue": {
        "min": 20,
        "max": 200,
    }
}
ALARM_SETTINGS = {
    "mode": 2,  # sin
    "dic": PWMM_SETTINGS_DEFAULT["sin"],  # mode -> dic
    "pins": PINS_COLORS[2],
    "fq": 4.0,
    "timeout": 600  # seconds
}
SEPERATING_CHAR = [',', ' ', '-']

###
### dictonaries
###
lsp = LSP_PROFILES_DEFAULT["0"]
lsp_profiles = LSP_PROFILES_DEFAULT
html = {
    "main": "io",
    "assist": "dc",
}
pwmm = {
    "map_mode": [0] * PIN_COUNT,
    "map_config": {},
    "config_noise": PWMM_SETTINGS_DEFAULT["noise"],
    "config_sin": PWMM_SETTINGS_DEFAULT["sin"],
    "config_cos": PWMM_SETTINGS_DEFAULT["cos"],
    "config_dim": PWMM_SETTINGS_DEFAULT["dim"],
    "config_glow": PWMM_SETTINGS_DEFAULT["glow"],
}
pwm = {
    "dc": [PWM_SETTINGS_DEFAULT["dc"]] * PIN_COUNT,
    "fq": [PWM_SETTINGS_DEFAULT["fq"]] * PIN_COUNT,
}
tmp = {
    "io_state": 1,
    "pin_states": [0] * PIN_COUNT,
    "pwmm_states": [0] * PIN_COUNT,
    "rgb_pins": [0] * PIN_COUNT,
    "rgb_stripes": [0] * len(PINS_STRIPES),
    "pwmm_state": 0,
    "rgbm_state": 0,
    "pwmm": 0,
    "rgb": 0,
    "lsp": "0",
    "lsp_state": 0,
    "tmp": 100,
    "tmp_values": [
        50,
        50,
        50
    ],
    "tmp_map": [0, 0, 0]
}
rgb = {
    "config": RGB_FADE,
    "map_config": {},
    "map_mode": [0] * len(PINS_STRIPES),
}


#############################################################################################
#                           html configuration
#############################################################################################
HTML_ADAPTATION = {
    "hack": """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/hack/wlan/1'" class="button green" 
                        value="Start Wlan"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/hack/wlan/0'" class="button red" 
                        value="Stop Wlan"></td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/hack/restart/99'" class="button blue"
                       value="Restart LED script">
            </td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/hack/reboot/99'" class="button blue"
                       value="Reboot Raspberry"></td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/hack/syncthing/1'" class="button green"
                       value="Start Syncthing"></td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/hack/syncthing/0'" class="button red"
                       value="Stop Syncthing"></td>
        </tr>
        <tr>
            <td colspan="4"><label>If you use one button below, use both!!!</label></td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/hack/slaughter_threads/99'" class="button red huge"
                       value="Kill all Threads"></td>
        </tr>
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/hack/revive_threads/99'" class="button green huge"
                       value="Revive all Threads"></td>
        </tr>
    """,

    "numpad": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width"/>
            <titel></titel>
            <style>
                body {
                    background-color: grey;
                }
                .button {
                    background-color: none;
                    color: black;
                    padding: 10px 22px;
                    text-decoration: none;
                    display: intline-block;
                    font-size: 16px;
                    margin: 8px 4px;
                    cursor: pointer;
                    border: 2px solid #696969;
                    border-radius: 8px;
                }
        
            </style>
        </head>
        <body>
        <table>
            <tr>
                <td>
                    <input type=button onClick="location.href='/haxxx/7'" class="button" value="7"></td>
                <td>
                    <input type=button onClick="location.href='/haxxx/8'" class="button" value="8"></td>
                <td>
                    <input type=button onClick="location.href='/haxxx/9'" class="button" value="9"></td>
            </tr>
            <tr>
                <td>
                    <input type=button onClick="location.href='/haxxx/4'" class="button" value="4"></td>
                <td>
                    <input type=button onClick="location.href='/haxxx/5'" class="button" value="5"></td>
                <td>
                    <input type=button onClick="location.href='/haxxx/6'" class="button" value="6"></td>
            </tr>
            <tr>
                <td>
                    <input type=button onClick="location.href='/haxxx/1'" class="button" value="1"></td>
                <td>
                    <input type=button onClick="location.href='/haxxx/2'" class="button" value="2"></td>
                <td>
                    <input type=button onClick="location.href='/haxxx/3'" class="button" value="3"></td>
            </tr>
            <tr>
                <td>
                </td>
                <td>
                    <input type=button onClick="location.href='/haxxx/0'" class="button" value="0"></td>
                <td>
                </td>
            </tr>
        </table>
        </body>
        </html>
    """,

    "blue_print": """
        <html>
        <head>
        <meta name="viewport" content="width=device-width"/>
        <titel></titel>
        <style>
            body {
                background-color: black;
                color: white;
            }
            
            .yellow {
                background-color: #FFD800;
            }
            .border_yellow {
                background-color: white;
                color: black;
                border: 2px solid #FFD800;
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
    
            .blue {
                background-color: #000099;
                color: white;
            }
    
            .green {
                background-color: #009900;
                color: white;
            }
    
            .red {
                background-color: #cc0000;
                color: white;
            }
    
            .border_blue {
                background-color: white;
                color: black;
                border: 2px solid #000099;
            }
    
            .border_green {
                background-color: white;
                color: black;
                border: 2px solid #009900;
            }
    
            .border_red {
                background-color: white;
                color: black;
                border: 2px solid #cc0000;
            }
    
            .active {
                background-color: grey;
            }
            .modal {}
            .popup {}
        </style>
        </head>
        <body>
        <table>
            _HEAD
            _INSERTION
            _PIN_TABLE
        </table>
        </body>
        </html>
    """,

    "head": """
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/select/io'" class="head _SELECT_IO" value="IO">
                <input type=button onClick="location.href='/select/pwm'" class="head _SELECT_PWM" value="PWM">
                <input type=button onClick="location.href='/select/pwmm'" class="head _SELECT_PWMM" value="PWMM">
                <input type=button onClick="location.href='/select/rgbm'" class="head _SELECT_RGBM" value="RGBM">
                <input type=button onClick="location.href='/select/lsp'" class="head _SELECT_LSP" value="LSP">
            </td>
        </tr>
    """,

    "config_lsp": """
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
                <input type="text" name="text" id="c0" maxlength="10" placeholder="default 130" size="12">
                <label for="c0"> PWM Value.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/pwm_range/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="pwm / onoff" size="12">
                <label for="c1"> Light Mode.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/pin_modes/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="default 0.0" size="12">
                <label for="c2"> Light Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/light_delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c3" maxlength="10" placeholder="default 80" size="12">
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
                <input type="text" name="text" id="c4" maxlength="10" placeholder="default 0.02" size="12">
                <label for="c4"> Decay Factor.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/decay_factor/'+ c4.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c5" maxlength="10" placeholder="default 0.3" size="12">
                <label for="c5"> SD low.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/SD_low/'+ c5.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c6" maxlength="10" placeholder="default 0.6" size="12">
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

    "config_rgbm": """
        <tr>
            <td>
                <input type=button onClick="location.href='/reset_rgb_config'" class="button reset" value="Reset">
            </td>
            <td>
                <input type=button onClick="location.href='/save_tmp_value/rgbm_config/'+ c0.value"
                       class="button border_green" value="Save">
            </td>
            <td colspan="2">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="value">
            </td>
        </tr>
        <tr>
            <td>
                <h4>Octave</h4>
            </td>
            <td>
                <h5>1</h5>
            </td>
            <td>
                <h5>2</h5>
            </td>
            <td>
                <h5>3</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h4>Delay</h4>
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/delay/0'" class="button set"
                       value="Set">
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/delay/1'" class="button set"
                       value="Set">
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/delay/2'" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td>
                <h4>Raise Steps</h4>
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/steps_raise/0'" class="button set"
                       value="Set">
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/steps_raise/1'" class="button set"
                       value="Set">
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/steps_raise/2'" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td>
                <h4>Lower Steps</h4>
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/steps_lower/0'" class="button set"
                       value="Set">
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/steps_lower/1'" class="button set"
                       value="Set">
            </td>
            <td>
                <input type=button onClick="location.href='/set_rgbm_config/steps_lower/2'" class="button set"
                       value="Set">
            </td>
        </tr>
    """,

    "config_pwmm": """
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/reset/99'"
                       class="button reset"
                       value="Reset"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/save_tmp_value/' + s0.value"
                       class="button border_green"
                       value="Save">
            </td>
            <td>
                <input type="text" name="text" id="s0" maxlength="5" placeholder="value" size="5">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <h2>Settings Mode Noise</h2>
            </td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/reset/noise'"
                       class="button reset"
                       value="Reset"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/noise/min'" class="button"
                       value="Min"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/noise/max'" class="button"
                       value="Max"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/noise/delay'" class="button"
                       value="Delay"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/noise/high'" class="button"
                       value="High"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/noise/factor'" class="button"
                       value="Factor"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/noise/octave'" class="button"
                       value="Octave"></td>
        </tr>
        <tr>
            <td colspan="3">
                <h2>Settings Mode Sinus</h2>
            </td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/reset/sin'"
                       class="button reset"
                       value="Reset"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/sin/min'" class="button"
                       value="Min"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/sin/max'" class="button"
                       value="Max"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/sin/delay'" class="button"
                       value="Delay"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/sin/periode'" class="button"
                       value="Period"></td>
        </tr>
        <tr>
            <td colspan="3">
                <h2>Settings Mode Cosinus</h2>
            </td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/reset/cos'"
                       class="button reset"
                       value="Reset"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/cos/min'" class="button"
                       value="Min"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/cos/max'" class="button"
                       value="Max"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/cos/delay'" class="button"
                       value="Delay"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/cos/periode'" class="button"
                       value="Period"></td>
        </tr>
        <tr>
            <td colspan="3">
                <h2>Settings Mode Glow</h2>
            </td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/reset/mode_glow'"
                       class="button reset"
                       value="Reset"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_glow/min'" class="button"
                       value="Min"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_glow/max'" class="button"
                       value="Max"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_glow/delay'" class="button"
                       value="Delay"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_glow/periode'" class="button"
                       value="Period"></td>
        </tr>
        <tr>
            <td colspan="3">
                <h2>Settings Mode Dim</h2>
            </td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/reset/mode_dim'"
                       class="button reset"
                       value="Reset"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_dim/min'" class="button"
                       value="Min"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_dim/max'" class="button"
                       value="Max"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_dim/delay'" class="button"
                       value="Delay"></td>
            <td>
                <input type=button onClick="location.href='/settings_pwm_mode/mode_dim/periode'" class="button"
                       value="Period"></td>
        </tr>
    """,

    "build_pin_table": """
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

    "pwm": """
        <tr>
            <td>
                <input type=button onClick="location.href='/save_tmp_value/' + t.value"
                       class="button border_green" value="Save"></td>
            <td>
                <input type="text" name="text" id="t" placeholder=" > 0 " size="3"></td>
            <td>
                <input type=button onClick="location.href='/select/dc'"
                       class="button _SELECT_DC" value="DC"></td>
            <td>
                <input type=button onClick="location.href='/select/fq'"
                       class="button _SELECT_FQ" value="FQ"></td>
        </tr>
    """,

    "!pwm": """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/flip_state'" class="button _STATE_SELECT" value="State"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/select/config'" class="button" value="Config"></td>
        </tr>
    """,

    "pwmm": """ 
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/save_pwm_thread/noise'" style="
                color: black;
                padding: 4px 8px;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                display: inline-block;"
                       class="border_green" value="Noise">
                <input type=button onClick="location.href='/save_pwm_thread/glow'" style="
                color: black;
                padding: 4px 8px;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                display: inline-block;"
                       class="border_green" value="Glow">
                <input type=button onClick="location.href='/save_pwm_thread/dim'" style="
                color: black;
                padding: 4px 8px;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                display: inline-block;"
                       class="border_green" value="Dim">
                <input type=button onClick="location.href='/save_pwm_thread/sin'" style="
                color: black;
                padding: 4px 8px;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                display: inline-block;"
                       class="border_green" value="Sinus">
                <input type=button onClick="location.href='/save_pwm_thread/cos'" style="
                color: black;
                padding: 4px 8px;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                display: inline-block;"
                       class="border_green" value="Cosinus"></td>
        </tr>
    """,

    "rgbm": """ 
        <tr>
            <td>
                <input type=button onClick="location.href='/save_rgbm_config_hex/' + h.value"
                       class="button border_green" value="Save">
            </td>
            <td colspan="2">
                <input type="text" name="text" id="h" maxlength="15" placeholder="hex [min, max]">
            </td>
            <td>
                <input type=button onClick="location.href='/select/pallet'" class="button" value="Show"></td>
        </tr>
        <tr>
            <td>
                <input type=button onClick="location.href='/save_rgb_config/' + r.value + '/' + g.value + '/' + b.value"
                       class="button border_green" value="Save">
            </td>
            <td colspan="3">
                <input type="text" name="text" id="r" size="4" placeholder="red">
                <input type="text" name="text" id="g" size="4" placeholder="green">
                <input type="text" name="text" id="b" size="4" placeholder="blue">
                
                <!-- Trigger/Open The Modal -->
                <button id="myBtn">Info</button>
                
                <!-- The Modal -->
                <div id="myModal" class="modal">
                
                  <!-- Modal content -->
                  <div class="modal-content">
                    <span class="close">&times;</span>
                    <p>
                        Green needs two values per color
                        <br>values seperated by
                        <br>"," or " " or "-"
                        <br>Example: [min, max]
                        <br>hex: 000000-ffffff
                        <br>red: 0,255
                        <br>green: 0,0
                        <br>blue: 33,222
                        <br>Red takes one value [max]</p>
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
        </tr>
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/save_rgb_mode/0'"
                       class="button border_green" value="Fade"></td>
            <td>
                <input type=button onClick="location.href='/save_rgb_mode/1'" class="button border_red" value="RGB"></td>
            <td>
                <input type=button onClick="location.href='/save_rgb_mode/99'" class="button border_red" value="Static"></td>
        </tr>
    """,

    "lsp_config_insertion": """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/select/config'" class="button" value="Back">
            </td>
            <td colspan="2">
                <input type=button onClick="location.href='/lightshowpi_update'" class="button green"
                       value="Update"></td>
        </tr>
    """,

    "lsp_profile": """
        <tr>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/0'" class="button _SELECT_0"
                value="P0"></td>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/1'" class="button _SELECT_1"
                value="P1"></td>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/2'" class="button _SELECT_2"
                value="P2"></td>
            <td>
                <input type=button onClick="location.href='/set_lsp_profile/3'" class="button _SELECT_3"
                value="P3"></td>
        </tr>
    """,

    "script": """
        <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/pwm_reset'" class="button reset" value="Reset PWM Values">
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

    "modal": """
        /* The Modal (background) */
        .modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1; /* Sit on top */
            padding-top: 100px; /* Location of the box */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgb(0,0,0); /* Fallback color */
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
        }
        
        /* Modal Content */
        .modal-content {
            background-color: grey;
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
        }
        
        /* The Close Button */
        .close {
            color: #aaaaaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        
        .close:hover,
        .close:focus {
            color: #000;
            text-decoration: none;
            cursor: pointer;
        }
    """,

    "pallet": """
        <tr>
            <td colspan="4">
            <div style="text-align:center; width:404; height:340px; margin-top:0px; margin-bottom:0px; margin-left:auto; margin-right:auto">
            <p id="color01" style="margin:2px">Platzhalter für Colorpalette</p>
            <p style="margin:2px"><a id="color02" href="http://www.seo-welten.de" target="_blank" style="text-decoration:none; font-size:80%; color:#654d1f"></a></p>
            <p style="margin:2px"><script type=">text/javascript">// <![CDATA[
            var fcborder = "ffffff"; var fcolorbg = "f1edda";
            // ]]></script>
            <script type="text/javascript" src="http://www.seo-welten.de/tools/color/userinpalette.js"></script></p>
            </div>
            </td>
        </tr>
    """
}
backup = {
    "kunz_pin_table": """
    <tr>
        <td>
            <input type=button onClick="location.href='/set/99/99/99'" class="button reset" value="Reset"></td>
        <td>
            <input type=button onClick="location.href='/set/99/99/0'" class="button head red" value="Rot"></td>
        <td>
            <input type=button onClick="location.href='/set/99/99/1'" class="button head green" value="Grun"></td>
        <td>
            <input type=button onClick="location.href='/set/99/99/2'" class="button head blue" value="Blau"></td>
    </tr>
    <tr>
        <td>
            <input type=button onClick="location.href='/set/24/99/99'" class="button PIN24red" value="Pin 5"></td>
        <td>
            <input type=button onClick="location.href='/set/4/99/99'" class="button PIN4red" value="Pin 7"></td>
        <td>
            <input type=button onClick="location.href='/set/14/99/99'" class="button PIN14green" value="Pin 15"></td>
        <td>
            <input type=button onClick="location.href='/set/25/99/99'" class="button PIN25yellow" value="Pin 6"></td>
    </tr>
    <tr>
        <td></td>
        <td>
            <input type=button onClick="location.href='/set/2/99/99'" class="button PIN2blue" value="Pin 8"></td>
        <td>
            <input type=button onClick="location.href='/set/17/99/99'" class="button PIN17blue" value="Pin 0"></td>
        <td>
            <input type=button onClick="location.href='/set/18/99/99'" class="button PIN18blue" value="Pin 1"></td>
    </tr>
    <tr>
        <td>
            <input type=button onClick="location.href='/set/99/1/99'" class="button black" value="Schrank"></td>
        <td>
            <input type=button onClick="location.href='/set/3/99/99'" class="button PIN3red" value="Pin 9"></td>
        <td>
            <input type=button onClick="location.href='/set/7/99/99'" class="button PIN7green" value="Pin 11"></td>
        <td>
            <input type=button onClick="location.href='/set/8/99/99'" class="button PIN8blue" value="Pin 10"></td>
    </tr>
    <tr>
        <td>
            <input type=button onClick="location.href='/set/99/0/99'" class="button" value="Bett"></td>
        <td>
            <input type=button onClick="location.href='/set/27/99/99'" class="button PIN27red" value="Pin 2"></td>
        <td>
            <input type=button onClick="location.href='/set/22/99/99'" class="button PIN22green" value="Pin 3"></td>
        <td>
            <input type=button onClick="location.href='/set/23/99/99'" class="button PIN23blue" value="Pin 4"></td>
    </tr>
    <tr>
        <td>
            <input type=button onClick="location.href='/set/99/2/99'" class="button" value="Glas"></td>
        <td>
            <input type=button onClick="location.href='/set/10/99/99'" class="button PIN10blue" value="Pin 12"></td>
        <td>
            <input type=button onClick="location.href='/set/9/99/99'" class="button PIN9blue" value="Pin 13"></td>
        <td>
            <input type=button onClick="location.href='/set/11/99/99'" class="button PIN11blue" value="Pin 14"></td>
    </tr>
    """,
}
# HTML_ADAPTATION["build_pin_table"] = backup["kunz_pin_table"]
