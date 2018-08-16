from time import sleep
from os import system
from .InstancePins import InstancePins
from .InstanceThreads import *
import config
from .Helper import *


class SimpleController:
    configuration = None
    Instances = InstancePins

    def set_master(self, state):
        if self.configuration["master_state"] != state:
            self.configuration["master_state"] = state
            self.update_all()

    def flip_master(self):
        self.configuration["master_state"] = not self.configuration["master_state"]
        self.update_all()

    def set_single(self, nr, state):
        self.configuration["state"][nr] = state
        self.update_single(nr)

    def flip_single(self, nr):
        self.configuration["state"][nr] = not self.configuration["state"][nr]
        self.update_single(nr)

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.configuration["state"][nr]:
                value = 0
                break
        for nr in group:
            self.configuration["state"][nr] = value
            self.update_single(nr)

    def update_all(self):
        for nr in range(len(self.Instances)):
            self.update_single(nr)

    def update_single(self, nr):
        if self.configuration["master_state"] and self.configuration["state"][nr]:
            self.Instances[nr].set_state(1)
        else:
            self.Instances[nr].set_state(0)


class ComplexerController(SimpleController):

    def flip_single(self, nr):
        self.configuration["state"][nr] = not self.configuration["state"][nr]
        if self.configuration["state"][nr]:
            self.set_selected_profile(nr)
        self.update_single(nr)

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.configuration["state"][nr]:
                value = 0
                break
        for nr in group:
            if value:
                self.set_selected_profile(nr)
            self.configuration["state"][nr] = value
            self.update_single(nr)

    def select_profile(self, nr):
        self.configuration["selected_profile"] = nr

    def set_selected_profile(self, nr):
        self.configuration["profiles"][nr] = self.configuration["profile"][self.configuration["selected_profile"]]


class ControllerMono(SimpleController):

    def __init__(self):
        self.configuration = dict(load_configuration("mono"))

    def update_single(self, nr):
        if self.configuration["master_state"] and self.configuration["state"][nr] and \
                not ((CtrlSingle.configuration["master_state"] and CtrlSingle.configuration["state"][nr]) or
                     (CtrlGroup.configuration["master_state"] and CtrlGroup.configuration["state"][nr]) or
                     (CtrlLsp.configuration["master_state"] and CtrlLsp.configuration["state"][nr])
                     ):
            self.Instances[nr].set_brightness(self.configuration["profiles"][nr]["dc"])
            self.Instances[nr].set_frequency(self.configuration["profiles"][nr]["fq"])
            self.Instances[nr].set_state(1)
        else:
            self.Instances[nr].set_state(0)

    def set_config_single(self, nr, value, config):
        self.configuration["profiles"][nr][config] = value
        self.update_single(nr)

    def set_config_group(self, group, value, config):
        for nr in group:
            self.set_config_single(nr, value, config)


class ControllerThreadsSingle(ComplexerController):

    def __init__(self):
        # generate Thread instances for each pin in use
        for pinNr in range(config.ControllerConfig["PinCount"]):
            self.Instances[pinNr] = ThreadGPIOSingle(self.Instances[pinNr])
        self.configuration = dict(load_configuration("single"))

    def update_single(self, pinNr):
        if self.configuration["master_state"] and self.configuration["state"][pinNr] and \
                not ((CtrlGroup.configuration["master_state"] and CtrlGroup.configuration["state"][pinNr]) or
                     (CtrlLsp.configuration["master_state"] and CtrlLsp.configuration["state"][pinNr])):
            self.Instances[pinNr].set_config(self.configuration["profiles"][pinNr])
            if self.Instances[pinNr].isAlive():
                self.Instances[pinNr].restart()
            else:
                self.Instances[pinNr].start()
                self.Instances[pinNr].restart()
        else:
            stop_instance(self.Instances[pinNr])
        CtrlMono.update_single(pinNr)


class ControllerThreadsGroup(ComplexerController):

    # constructor needs to be overworked
    def __init__(self):
        # generate Thread groups for each pin group in config.Default_Thread_Group
        count = 0
        for pinList in config.ControllerConfig[config.Default_Thread_Group]:
            tmp = []
            for pinNr in pinList:
                if pinNr < config.ControllerConfig["PinCount"]:
                    tmp.append(InstancePins[pinNr])
                    self.configuration["group"][pinNr] = count
                else:
                    raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                     config.ControllerConfig["PinCount"] + ")")
            self.Instances[count] = ThreadGPIOGroup(tmp)
            count += 1
        self.configuration = dict(load_configuration("group"))

    def update_single(self, pinNr):
        self.update_group(self.configuration["group"][pinNr])
        CtrlMono.update_all()
        CtrlSingle.update_all()

    def update_group(self, groupNr):
        if self.configuration["master_state"]:
            tmpPinNrs = []
            pinNr = 0
            for groupStatus in self.configuration["group"]:
                if groupStatus == groupNr and \
                        not (CtrlLsp.configuration["master_state"] and CtrlLsp.configuration["state"][pinNr]):
                    tmpPinNrs.append(pinNr)
                pinNr += 1

            tmpInstances = []
            for pinNr in tmpPinNrs:
                if self.configuration["state"][pinNr]:
                    tmpInstances.append(self.Instances[pinNr])

            if len(tmpInstances) > 0:
                self.Instances[groupNr].set_instances(tmpInstances)
                self.set_selected_profile(groupNr)
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
        for groupStatus in self.configuration["group"]:
            if groupStatus > highestGroup:
                highestGroup = groupStatus
        for i in range(highestGroup + 1):
            self.update_group(i)
        CtrlMono.update_all()
        CtrlSingle.update_all()


class ControllerLightshowpi(SimpleController):

    def __init__(self):
        self.configuration = dict(load_configuration("lsp"))

    def update_single(self, nr):
        self.update_all()

    def update_all(self):
        if self.configuration["master_state"]:
            self.update_target()
            system("sudo systemctl restart lightshowpi")
        else:
            system("sudo systemctl kill lightshowpi")
        CtrlMono.update_all()
        CtrlGroup.update_all()
        CtrlSingle.update_all()

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
        for value in self.configuration["state"]:
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
        for value in self.configuration["state"]:
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
