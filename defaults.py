# coding: utf8
import os
import copy
#############################################################################################
#                           raspberry configuration
#############################################################################################


SERVER = "bjoern"
HOST = "0.0.0.0"
PORT = 8085

PinConfig = {
    # GPIO library brightness only takes values up to 100
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
    # GPIO library has the BCM mode or the BOARD mode
    "GPIO_mode": "BCM"
}

ControllerConfig = {
    "SelectionCount": 4,
    "GroupCount": 8,
    "PinCount": 28,  # has to be the highest pin nr in use +1
    "PinsInUse": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    "stripe":  [[0, 1, 2, 3],
                [4, 5, 6, 7],
                [8, 9, 10, 11],
                [12, 13, 14, 19],
                [20, 21, 22, 23],
                [24, 25, 26],
                [27],
                ],
    "color": [
        [0, 4, 8, 12, 20, 24, 27],      # red
        [1, 5, 9, 13, 21, 25],      # green
        [2, 6, 10, 14, 22, 26],     # blue
        [3, 7, 11, 19, 23, 27]      # white
             ],
}

pin_table_build_plan = {
    "head": ["PinsInUse", "color"],
    "color": ["red", "green", "blue", "white"],
    "stripe": ["Leiste 1", "Leiste 2", "Leiste 3", "Leiste 4", "Leiste 5", "Tisch", "Bett", "Eck", "Schrank"]

}

Settings = {
    "verbose": 0,
    "load-json": 0,
    "save-json": 0,
    "generate_table": 1,
}

helpPage = (
    "Calling the help page will also start the program! Bad coding, thats life.\n" +
    "\n" +
    "Usage: Operation\n" +
    "-h || --help             print the help page\n" +
    "-v || --verbose          enables prints at some points\n" +
    "\n" +
    "Usage: Operation [boolean]\n" +
    "-sj || --save-json       " +
    "sets if you always save the current state in a Json [default=" + str(Settings["save-json"]) + "\n" +
    "-lj || --load-json       " +
    "sets if you load and set the old state at start from Json [default=" + str(Settings["load-json"]) + "]\n" +
    "-gt || --generate_table  " +
    "set if you want to generate the pin table gui or use a costume [default=" + str(Settings["generate_table"]) + "]\n"
)

CONFIG_PATH = os.path.abspath(__file__)
PROJECT_DIR = os.path.split(CONFIG_PATH)[0]
HOME_DIR = os.path.split(PROJECT_DIR)[0]

JSON_FILES = {
    "standard": os.path.join(PROJECT_DIR, "mono.json"),
    "tmp": os.path.join(PROJECT_DIR, "tmp.json"),
    "lsp": os.path.join(PROJECT_DIR, "lsp.json"),
    "pwm": os.path.join(PROJECT_DIR, "pwm.json"),
    "pwmm": os.path.join(PROJECT_DIR, "pwmm.json"),
    "rgb": os.path.join(PROJECT_DIR, "rgb.json"),
    "html": os.path.join(PROJECT_DIR, "html.json"),
    "lsp_profiles": os.path.join(PROJECT_DIR, "lsp_profiles.json"),
}

# alias map for each controller
Meta = {
    "standard": 0,
    "ThreadSingle": 1,
    "ThreadGroup": 2,
    "lsp": 3
}

# first named controller has the highest priority
ControllerPriority = ["lsp", "ThreadGroup", "ThreadSingle", "standard"]

# each controller has it own config
CONFIGURATION = {
    # each "selection" contains a "default" dictionary

    "standard": {
        "master_state": 0,

        "default": {
            "state": [0] * ControllerConfig["PinCount"],
            "dc": [PinConfig["brightness"]["default"]] * ControllerConfig["PinCount"],
            "fq": [PinConfig["frequency"]["default"]] * ControllerConfig["PinCount"],
        },
        "selected": 0,
        "selection": [None] * ControllerConfig["SelectionCount"],
    },

    "ThreadSingle": {
        "master_state": 0,

        # profile contains different mode profiles
        "pro": 0,
        "profile": {
            0: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "period": 3,
                "name": "sin",
                "id": [0, 0]
            },
            1: {
                "timestamp": 1,
                "min": 10,
                "max": 80,
                "delay": 0.1,
                "period": 5,
                "name": "sin",
                "id": [0, 1]
            },
            2: {
                "timestamp": 1,
                "min": 30,
                "max": 90,
                "delay": 0.1,
                "period": 3,
                "name": "sin",
                "id": [0, 2]
            },
            3: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "factor": 3,
                "high": 3,
                "octave": 3,
                "name": "nse",
                "id": [1, 3]
            }
        },

        "default": {
            "state": [0] * ControllerConfig["PinCount"],
            "mode": [None] * ControllerConfig["PinCount"]
        },
        "selected": 0,
        "selection": [None] * ControllerConfig["SelectionCount"],
    },

    # ThreadGroup has a fixed size of profiles
    "ThreadGroup": {
        "master_state": 0,
        "group": 0,

        # profile contains different mode profiles
        "pro": 0,
        "profile": {
            0: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "period": 1,
                "name": "rec",
                "id": [0, 0],
                "timeCycle": 1.0,
            },
            1: {
                "timestamp": 1,
                "min": 10,
                "max": 80,
                "delay": 0.1,
                "period": 5,
                "name": "ur",
                "id": [0, 1],
                "timeCycle": 1.0,
            },
            2: {
                "timestamp": 1,
                "min": 30,
                "max": 90,
                "delay": 0.1,
                "period": 3,
                "name": "si",
                "id": [0, 2],
                "timeCycle": 1.0,
            },
            3: {
                "timestamp": 1,
                "min": 0,
                "max": 100,
                "delay": 0.1,
                "factor": 3,
                "high": 3,
                "octave": 3,
                "name": "ve",
                "id": [0, 3],
                "timeCycle": 1.0,
            }
        },

        "default": {
            "state": [0] * ControllerConfig["PinCount"],
            "membership": [0] * ControllerConfig["PinCount"],
            "mode": [None] * ControllerConfig["GroupCount"],
        },
        "selected": 0,
        "selection": [None] * ControllerConfig["SelectionCount"],
    },

    "lsp": {
        "master_state": 0,

        # profile contains different mode profiles
        "pro": 0,
        "profile": {
            0: {
                "pwm_range": "130",
                "pin_modes": "pwm",
                "decay_factor": "0.02",
                "SD_low": "0.3",
                "SD_high": "0.6",
                "attenuate_pct": "80",
                "light_delay": "0.0",
                "name": "P0",
            },
            1: {
                "pwm_range": "150",
                "pin_modes": "pwm",
                "decay_factor": "0.03",
                "SD_low": "0.3",
                "SD_high": "0.75",
                "attenuate_pct": "0",
                "light_delay": "0.0",
                "name": "P1",
            },
            2: {
                "pwm_range": "130",
                "pin_modes": "onoff",
                "decay_factor": "0.02",
                "SD_low": "0.5",
                "SD_high": "0.6",
                "attenuate_pct": "0.0",
                "light_delay": "20",
                "name": "P2",
            },
            3: {
                "pwm_range": "100",
                "pin_modes": "onoff",
                "decay_factor": "0.05",
                "SD_low": "0.3",
                "SD_high": "0.8",
                "attenuate_pct": "0.0",
                "light_delay": "30",
                "name": "P3",
            },
        },

        "default": {
            "state": [0] * ControllerConfig["PinCount"],
            "mode": None
        },
        "selected": 0,
        "selection": [None] * ControllerConfig["SelectionCount"],
    },

    "master": {
        "master_state": [0] * len(Meta),
        "state": [0] * ControllerConfig["PinCount"],
    }
}

# complete profiles and selection for each controller
for target in ["standard", "ThreadSingle", "ThreadGroup", "lsp"]:
    for nr in range(len(CONFIGURATION[target]["selection"])):
        CONFIGURATION[target]["selection"][nr] = copy.deepcopy(CONFIGURATION[target]["default"])
        if "mode" in CONFIGURATION[target]["selection"][nr]:
            if CONFIGURATION[target]["selection"][nr]["mode"] is None:
                CONFIGURATION[target]["selection"][nr]["mode"] = copy.deepcopy(CONFIGURATION[target]["profile"][CONFIGURATION[target]["pro"]])
            else:
                for num in range(len(CONFIGURATION[target]["selection"][nr]["mode"])):
                    CONFIGURATION[target]["selection"][nr]["mode"][num] = copy.deepcopy(CONFIGURATION[target]["profile"][CONFIGURATION[target]["pro"]])


#############################################################################################
#                           LightShowPi configuration
#############################################################################################


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
    "GPIO_mode": PinConfig["GPIO_mode"],
}

# contains all parameters which are needed to be saved as string and not as float
config_profile_string = [
    "name",
    "pwm_range",
    "pin_modes",
    "decay_factor",
    "SD_low",
    "SD_high",
    "attenuate_pct",
    "light_delay"
]

#############################################################################################
#                           HTML configuration
#############################################################################################


# in each part has each controller, for all possible states, a html map
html_formation = {

    "style": {

        # 0 contains the standard html graphic parts
        # set_button contains config button
        # rgb contains rgb buttons
        # info contains ccs display art

        "standard": {
            "": [0, "rgb"],
            "dc": [0, "rgb"],
            "fq": [0, "rgb"],
            "config": [0, "info"],
        },
        "ThreadSingle": {
            "": [0, "rgb"],
            "config": [0, "rgb", "set_button"],
            "adjust": [0, "rgb"],
        },
        "ThreadGroup": {
            "": [0, "rgb"],
            "config": [0, "rgb", "set_button"],
            "adjust": [0, "rgb"],
        },
        "lsp": {
            "": [0, "rgb"],
            "config": [0, "rgb", "set_button"],
            "pins": [0, "rgb", "set_button"],
        }
    },

    "head": {
        # 0 contains the Controller selection buttons
        # master_conf contains the master_state and config buttons
        # pwm contains value input for dc or fq and reset and config buttons
        # selection contains buttons to switch between profiles

        # group_options contains select and adjust buttons
        # groups contains group profile buttons
        # colored_groups contains group profile buttons marked with an color

        "standard": {
            "": [0, "master_conf", "selection"],
            "dc": [0, "selection", "pwm"],
            "fq": [0, "selection", "pwm"],
            "config": [0],
        },
        "ThreadSingle": {
            "": [0, "master_conf", "selection", "group_options"],
            "adjust": [0, "master_conf", "selection", "group_options", "light_modes_colored"],
            "config": [0, "light_modes"],
        },
        "ThreadGroup": {
            "": [0, "master_conf", "selection", "group_options"],
            "config": [0, "light_modes"],
            "adjust": [0, "master_conf", "selection", "group_options", "light_modes", "colored_groups"],
        },
        "lsp": {
            "": [0, "master_conf", "selection", "light_modes"],
            "config": [0, "light_modes"],
        }
    },

    "body": {

        # pin_table contains button table for each led pin
        # config_mono contains special config with timer and other crazy shit
        # table_row_value_input contains buildplan for one input row

        # mode_selection contains ThreadGroup Shit
        # hack contains hack interface
        # nummpad contains button interface

        "standard": {
            "": ["pin_table"],
            "dc": ["pin_table"],
            "fq": ["pin_table"],
            "config": ["config_mono"],
        },
        "ThreadSingle": {
            "": ["pin_table"],
            "config": ["table_row_value_input", "reset_profile"],
            "adjust": ["pin_table"],
        },
        "ThreadGroup": {
            "": ["pin_table"],
            "config": ["table_row_value_input", "reset_profile"],
            "adjust": ["pin_table"],
        },
        "lsp": {
            "": ["pin_table"],
            "config": ["table_row_value_input", "reset_profile"],
        }
    },
}

html = {
    "styles": {
        0: """
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

        "rgb": """
            .blue {
                background-color: #000099;
                color: white;
            }
            .border_blue {
                background-color: white;
                color: black;
                border: 2px solid #000099;
            }
            .blocked_blue {
                background-color: #000055;
                color: white;
                border: 2px solid #000099;
            }
            .white {
                background-color: #999999;
                color: black;
            }
            .blocked_white {
                background-color: #222222;
                color: white;
                border: 2px solid white;
            }
            .border_white {
                background-color: white;
                color: black;
                border: 2px solid #e7e7e7;
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
            .blocked_green {
                background-color: #005500;
                color: white;
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
            .blocked_red {
                background-color: #550000;
                color: white;
                border: 2px solid #990000;
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
    ^   """,

        "color_extension": """            
                .yellow {
                    background-color: #FFD800;
                }
                .border_yellow {
                    background-color: white;
                    color: black;
                    border: 2px solid #FFD800;
                }
        """,

        "set_button": """
            .set {
                font-size: 10px;
                margin: 4px 2px;
                border: 2px solid #696969;
                border-radius: 2px;
                background-color: #009900;
            }
        """,

        "info": """
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

        "numpad": """
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
        """,
    },

    "head": {
        0: """
            <tr>
                <td colspan="4">
                    <input type=button onClick="location.href='/select/standard'" class="head xXxstandardxXx" value="MNO">
                    <input type=button onClick="location.href='/select/ThreadSingle'" class="head xXxThreadSinglexXx" value="SGL">
                    <input type=button onClick="location.href='/select/ThreadGroup'" class="head xXxThreadGroupxXx" value="GRP">
                    <input type=button onClick="location.href='/select/lsp'" class="head xXxlspxXx" value="LSP">
                </td>
            </tr>
        """,

        "master_conf":
            """
            <tr>
                <td colspan="2">
                    <input type=button onClick="location.href='/flip_meta_state'" class="button red" value="State"></td>
                <td colspan="2">
                    <input type=button onClick="location.href='/select/config'" class="button reset" value="Config"></td>
            </tr>
        """,

        "selection":
            """
                <td><input type=button onClick="location.href='/select_profile/_NR_'" class="button _SELECTED_" value="_VALUE_"></td>
            """,

        "light_modes":
            """
                <td><input type=button onClick="location.href='/select_light_mode/_NR_'" class="button _SELECTED_" value="_VALUE_"></td>
            """,

        "light_modes_colored":
            """
                <td><input type=button onClick="location.href='/select_light_mode/_NR_'" style="background:_BACKGROUND_" class="button _SELECTED_" value="_VALUE_"></td>
            """,

        "groups":
            """
                <td><input type=button onClick="location.href='/select_group/_NR_'" class="button _SELECTED_" value="_VALUE_"></td>
            """,

        "colored_groups":
            """
                <td><input type=button onClick="location.href='/select_group/_NR_'" style="background:_BACKGROUND_" class="button xxxborder_green" value="_VALUE_"></td>
            """,

        "group_options":
            """
            <tr>
                <td colspan="2">
                    <input type=button onClick="location.href='/select/_META_'" class="button xxxxxx border_red" value="Select"></td>
                <td colspan="2">
                    <input type=button onClick="location.href='/select/adjust'" class="button xxxxxxadjust border_red" value="Adjust"></td>
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
                           class="button xxxxxxdc red" value="DC"></td>
                <td>
                    <input type=button onClick="location.href='/select/fq'"
                           class="button xxxxxxfq red" value="FQ"></td>
            </tr>
        """,
    },

    "body": {
        "table_row_value_input":
            """  
            <tr>
                <td colspan="4">
                    <input type="text" name="text" id="ID_A" maxlength="10" placeholder="NAME_B" size="10">
                    <label for="ID_A">LABEL_C.</label>
                </td>
            </tr>
        """,

        "set_button":
            """
            <tr>
            <td colspan="4">
                <input type=button onClick="location.href='/set_config_values/' IDS" class="button head green"
                       value="Set Values">
            </td>
            </tr>
        """,

        "mode_selection":
            """
            <tr>
                <td colspan="2">
                    <input type=button onClick="location.href='/set_thread_mode/noise'" class="button _noise border_red" value="Noise"></td>
                <td colspan="2">
                    <input type=button onClick="location.href='/set_thread_mode/sin'" class="button _sin border_red" value="Sin"></td>
            </tr> 
        """,
        "table_build": """
            <tr>
                <td>
                    <input type=button onClick="location.href='/set/PinsInUse/99'" class="button reset" value="All"></td>
                <td>
                    <input type=button onClick="location.href='/set/color/0'" class="button red" value="Red"></td>
                <td>
                    <input type=button onClick="location.href='/set/color/1'" class="button green" value="Green"></td>
                <td>
                    <input type=button onClick="location.href='/set/color/2'" class="button blue" value="Blue"></td>
            </tr>
                    """,

        "table_set_button": """
            <td><input type=button onClick="location.href='/set/_MODE_/_NR_'" style="background:_BACKGROUND_" class="button _CLASS_" value="_VALUE_"></td>
        """,

        "table_reset_button": """
            <td><input type=button onClick="location.href='/set/PinsInUse/99'" class="button reset" value="All"></td>
        """,


        "pin_table": """
            <tr>
                <td>
                    <input type=button onClick="location.href='/set/PinsInUse/99'" class="button reset" value="All"></td>
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

        "reset_profile": """
            <tr>
                <td colspan="4">
                    <input type=button onClick="location.href='/reset_profile'" class="button reset"
                           value="Reset Current Profile">
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <input type=button onClick="location.href='/reset_profiles'" class="button reset"
                           value="Reset All Profiles">
                </td>
            </tr>
        """,

        "config_mono": """
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
        """,

        "numpad": """
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
        """,
    },

    "blueprint": """
            <html>
            <head>
            <meta name="viewport" content="width=device-width"/>
            <style>
                body {
                    background-color: black;
                    color: white;
                }
        xxxxxxSTYLExxxxxx
            </style>
            </head>
            <body>
        yyyyyyHEADyyyyyy
        zzzzzzBODYzzzzzz
            </body>
            </html>
    """,
}

# set values
import random
random_hex_group_colors = [None] * ControllerConfig["GroupCount"]
r = lambda: random.randint(0, 255)
for nr in range(ControllerConfig["GroupCount"]):
    random_hex_group_colors[nr] = ('#%02X%02X%02X' % (r(), r(), r()))

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
