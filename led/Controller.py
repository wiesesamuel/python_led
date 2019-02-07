from os import system
from .InstancePins import InstancePins
from .InstanceThreads import *
import config
from .Helper import *
from .cmddispatcher import CmdDispatcher


class Controller:

    def __init__(self, configuration):
        self.configuration = configuration

        # removed list() copy
        # every Controller use the same GPIO Pin Instances
        self.Instances = InstancePins

    def set_single(self, nr, state):
        self.configuration["selection"][self.configuration["selected"]]["state"][nr] = state

    def set_state(self, nr, state):
        self.Instances[nr].set_state(state)

    def select_profile(self, nr):
        self.configuration["selected"] = nr

    def select_pro(self, nr):
        self.configuration["pro"] = nr

    def get_single_state(self, nr):
        return self.configuration["selection"][self.get_selected()]["state"][nr]

    def update_profile(self):
        self.configuration["selection"][self.get_selected()]["mode"] = \
            self.configuration["profile"][self.configuration["pro"]]

    def get_selected(self):
        return self.configuration["selected"]


class ControllerMono(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("standard")))

    def set_state(self, nr, state):
        if state:
            self.Instances[nr].set_brightness(self.configuration["selection"][self.configuration["selected"]]["dc"][nr])
            self.Instances[nr].set_frequency(self.configuration["selection"][self.configuration["selected"]]["fq"][nr])
            self.Instances[nr].set_state(1)
        else:
            self.Instances[nr].set_state(0)

    def set_config_single(self, nr, value, conf):
        self.configuration["selection"][self.configuration["selected"]][conf][nr] = value


class ControllerThreadsSingle(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("ThreadSingle")))

        self.singleInstances = [None] * config.ControllerConfig["PinCount"]
        # generate Thread instances for each pin in use
        for pinNr in range(config.ControllerConfig["PinCount"]):
            self.singleInstances[pinNr] = ThreadGPIOSingle(self.Instances[pinNr],
                                                           self.configuration["profile"][self.configuration["pro"]])

    def set_state(self, nr, state):
        if state:
            if not self.singleInstances[nr].isAlive():
                self.singleInstances[nr].start()
            self.singleInstances[nr].set_config(self.configuration["selection"][self.get_selected()]["mode"][nr])
            self.singleInstances[nr].restart()
        else:
            if self.singleInstances[nr].running:
                self.singleInstances[nr].stop()
                while not self.singleInstances[nr].idle:
                    sleep(0.0001)

    def set_configuration_single(self, nr):
        self.configuration["selection"][self.get_selected()]["mode"][nr] = \
            self.configuration["profile"][self.configuration["pro"]]
        self.singleInstances[nr].set_config(self.configuration["selection"][self.get_selected()]["mode"][nr])

    def set_configuration_group(self, group):
        for nr in group:
            self.set_configuration_single(nr)


class ControllerThreadsGroup(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("ThreadGroup")))

        # states
        self.groupInstances = [None] * config.ControllerConfig["GroupCount"]
        self.in_use_map = [0] * config.ControllerConfig["PinCount"]

        # initialising
        for group in range(config.ControllerConfig["GroupCount"]):
            self.groupInstances[group] = ThreadGPIOGroup(self.configuration["selection"][self.get_selected()]["mode"][group])
            self.groupInstances[group].enable_instances(self.get_group_state(group))
            self.groupInstances[group].set_instances(self.get_group_instances(group))

    def set_state(self, nr, state):
        # set 'in use' state
        self.in_use_map[nr] = state

        # update current group
        self.update_group(self.configuration["selection"][self.get_selected()]["membership"][nr])

    def update_group(self, nr):
        # current memberships
        current_instances = self.get_group_instances(nr)

        # update thread instances
        if self.groupInstances[nr].instances is not current_instances:
            self.groupInstances[nr].set_instances(current_instances)

        # set thread instances state
        self.groupInstances[nr].enable_instances(self.get_group_state(nr))

        # check if thread is still in use
        state = 1
        for index in range(config.ControllerConfig["PinCount"]):
            if self.configuration["selection"][self.get_selected()]["membership"][index] == nr and \
                    self.in_use_map[index]:
                state = 0
                break

        if state:
            # start thread
            if not self.groupInstances[nr].isAlive():
                self.groupInstances[nr].start()

            # update config
            self.groupInstances[nr].set_config(self.configuration["selection"][self.get_selected()]["mode"][nr])

            # run thread
            self.groupInstances[nr].restart()
        else:
            # stop thread
            if self.groupInstances[nr].running:
                self.groupInstances[nr].stop()
                while not self.groupInstances[nr].idle:
                    sleep(0.0001)

    def add_members_to_current_group(self, group):
        for member in group:
            self.add_member_to_current_group(member)

    def add_member_to_current_group(self, member):
        self.add_member_to_group(member, self.configuration["group"])

    def add_member_to_group(self, member, group):
        group_a = self.configuration["selection"][self.get_selected()]["membership"][member]
        self.configuration["selection"][self.get_selected()]["membership"][member] = group
        self.update_groups(group_a, group)

    def update_groups(self, group_a, group_b):
        if group_a != group_b:
            self.update_group(group_a)
            self.update_group(group_b)

    def get_membership(self, nr):
        return self.configuration["selection"][self.get_selected()]["membership"][nr]

    def get_group_state(self, group):
        state_list = []
        for nr in range(len(self.configuration["selection"][self.get_selected()]["state"])):
            if self.configuration["selection"][self.get_selected()]["membership"][nr] == group:
                value = 0
                if self.configuration["selection"][self.get_selected()]["state"][nr] and self.in_use_map[nr]:
                    value = 1
                state_list.append(value)
        return state_list

    def get_group_instances(self, group):
        instances_list = []
        for nr in range(len(self.configuration["selection"][self.get_selected()]["state"])):
            if self.configuration["selection"][self.get_selected()]["membership"][nr] == group:
                instances_list.append(self.Instances[nr])
        return instances_list

    def select_group(self, nr):
        self.configuration["group"] = nr

    def set_configuration_group(self, group):
        self.configuration["selection"][self.get_selected()]["mode"][group] = \
            self.configuration["profile"][self.configuration["pro"]]
        self.update_group(group)

    def set_configuration_current_group(self):
        self.set_configuration_group(self.configuration["group"])


class ControllerLightshowpi(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration("lsp")))
        self.dispatcher = CmdDispatcher()
        self.dispatcher.start()
        self.PreviousSettings = ""
        self.PreviousCommand = ""

    def set_state(self, nr, state):
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
            if self.PreviousCommand != "restart":
                self.dispatcher.dispatch_cmd("sudo systemctl restart lightshowpi")
                self.PreviousCommand = "restart"
        else:
            if self.PreviousCommand != "kill":
                self.dispatcher.dispatch_cmd("sudo systemctl kill lightshowpi")
                self.PreviousCommand = "kill"

    def update_target(self):
        # only update lsp config file if a change was made
        current = self.get_target_text()
        if self.PreviousSettings != current:
            try:
                with open(config.lsp_settings["target"], "w") as f:
                    f.write(current)
                    self.PreviousSettings = current
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
        pin_nr = 0
        for value in self.configuration["selection"][self.configuration["selected"]]["state"]:
            if value:
                try:
                    wpi.append(config.lsp_settings[source][pin_nr])
                except IndexError:
                    pass
            pin_nr += 1
        return wpi

    def convert_to_pins(self):
        pins = []
        pin_nr = 0
        for value in self.configuration["selection"][self.configuration["selected"]]["state"]:
            if value:
                try:
                    pins.append(pin_nr)
                except IndexError:
                    pass
            pin_nr += 1
        return pins

    @staticmethod
    def list_to_string(the_list):
        return str(the_list)[1:-1]


CtrlLsp = ControllerLightshowpi()
CtrlGroup = ControllerThreadsGroup()
CtrlSingle = ControllerThreadsSingle()
CtrlMono = ControllerMono()

CTRL = [CtrlMono, CtrlSingle, CtrlGroup, CtrlLsp]


class MasterController:

    def __init__(self):
        self.configuration = load_configuration("master")

    def set_master(self, ctrl, state):
        self.configuration["master_state"][ctrl] = state
        CTRL[ctrl].configuration["master_state"] = state
        self.update_all()

    def flip_master(self, ctrl):
        self.set_master(ctrl, not self.configuration["master_state"][ctrl])

    def set_single(self, ctrl, nr, state):
        CTRL[ctrl].set_single(nr, state)
        self.update_single(nr)

    def flip_single(self, ctrl, nr):
        self.set_single(ctrl, nr, not CTRL[ctrl].get_single_state(nr))

    def unify_group(self, ctrl, group):
        value = 1
        for nr in group:
            if CTRL[ctrl].get_single_state(nr):
                value = 0
                break
        for nr in group:
            self.set_single(ctrl, nr, value)

    def update_all(self):
        for nr in range(config.ControllerConfig["PinCount"]):
            self.update_single(nr)

    # choose pin controller in use by priority
    def get_controller_in_use(self, nr):
        ctrl, controller = None, None

        for highest_member in config.ControllerPriority:
            ctrl = config.Meta[highest_member]
            if self.configuration["master_state"][ctrl] and CTRL[ctrl].get_single_state(nr):
                controller = CTRL[ctrl]
                break

        return controller, ctrl

    def update_single(self, nr):
        controller, index = self.get_controller_in_use(nr)
        # shut other controller pin off
        for ctrl in CTRL:
            if ctrl is not controller:
                ctrl.set_state(nr, 0)

        if controller is not None:
            controller.set_state(nr, 1)
            self.configuration["state"][nr] = index
        else:
            self.configuration["state"][nr] = -1

    def change_profile(self, ctrl, nr):
        CTRL[ctrl].select_profile(nr)
        self.update_all()

    def get_single_state(self, ctrl, nr):
        in_use = 0
        if self.configuration["state"][nr] == ctrl:
            in_use = 1
        # return on, inUse
        return CTRL[ctrl].get_single_state(nr), in_use


CtrlMaster = MasterController()
