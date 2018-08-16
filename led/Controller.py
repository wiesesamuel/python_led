from time import sleep
from os import system
from .InstancePins import InstancePins
from .InstanceThreads import *
import config
from .Helper import *


class ControllerMono:
    master_state = 0

    def __init__(self):
        self.instance = InstancePins
        self.state = [0] * config.ControllerConfig["PinCount"]
        self.configuration = dict(load_configuration("mono"))

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update_single(nr)

    def flip_single(self, nr):
        self.state[nr] = not self.state[nr]
        self.update_single(nr)

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.state[nr]:
                value = 0
                break
        for nr in group:
            self.state[nr] = value
            self.update_single(nr)

    def update_all(self):
        for nr in range(len(self.instance)):
            self.update_single(nr)

    def update_single(self, nr):
        if self.master_state and self.state[nr]:
            self.instance[nr].set_brightness(self.configuration["profiles"][nr]["dc"])
            self.instance[nr].set_frequency(self.configuration["profiles"][nr]["fq"])
            self.instance[nr].set_state(1)
        else:
            self.instance[nr].set_state(0)

    def set_config_single(self, nr, value, config):
        self.configuration["profiles"][nr][config] = value
        self.update_single(nr)

    def set_config_group(self, group, value, config):
        for nr in group:
            self.set_config_single(nr, value, config)


class ControllerThreadsSingle:
    Instances = [None] * config.ControllerConfig["PinCount"]
    state = [0] * config.ControllerConfig["PinCount"]
    master_state = 0

    def __init__(self):
        # generate Thread instances for each pin in use
        for pinNr in config.ControllerConfig["PinsInUse"]:
            if pinNr < config.ControllerConfig["PinCount"]:
                self.Instances[pinNr] = ThreadGPIOSingle(InstancePins[pinNr])
            else:
                raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                 config.ControllerConfig["PinCount"] + ")")
        self.configuration = dict(load_configuration("single"))

    def set_master(self, state):
        if self.master_state != state:
            self.flip_master()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, pinNr, state):
        if self.state[pinNr] != state:
            self.flip_single(pinNr)

    def flip_single(self, pinNr):
        self.state[pinNr] = not self.state[pinNr]
        if self.state[pinNr]:
            self.set_selected_profile(pinNr)
        self.update_single(pinNr)

    def unify_group(self, group):
        value = 1
        for pinNr in group:
            if self.state[pinNr]:
                value = 0
                break
        for pinNr in group:
            if value:
                self.set_selected_profile(pinNr)
            self.state[pinNr] = value
            self.update_single(pinNr)

    def update_single(self, pinNr):
        if self.master_state and self.state[pinNr] and not (CtrlGroup.master_state and CtrlGroup.state[pinNr]):
            self.Instances[pinNr].set_config(self.configuration["profiles"][pinNr])
            if self.Instances[pinNr].isAlive():
                self.Instances[pinNr].restart()
            else:
                self.Instances[pinNr].start()
                self.Instances[pinNr].restart()
        else:
            stop_instance(self.Instances[pinNr])

    def update_all(self):
        for instance in self.Instances:
            self.update_single(instance.pinNr)

    def select_profile(self, nr):
        self.configuration["selected_profile"] = nr

    def set_selected_profile(self, nr):
        self.configuration["profiles"][nr] = self.configuration["profile"][self.configuration["selected_profile"]]


class ControllerThreadsGroup:
    Instances = [None] * config.ControllerConfig["PinCount"]
    state = [0] * config.ControllerConfig["PinCount"]
    group = [0] * config.ControllerConfig["PinCount"]
    master_state = 0

    def __init__(self):
        # generate Thread groups for each pin group in config.Default_Thread_Group
        count = 0
        for pinList in config.ControllerConfig[config.Default_Thread_Group]:
            tmp = []
            for pinNr in pinList:
                if pinNr < config.ControllerConfig["PinCount"]:
                    tmp.append(InstancePins[pinNr])
                    self.group[pinNr] = count
                else:
                    raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                     config.ControllerConfig["PinCount"] + ")")
            self.Instances[count] = tmp
            count += 1
        self.configuration = dict(load_configuration("group"))

    def set_master(self, state):
        if self.master_state != state:
            self.flip_master()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, pinNr, state):
        if self.state[pinNr] != state:
            self.flip_single(pinNr)

    def flip_single(self, pinNr):
        self.state[pinNr] = not self.state[pinNr]
        if self.state[pinNr]:
            self.set_selected_profile(pinNr)
        self.update_group(self.group[pinNr])

    def unify_group(self, group):
        value = 1
        for pinNr in group:
            if self.state[pinNr]:
                value = 0
                break
        for pinNr in group:
            if value:
                self.set_selected_profile(pinNr)
            self.state[pinNr] = value
            self.update_group(self.group[pinNr])

    def update_group(self, groupNr):
        if self.master_state:
            tmpPinNrs = []
            pinNr = 0
            for groupStatus in self.group:
                if groupStatus == groupNr:
                    tmpPinNrs.append(pinNr)
                pinNr += 1

            tmpInstances = []
            for pinNr in tmpPinNrs:
                if self.state[pinNr]:
                    tmpInstances.append(self.Instances[pinNr])

            if len(tmpInstances) > 0:
                self.Instances[groupNr].set_instances(tmpInstances)
                self.Instances[groupNr].set_config(self.configuration["profiles"][groupNr])
                if self.Instances[groupNr].isAlive():
                    self.Instances[groupNr].restart()
                else:
                    self.Instances[groupNr].start()
                    self.Instances[groupNr].restart()
            else:
                stop_instance(self.Instances[groupNr])
        else:
            stop_instance(self.Instances[groupNr])

    def update_all(self):
        highestGroup = 0
        for groupStatus in self.group:
            if groupStatus > highestGroup:
                highestGroup = groupStatus
        for i in range(highestGroup + 1):
            self.update_group(i)

    def set_config(self, groupNr, dic):
        self.configuration[groupNr] = dic
        self.update_group(groupNr)

    def select_profile(self, nr):
        self.configuration["selected_profile"] = nr

    def set_selected_profile(self, nr):
        self.configuration["profiles"][nr] = self.configuration["profile"][self.configuration["selected_profile"]]


class ControllerLightshowpi:
    state = [0] * config.ControllerConfig["PinCount"]
    master_state = 0

    def __init__(self):
        self.configuration = dict(load_configuration("lsp"))

    def set_master(self, state):
        if self.master_state != state:
            self.flip_master()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, pinNr, state):
        if self.state[pinNr] != state:
            self.flip_single(pinNr)

    def flip_single(self, pinNr):
        self.state[pinNr] = not self.state[pinNr]
        self.update_all()

    def unify_group(self, group):
        value = 1
        for pinNr in group:
            if self.state[pinNr]:
                value = 0
                break
        for pinNr in group:
            self.state[pinNr] = value
        self.update_all()

    def update_all(self):
        if self.master_state:
            self.update_target()
            system("sudo systemctl restart lightshowpi")
        else:
            system("sudo systemctl kill lightshowpi")

    def update_target(self):
        with open(config.lsp_settings["target"], "w") as f:
            f.write("[hardware]\n")
            f.write("gpio_pins = " + self.get_lsp_pins() + "\n")
            f.write("pwm_range = " + self.get_settings("pwm_range") + "\n")
            if not self.get_settings("pin_modes") in ["onoff", "pwm"]:
                self.set_settings("pin_modes", self.configuration["default"]["pin_modes"])
            f.write("pin_modes = " + self.get_settings("pin_modes") + "\n")
            f.write("[lightshow]\n")
            f.write("decay_factor = " + self.get_settings("decay_factor") + "\n")
            f.write("SD_low = " + self.get_settings("SD_low") + "\n")
            f.write("SD_high = " + self.get_settings("SD_high") + "\n")
            f.write("attenuate_pct = " + self.get_settings("attenuate_pct") + "\n")
            f.write("light_delay = " + self.get_settings("light_delay") + "\n")
            f.write(config.lsp_settings["stream"])

    def get_settings(self, key):
        if self.configuration["profile"][self.configuration["selected_profile"]][key] is not None:
            return self.configuration["profile"][self.configuration["selected_profile"]][key]
        else:
            return self.configuration["default"][key]

    def set_settings(self, key, value):
        self.configuration["profile"][self.configuration["selected_profile"]][key] = value

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
        for value in self.state:
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
        for value in self.state:
            if value:
                try:
                    pins.append(pinNr)
                except IndexError:
                    pass
            pinNr += 1
        return pins

    def list_to_string(self, list):
        return str(list)[1:-1]

    def select_profile(self, nr):
        self.configuration["selected_profile"] = nr
        self.update_all()


CtrlMono = ControllerMono()
CtrlSingle = ControllerThreadsSingle()
CtrlGroup = ControllerThreadsGroup()
CtrlLsp = ControllerLightshowpi()
