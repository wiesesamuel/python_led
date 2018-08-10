from time import sleep
from os import system
from .InstancePins import InstancePins
from .InstanceThreads import InstancesThreadSingle, InstancesThreadGroup
from config import lsp_settings, lsp_profile

class Master:

    def __init__(self):
        self.pieces = len(InstancePins)
        c0 = ControllerMono(InstancePins)
        c1 = ControllerThreadsSingle(InstancesThreadSingle(InstancePins).Instances)
        c2 = ControllerThreadsGroup(InstancesThreadGroup(InstancePins).Instances)
        c3 = ControllerLightshowpi(lsp_settings, lsp_profile[lsp_settings["default_profile"]], self.pieces)
        self.controller = [c0, c1, c2, c3]
        self.monitor = [[0, 0, 0, 0]] * self.pieces
        self.master_state = [0, 0, 0, 0]

    def set_master(self, meta, value):
        if self.master_state[meta] != value:
            self.master_state[meta] = value
            self.update_all_controller()

    def flip_master(self, meta):
        self.set_master(meta, not self.master_state[meta])

    def update_all_controller(self):
        if self.master_state[0]:
            # update ControllerMono
            self.update_single_controller(0)
            if self.master_state[2]:
                if self.master_state[1]:
                    # manipulate pins in ControllerSingle if there's a conflict with ControllerGroup
                    for pin in range(self.pieces):
                        if self.monitor[pin][1] and self.monitor[pin][2]:
                            self.set_single(1, pin, 0)
                            self.set_single(2, pin, 1)
                            #self.controller[1].set_single(pin, 0)
                            #self.controller[2].set_single(pin, 1)
                        else:
                            # update ControllerSingle and ControllerGroup
                            self.set_single(1, pin, self.monitor[pin][1])
                            self.set_single(2, pin, self.monitor[pin][2])
                            #self.controller[1].set_single(pin, self.monitor[pin][1])
                            #self.controller[2].set_single(pin, self.monitor[pin][2])
                    self.controller[1].set_master(1)
                    self.controller[2].set_master(1)
                else:
                    self.controller[1].set_master(0)
                    # update ControllerGroup
                    self.update_single_controller(2)
            else:
                self.controller[2].set_master(0)
                if self.master_state[1]:
                    # update ControllerSingle
                    self.update_single_controller(1)
                else:
                    self.controller[1].set_master(0)
        # shut all down
        else:
            for i in range(3):
                self.controller[i].set_master(0)

    def update_single_controller(self, meta):
        for pin in range(self.pieces):
            self.set_single(meta, pin, self.monitor[pin][meta])
            #self.controller[meta].set_single(pin, self.monitor[pin][meta])
        self.controller[meta].set_master(self.master_state[meta])

    def set_single(self, meta, pin, value):
        # check if lsp uses the pin
        if self.master_state[3] and self.monitor[pin][3]:
            value = 0
            # maybe add kill meta = 1,2
        self.controller[meta].set_single(pin, value)

    def update_single_pin(self, meta, pin):
        if self.master_state[0]:
            # manipulate pins in ControllerSingle if there's a conflict with ControllerGroup
            if meta and self.monitor[pin][1] and self.monitor[pin][2]:
                self.set_single(1, pin, 0)
                self.set_single(2, pin, 1)
                #self.controller[1].set_single(pin, 0)
                #self.controller[2].set_single(pin, 1)
            else:
                # update
                self.set_single(meta, pin, self.monitor[pin][meta])
                #self.controller[meta].set_single(pin, self.monitor[pin][meta])
        # shut all down
        else:
            for i in range(3):
                self.controller[i].set_master(0)

    def set_pin_state(self, meta, pin, value):
        self.monitor[pin][meta] = value
        self.update_single_pin(meta, pin)

    def flip_single(self, meta, pin):
        self.set_pin_state(meta, pin, not self.monitor[pin][meta])

    def unify_group(self, meta, group):
        value = 1
        for nr in group:
            if self.monitor[nr][meta]:
                value = 0
                break
        for nr in group:
            self.monitor[nr][meta] = value
            self.update_single_pin(meta, nr)


class ControllerLightshowpi:
    current_profile = None
    master_state = 0

    def __init__(self, settings, default_profile, length):
        self.settings = settings
        self.default_profile = default_profile
        self.state = [0] * length

    def set_master(self, state):
        self.master_state = state
        self.update()

    def flip_master(self):
        self.master_state = not self.master_state
        self.update()

    def set_config(self, dic):
        self.current_profile = dic

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update()

    def update(self):
        if self.master_state:
            self.update_target()
            system("sudo systemctl restart lightshowpi")
        else:
            system("sudo systemctl kill lightshowpi")

    def get_default_settings(self, key):
        return self.default_profile[key]

    def get_settings(self, key):
        if self.current_profile[key] is not None:
            return self.current_profile[key]
        else:
            return self.get_default_settings(key)

    def update_target(self):
        with open(self.settings["target"], "w") as f:
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
            f.write(self.settings["stream"])

    def get_lsp_pins(self):
        if self.settings["GPIO_mode"] == "BCM":
            return self.list_to_string(self.convert_to_WPI("BCMtoWPI"))
        if self.settings["GPIO_mode"] == "BOARD":
            return self.list_to_string(self.convert_to_WPI("BOARDtoWPI"))
        return self.list_to_string(self.convert_to_pins())

    def convert_to_WPI(self, source):
        wpi = []
        count = 0
        for value in self.state:
            if value:
                try:
                    wpi.append(self.settings[source][count])
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


# add setbrigthness and fq
class ControllerMono:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance
        self.state = [0] * len(instance)

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

    def set_config(self, dic):



class ControllerThreadsSingle:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance  # list with objects
        self.pieces = len(instance)
        self.state = [0] * self.pieces

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
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

    def update_single(self, nr):
        if self.master_state and self.state[nr]:
            if self.instance[nr].isAlive():
                self.instance[nr].restart()
            else:
                self.instance[nr].start()
                self.instance[nr].restart()
        else:
            self.stop_instance(self.instance[nr])

    def update_all(self):
        for nr in range(self.pieces):
            self.update_single(nr)

    @staticmethod
    def stop_instance(instance):
        if instance.running:
            instance.stop()
            while not instance.idle:
                sleep(0.0001)

    def get_state_pin(self, pin):
        return self.state[pin]

    def set_config(self, nr, dic):
        self.instance[nr].set_config(dic)


class ControllerThreadsGroup:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance    # list with lists with objects
        self.pieces = len(instance)
        self.state = [] * self.pieces
        self.group = []
        self.groupPin = []
        for list in instance:
            self.group.append([0] * len(list))
            tmpList = []
            for inst in list:
                tmpList.append(inst.pinNr)
            self.groupPin.append(tmpList)

    def get_state_pin(self, pin):
        stateNr = 0
        for list in self.groupPin:
            groupNr = 0
            for nr in list:
                if nr == pin:
                    if self.state[stateNr] and self.group[groupNr]:
                        return 1
                    else:
                        return 0
                groupNr += 1
            stateNr += 1

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update_group(nr)

    def flip_single(self, nr):
        self.state[nr] = not self.state[nr]
        self.update_group(nr)

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

    def update_group(self, nr):
        if self.master_state and self.state[nr]:
            if self.instance[nr].isAlive():
                self.instance[nr].restart()
            else:
                self.instance[nr].start()
                self.instance[nr].restart()
        else:
            self.stop_instance(self.instance[nr])

    def update_all(self):
        for nr in range(self.pieces):
            self.update_group(nr)

    def set_config(self, nr, dic):
        self.instance[nr].set_config(dic)

    @staticmethod
    def stop_instance(instance):
        if instance.running:
            instance.stop()
            while not instance.idle:
                sleep(0.0001)


master = Master()
