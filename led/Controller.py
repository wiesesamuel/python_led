from os import system
from .InstancePins import InstancePins
from .InstanceThreads import *
import config
from .Helper import *


class Controller:

    # every Controller use the same GPIO Pin Instances
    Instances = InstancePins

    def __init__(self, configuration):
        self.configuration = configuration

    def set_master(self, state):
        if self.configuration["master_state"] != state:
            self.configuration["master_state"] = state
            self.update_all()

    def flip_master(self):
        self.configuration["master_state"] = not self.configuration["master_state"]
        self.update_all()

    def flip_single(self, nr):
        self.configuration["selection"][self.configuration["selected"]]["state"][nr] = \
            not self.configuration["selection"][self.configuration["selected"]]["state"][nr]

        self.update_single(nr)

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.configuration["selection"][self.configuration["selected"]]["state"][nr]:
                value = 0
                break
        for nr in group:
            self.configuration["selection"][self.configuration["selected"]]["state"][nr] = value
            self.update_single(nr)

    def update_all(self):
        for nr in range(len(self.Instances)):
            self.update_single(nr)

    def set_single(self, nr, state):
        self.configuration["selection"][self.configuration["selected"]]["state"][nr] = state
        self.update_single(nr)

    def update_single(self, nr):
        if self.configuration["master_state"] and \
                self.configuration["selection"][self.configuration["selected"]]["state"][nr]:

            self.Instances[nr].set_state(1)
        else:
            self.Instances[nr].set_state(0)

    def select_profile(self, nr):
        self.configuration["selected"] = nr

    def select_pro(self, nr):
        self.configuration["pro"] = nr

    def get_single_state(self, nr):
        return self.configuration["selection"][self.configuration["selected"]]["state"][nr]

    def update_profile(self):
        self.configuration["selection"][self.configuration["selected"]]["mode"] = \
            self.configuration["profile"][self.configuration["pro"]]


class ControllerMono(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("standard")))

    def update_single(self, nr):
        if self.configuration["master_state"] and \
                self.configuration["selection"][self.configuration["selected"]]["state"][nr]:

            self.Instances[nr].set_brightness(self.configuration["selection"][self.configuration["selected"]]["dc"][nr])
            self.Instances[nr].set_frequency(self.configuration["selection"][self.configuration["selected"]]["fq"][nr])
            self.Instances[nr].set_state(1)
        else:
            self.Instances[nr].set_state(0)

    def set_config_single(self, nr, value, conf):
        self.configuration["selection"][self.configuration["selected"]][conf][nr] = value
        self.update_single(nr)

    def set_config_group(self, group, value, conf):
        for nr in group:
            self.set_config_single(nr, value, conf)


class ControllerThreadsSingle(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("ThreadSingle")))
        # generate Thread instances for each pin in use
        for pinNr in range(config.ControllerConfig["PinCount"]):
            self.Instances[pinNr] = ThreadGPIOSingle(self.Instances[pinNr],
                                                     self.configuration["profile"][self.configuration["pro"]])

    def update_single(self, nr):
        if self.configuration["master_state"] and \
                self.configuration["selection"][self.configuration["selected"]]["state"][nr]:
            if self.Instances[nr].isAlive():
                self.Instances[nr].restart()
            else:
                self.Instances[nr].start()
                self.Instances[nr].restart()
        else:
            stop_instance(self.Instances[nr])


class ControllerThreadsGroup(Controller):

    # constructor needs to be overworked
    def __init__(self):
        # generate Thread groups for each pin group in config.Default_Thread_Group
        super().__init__(dict(load_configuration("ThreadGroup")))


class ControllerLightshowpi(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("lsp")))
        self.Previous = ""

    def update_single(self, nr):
        self.update_all()

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.configuration["state"][nr]:
                value = 0
                break
        for nr in group:
            self.configuration["state"][nr] = value
        self.update_all()

    def update_all(self):
        if self.configuration["master_state"]:
            self.update_target()
            system("sudo systemctl restart lightshowpi")
        else:
            system("sudo systemctl kill lightshowpi")

    def update_target(self):
        # only update lsp config file if a change was made
        current = self.get_target_text()
        if self.Previous != current:
            try:
                with open(config.lsp_settings["target"], "w") as f:
                    f.write(current)
                    self.Previous = current
            except Exception:
                pass

    def get_target_text(self):
        tmp = "[hardware]\n"
        tmp += ("gpio_pins = " + self.get_lsp_pins() + "\n")
        tmp += self.get_settings_text("pwm_range")

        if not self.get_settings("pin_modes") in ["onoff", "pwm"]:
            self.set_settings("pin_modes", self.configuration["profile"][self.configuration["pro"]]["pin_modes"])

        tmp += self.get_settings_text("pin_modes")
        tmp += "[lightshow]\n"
        tmp += self.get_settings_text("decay_factor")
        tmp += self.get_settings_text("SD_low")
        tmp += self.get_settings_text("SD_high")
        tmp += self.get_settings("attenuate_pct")
        tmp += self.get_settings("light_delay")
        tmp += config.lsp_settings["stream"]

        return tmp

    def get_settings(self, key):
        if self.configuration["profile"][self.configuration["selected"]][key] is not None:
            return self.configuration["selection"][self.configuration["selected"]]["mode"][key]
        else:
            return self.configuration["profile"][self.configuration["pro"]][key]

    def get_settings_text(self, key):
        return key + " = " + self.get_settings(key) + "\n"

    def set_settings(self, key, value):
        self.configuration["profile"][self.configuration["selected"]][key] = value

    def get_lsp_pins(self):
        if config.lsp_settings["GPIO_mode"] == "BCM":
            return self.list_to_string(self.convert_to_WPI("BCMtoWPI"))
        if config.lsp_settings["GPIO_mode"] == "BOARD":
            return self.list_to_string(self.convert_to_WPI("BOARDtoWPI"))
        # User uses WiringPi
        return self.list_to_string(self.convert_to_pins())

    def convert_to_WPI(self, source):
        wpi = []
        pinNr = 0
        for value in self.configuration["selection"][self.configuration["selected"]]["state"]:
            if value:
                try:
                    wpi.append(config.lsp_settings[source][pinNr])
                except IndexError:
                    pass
            pinNr += 1
        return wpi

    def convert_to_pins(self):
        pins = []
        pinNr = 0
        for value in self.configuration["selection"][self.configuration["selected"]]["state"]:
            if value:
                try:
                    pins.append(pinNr)
                except IndexError:
                    pass
            pinNr += 1
        return pins

    @staticmethod
    def list_to_string(list):
        return str(list)[1:-1]


CtrlLsp = ControllerLightshowpi()
CtrlGroup = ControllerThreadsGroup()
CtrlSingle = ControllerThreadsSingle()
CtrlMono = ControllerMono()

CTRL = [CtrlMono, CtrlSingle, CtrlGroup, CtrlLsp]


class MasterController:

    def __init__(self):
        self.configuration = load_configuration("master")

    def set_master(self, ctrl, state):
        if self.configuration["master_state"][ctrl] != state:
            self.configuration["master_state"][ctrl] = state
            CTRL[ctrl].configuration["master_state"] = state
            self.update_all()

    def flip_master(self, ctrl):
        self.configuration["master_state"][ctrl] = not self.configuration["master_state"][ctrl]
        CTRL[ctrl].configuration["master_state"] = self.configuration["master_state"][ctrl]
        self.update_all()

    def set_single(self, ctrl, nr, state):
        self.configuration["state"][ctrl][nr] = state
        CTRL[ctrl].configuration["selection"][self.configuration["selected"][ctrl]]["state"][nr] = state
        self.update_single(nr)

    def flip_single(self, ctrl, nr):
        self.configuration["state"][ctrl][nr] = not self.configuration["state"][ctrl][nr]
        CTRL[ctrl].configuration["selection"][self.configuration["selected"][ctrl]]["state"][nr] = \
            self.configuration["state"][ctrl][nr]
        self.update_single(nr)

    def unify_group(self, ctrl, group):
        value = 1
        for nr in group:
            if self.configuration["state"][ctrl][nr]:
                value = 0
                break
        for nr in group:
            self.configuration["state"][ctrl][nr] = value
            self.update_single(nr)

    def update_all(self):
        for nr in range(config.ControllerConfig["PinCount"]):
            self.update_single(nr)

    def update_single(self, nr):
        free = 1
        for highest_member in config.ControllerPriority:
            ctrl = config.Meta[highest_member]
            if free:
                if self.configuration["master_state"][ctrl] and self.configuration["state"][ctrl][nr]:
                    CTRL[ctrl].set_single(nr, 1)
                    free = 0
                else:
                    CTRL[ctrl].set_single(nr, 0)
            else:
                CTRL[ctrl].set_single(nr, 0)

    def change_profile(self, ctrl, nr):
        print("prev:")
        print(self.configuration)
        self.configuration["selected"][ctrl] = nr
        self.configuration["state"][ctrl] = list(CTRL[ctrl].configuration["selection"][nr]["state"])
        CTRL[ctrl].select_profile(nr)
        self.update_all()
        print("aft:")
        print(self.configuration)

    def get_single_state(self, ctrl, nr):
        on = 0
        inUse = 0
        if self.configuration["state"][ctrl][nr]:
            on = 1
            if CTRL[ctrl].get_single_state(nr):
                inUse = 1
        return on, inUse


CtrlMaster = MasterController()

