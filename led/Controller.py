from time import sleep
from os import system
from .InstancePins import InstancePins
from .InstanceThreads import *
import config


def stop_instance(instance):
    if instance.running:
        instance.stop()
        while not instance.idle:
            sleep(0.0001)


# add setbrigthness and fq
class ControllerMono:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance
        self.state = [0] * config.ControllerConfig["PinCount"]

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update_single(nr)

    # never in use
    def flip_single(self, nr):
        self.state[nr] = not self.state[nr]
        self.update_single(nr)

    # never in use
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
            self.instance[nr].set_state(1)
        else:
            self.instance[nr].set_state(0)

    def get_state_pin(self, pin):
        return self.state[pin]


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

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, pinNr, state):
        self.state[pinNr] = state
        self.update_single(pinNr)

    def flip_single(self, pinNr):
        self.state[pinNr] = not self.state[pinNr]
        self.update_single(pinNr)

    def unify_group(self, group):
        value = 1
        for pinNr in group:
            if self.state[pinNr]:
                value = 0
                break
        for pinNr in group:
            self.state[pinNr] = value
            self.update_single(pinNr)

    def update_single(self, pinNr):
        if self.master_state and self.state[pinNr]:
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

    def set_config(self, nr, dic):
        self.Instances[nr].set_config(dic)


class ControllerThreadsGroup:
    Instances = [None] * config.ControllerConfig["PinCount"]
    configuration = [None] * config.ControllerConfig["PinCount"]
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

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, pinNr, state):
        self.state[pinNr] = state
        self.update_group(self.group[pinNr])

    def flip_single(self, pinNr):
        self.state[pinNr] = not self.state[pinNr]
        self.update_group(self.group[pinNr])

    def unify_group(self, group):
        values = [1] * len(self.state)
        for pin in group:
            stateNr = 0
            for list in self.groupPin:
                groupNr = 0
                for nr in list:
                    if nr == pin:
                        if self.group[groupNr]:
                            values[stateNr] = 0
                            break
                    groupNr += 1
                stateNr += 1

        count = 0
        for value in values:
            self.state[count] = value
            self.update_group(count)

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
                self.Instances[groupNr].set_config(self.configuration[groupNr])
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


class ControllerLightshowpi:
    Instances = [None] * config.ControllerConfig["PinCount"]
    state = [0] * config.ControllerConfig["PinCount"]
    master_state = 0
    current_profile = None

    def __init__(self):
        # generate Thread instances for each pin in use
        for pinNr in config.ControllerConfig["PinsInUse"]:
            if pinNr < config.ControllerConfig["PinCount"]:
                self.Instances[pinNr] = ThreadGPIOSingle(InstancePins[pinNr])
            else:
                raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                 config.ControllerConfig["PinCount"] + ")")

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update_all()

    def set_single(self, pinNr, state):
        self.state[pinNr] = state
        self.update_all()

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

    def set_config(self, dic):
        self.current_profile = dic

    def update_all(self):
        if self.master_state:
            self.update_target()
            pinNr = 0
            for state in self.state:
                if state:
                    self.Instances[pinNr].block()
                else:
                    self.Instances[pinNr].unblock()
                pinNr += 1
            system("sudo systemctl restart lightshowpi")
        else:
            system("sudo systemctl kill lightshowpi")
            for pinNr in range(len(self.state)):
                self.Instances[pinNr].unblock()

    def get_settings(self, key):
        if self.current_profile[key] is not None:
            return self.current_profile[key]
        else:
            return config.lsp_profile[config.lsp_settings["default_profile"]][key]

    def update_target(self):
        with open(config.lsp_settings["target"], "w") as f:
            f.write("[hardware]\n")
            f.write("gpio_pins = " + self.get_lsp_pins() + "\n")
            f.write("pwm_range = " + self.get_settings("pwm_range") + "\n")
            f.write("pin_modes = " + self.get_settings("pin_modes") + "\n")
            f.write("[lightshow]\n")
            f.write("decay_factor = " + self.get_settings("decay_factor") + "\n")
            f.write("SD_low = " + self.get_settings("SD_low") + "\n")
            f.write("SD_high = " + self.get_settings("SD_high") + "\n")
            f.write("attenuate_pct = " + self.get_settings("attenuate_pct") + "\n")
            f.write("light_delay = " + self.get_settings("light_delay") + "\n")
            f.write(config.lsp_settings["stream"])

    def get_lsp_pins(self):
        if config.lsp_settings["GPIO_mode"] == "BCM":
            return self.list_to_string(self.convert_to_WPI("BCMtoWPI"))
        if config.lsp_settings["GPIO_mode"] == "BOARD":
            return self.list_to_string(self.convert_to_WPI("BOARDtoWPI"))
        return self.list_to_string(self.convert_to_pins())

    def convert_to_WPI(self, source):
        wpi = []
        count = 0
        for value in self.state:
            if value:
                try:
                    wpi.append(config.lsp_settings[source][count])
                except IndexError:
                    pass
            count += 1
        return wpi

    def convert_to_pins(self):
        pins = []
        count = 0
        for value in self.state:
            if value:
                try:
                    pins.append(count)
                except IndexError:
                    pass
            count += 1
        return pins

    def list_to_string(self, list):
        return str(list)[1:-1]
