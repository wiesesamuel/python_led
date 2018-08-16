# coding: utf8
import os
# GPIO library has the BCM mode or the BOARD mode
GPIO_mode = "BCM"
# Group Thread uses the defined 2D List of ControllerConfig
Default_Thread_Group = "Stripes"
PinConfig = {
    # GPIO library only takes values up to 100
    # by using values up to 255 factor has to be 2.55
    # by using values up to 100 factor has to be 1.0
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
    "GPIO_mode": GPIO_mode
}
ControllerConfig = {
    "PinCount": 28,  # has to be the highest pin nr in use +1
    "PinsInUse": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    "stripe": [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [9, 10, 11],
                [12, 13, 14],
                [27, 19, 20],
                [21, 22, 23],
                [24, 25, 26]
                ],
    "color": [[0, 3, 6, 9, 12, 27, 21, 24],   # red
               [1, 4, 7, 10, 13, 19, 22, 25],  # green
               [2, 5, 8, 11, 14, 20, 23, 26]   # blue
               ],
    "Group": [[0, 1, 2,4,7,8],
              [11, 13, 15, 21]
              ],
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
CONFIG_PATH = os.path.abspath(__file__)
PROJECT_DIR = os.path.split(CONFIG_PATH)[0]
HOME_DIR = os.path.split(PROJECT_DIR)[0]

JSON_FILES = {
    "mono": os.path.join(PROJECT_DIR, "mono.json"),
    "tmp": os.path.join(PROJECT_DIR, "tmp.json"),
    "lsp": os.path.join(PROJECT_DIR, "lsp.json"),
    "pwm": os.path.join(PROJECT_DIR, "pwm.json"),
    "pwmm": os.path.join(PROJECT_DIR, "pwmm.json"),
    "rgb": os.path.join(PROJECT_DIR, "rgb.json"),
    "html": os.path.join(PROJECT_DIR, "html.json"),
    "lsp_profiles": os.path.join(PROJECT_DIR, "lsp_profiles.json"),
}
CONFIGURATION = {
    "mono": {
        "default": {
            "dc": PinConfig["brightness"]["default"],
            "fq": PinConfig["frequency"]["default"]
        },
        "profiles": [None] * ControllerConfig["PinCount"],
    },

    "single": {
        "selected_profile": 0,
        "profile": {
            0: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "period": 3,
                "name": "sin"
            },
            1: {
                "timestamp": 1,
                "min": 10,
                "max": 80,
                "delay": 0.1,
                "period": 5,
                "name": "sin"
            },
            3: {
                "timestamp": 1,
                "min": 30,
                "max": 90,
                "delay": 0.1,
                "period": 3,
                "name": "sin"
            },
            4: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "factor": 3,
                "high": 3,
                "octave": 3,
                "name": "nse"
            }
        },
        "default": {
            "noise": {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "factor": 3,
                "high": 3,
                "octave": 3,
                "name": "nse"
            },
            "sin": {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "period": 3,
                "name": "sin"
            }
        },
        "profiles": [None] * ControllerConfig["PinCount"],
    },

    "group": {
        "selected_profile": 0,
        "profile": {
            0: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "period": 3,
                "name": "sin"
            },
            1: {
                "timestamp": 1,
                "min": 10,
                "max": 80,
                "delay": 0.1,
                "period": 5,
                "name": "sin"
            },
            3: {
                "timestamp": 1,
                "min": 30,
                "max": 90,
                "delay": 0.1,
                "period": 3,
                "name": "sin"
            },
            4: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "factor": 3,
                "high": 3,
                "octave": 3,
                "name": "nse"
            }
        },
        "default": {
            "noise": {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "factor": 3,
                "high": 3,
                "octave": 3,
                "name": "nse"
            },
            "sin": {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "period": 3,
                "name": "sin"
            }
        },
        "profiles": [None] * ControllerConfig["PinCount"],
    },

    "lsp": {
        "selected_profile": 0,
        "default": {
            "pwm_range": "130",
            "pin_modes": "pwm",
            "decay_factor": "0.02",
            "SD_low": "0.3",
            "SD_high": "0.6",
            "attenuate_pct": "80",
            "light_delay": "0.0",
        },
        "profile": {
            0: {
                "pwm_range": "130",
                "pin_modes": "pwm",
                "decay_factor": "0.02",
                "SD_low": "0.3",
                "SD_high": "0.6",
                "attenuate_pct": "80",
                "light_delay": "0.0",
            },
            1: {
                "pwm_range": "150",
                "pin_modes": "pwm",
                "decay_factor": "0.03",
                "SD_low": "0.3",
                "SD_high": "0.75",
                "attenuate_pct": "0",
                "light_delay": "0.0",
            },
            2: {
                "pwm_range": "130",
                "pin_modes": "onoff",
                "decay_factor": "0.02",
                "SD_low": "0.5",
                "SD_high": "0.6",
                "attenuate_pct": "0.0",
                "light_delay": "20"
            },
            3: {
                "pwm_range": "100",
                "pin_modes": "onoff",
                "decay_factor": "0.05",
                "SD_low": "0.3",
                "SD_high": "0.8",
                "attenuate_pct": "0.0",
                "light_delay": "30"
            }
        }
    }
}
for profile in range(ControllerConfig["PinCount"]):
    CONFIGURATION["mono"]["profiles"][profile] = CONFIGURATION["mono"]["default"]
    CONFIGURATION["single"]["profiles"][profile] = CONFIGURATION["single"]["default"]["sin"]
    CONFIGURATION["group"]["profiles"][profile] = CONFIGURATION["group"]["default"]["sin"]

lsp_settings = {
    "target": os.path.join(HOME_DIR, "lightshowpi/config/overrides.cfg"),
    "BCMtoWPI": [30, 31, 8, 9, 7, 21, 22, 11, 10, 13, 12, 14, 26, 23, 15, 16, 27, 0, 1, 24, 28, 29, 3, 4, 5, 6,
                 25, 2],
    "BOARDtoWPI": [],  # not implemented
    "stream": ("mode = stream-in\n" +
               "stream_command_string = mpg123 --stdout --no-resync -q" +
               " --timeout 1 --loop -1 http://127.0.0.1:8000/stream.mp3\n" +
               "input_sample_rate = 48000\n"
               ),
    "GPIO_mode": GPIO_mode,
}

#############################################################################################
#                           raspberry configuration
#############################################################################################
SERVER = "bjoern"
HOST = "0.0.0.0"
PORT = 8080

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

    "head_selection":
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

    "head_selection_extension":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/flip_meta_state'" class="button red" value="State"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/select/config'" class="button" value="Config"></td>
        </tr>
""",

    "thread_profiles":
        """
        <tr>
            <td>
                <input type=button onClick="location.href='/select_profile/0'" class="button _tProfile0" value="P0"></td>
            <td>
                <input type=button onClick="location.href='/select_profile/1'" class="button _tProfile1" value="P1"></td>
            <td>
                <input type=button onClick="location.href='/select_profile/2'" class="button _tProfile2" value="P2"></td>
            <td>
                <input type=button onClick="location.href='/select_profile/3'" class="button _tProfile3" value="P3"></td>
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

    "Thread_mode_selection":
        """
        <tr>
            <td colspan="2">
                <input type=button onClick="location.href='/set_thread_mode/noise'" class="button _noise" value="Noise"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/set_thread_mode/sin'" class="button _sin" value="Sin"></td>
        </tr> 
""",

    "Thread_mode_sin":
        """
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="current _min" size="10">
                <label for="c0"> Min.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/min/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="current _max" size="10">
                <label for="c1"> Max.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/max/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _delay size="10">
                <label for="c2">Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _period" size="10">
                <label for="c3">Period.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/period/'+ c3.value" class="button set"
                       value="Set">
            </td>
        </tr>
""",

    "Thread_mode_noise":
        """
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="current _min" size="10">
                <label for="c0"> Min.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/min/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="current _max" size="10">
                <label for="c1"> Max.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/max/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _delay" size="10">
                <label for="c2">Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c3" maxlength="10" placeholder="current _high" size="10">
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
                <input type="text" name="text" id="c4" maxlength="10" placeholder="current _factor" size="10">
                <label for="c4"> Factor.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_tg_conf/factor/'+ c4.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c5" maxlength="10" placeholder="current _octave" size="10">
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
                <input type=button onClick="location.href='/select/lsp_table'" class="button head black" 
                        value="Pins LSP"></td>
            <td colspan="2">
                <input type=button onClick="location.href='/lightshowpi_update'" class="button head green"
                       value="Update"></td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c0" maxlength="10" placeholder="current _pwm_range" size="10">
                <label for="c0"> PWM Value.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/pwm_range/'+ c0.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c1" maxlength="10" placeholder="current _pin_modes" size="10">
                <label for="c1"> Light Mode.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/pin_modes/'+ c1.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c2" maxlength="10" placeholder="current _light_delay" size="10">
                <label for="c2"> Light Delay.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/light_delay/'+ c2.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c3" maxlength="10" placeholder="current _attenuate_pct" size="10">
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
                <input type="text" name="text" id="c4" maxlength="10" placeholder="current _decay_factor" size="10">
                <label for="c4"> Decay Factor.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/decay_factor/'+ c4.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c5" maxlength="10" placeholder="current _SD_low" size="10">
                <label for="c5"> SD low.</label>
            </td>
            <td>
                <input type=button onClick="location.href='/set_lsp_conf/SD_low/'+ c5.value" class="button set"
                       value="Set">
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="text" name="text" id="c6" maxlength="10" placeholder="current _SD_high" size="10">
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

#############################################################################################
#                           old shit
#############################################################################################
#############################################################################################
#############################################################################################

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
