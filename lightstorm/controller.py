from .instance_pins import InstancePins
from .instance_threads import *
from . import config
from .helper import *
from .cmddispatcher import CmdDispatcher


class Controller:

    def __init__(self, configuration):
        self.configuration = configuration
        self.MainInstanceRepresenter = None
        self.in_use_map = [0] * config.ControllerConfig["PinCount"]

    def set_single(self, nr, state):
        self.configuration["selection"][self.configuration["selected"]]["state"][nr] = state

    def set_state(self, nr, state):
        self.in_use_map[nr] = state
        self.MainInstanceRepresenter[nr].set_state(state)

    def select_profile(self, nr):
        self.configuration["selected"] = nr

    def select_pro(self, nr):
        self.configuration["pro"] = nr

    def get_single_state(self, nr):
        return self.configuration["selection"][self.get_selected()]["state"][nr]

    def get_selected(self):
        return self.configuration["selected"]

    def set_config_values(self, input):
        blacklist = ["timestamp", "id"]

        # each value is loaded to the next possible parameter
        for values in input.split("&"):
            for name, value in \
                    self.configuration["profile"][self.configuration["pro"]].items():
                if name not in blacklist:
                    blacklist.append(name)
                    if values is not "":
                        if name in config.config_profile_string:
                            self.configuration["profile"][self.configuration["pro"]][
                                name] = values
                        else:
                            self.configuration["profile"][self.configuration["pro"]][name] = \
                                float(values)

                    break


class ControllerMono(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration(config.Meta["standard"])))

    def set_state(self, nr, state):
        if state:
            InstancePins[nr].set_brightness(self.configuration["selection"][self.configuration["selected"]]["dc"][nr])
            InstancePins[nr].set_frequency(self.configuration["selection"][self.configuration["selected"]]["fq"][nr])
            InstancePins[nr].set_state(1)
        else:
            InstancePins[nr].set_state(0)

    def set_config_single(self, nr, value, conf):
        self.configuration["selection"][self.configuration["selected"]][conf][nr] = value


class ControllerThreadsSingle(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration(config.Meta["ThreadSingle"])))

        # states
        self.MainInstanceRepresenter = [None] * config.ControllerConfig["PinCount"]

        # generate Thread instances for each pin in use
        for pinNr in range(config.ControllerConfig["PinCount"]):

            self.MainInstanceRepresenter[pinNr] = ThreadGPIOSingle(InstancePins[pinNr],
                                                                   self.configuration["profile"][self.configuration["pro"]])

    def set_state(self, nr, state):
        self.in_use_map[nr] = state
        self.update_instance(nr)

    def update_instance(self, nr):
        if self.in_use_map[nr]:
            if not self.MainInstanceRepresenter[nr].isAlive():
                self.MainInstanceRepresenter[nr].start()
            self.MainInstanceRepresenter[nr].set_config(self.configuration["selection"][self.get_selected()]["mode"][nr])
            self.MainInstanceRepresenter[nr].restart()
            self.MainInstanceRepresenter[nr].set_state_instance(1)

        else:
            self.stop_instance(nr)

    def stop_instance(self, nr):
        if self.MainInstanceRepresenter[nr].running:
            self.MainInstanceRepresenter[nr].stop()
            while not self.MainInstanceRepresenter[nr].idle:
                sleep(0.0001)

    def set_configuration_single(self, nr):
        self.configuration["selection"][self.get_selected()]["mode"][nr] = \
            self.configuration["profile"][self.configuration["pro"]]
        self.stop_instance(nr)
        self.MainInstanceRepresenter[nr].set_config(self.configuration["selection"][self.get_selected()]["mode"][nr])
        self.update_instance(nr)

    def set_configuration_group(self, group):
        for nr in group:
            self.set_configuration_single(nr)

    def update_instances_with_current_profile(self):
        for index in range(config.ControllerConfig["PinCount"]):
            if self.MainInstanceRepresenter[index].configuration["id"] == \
                    self.configuration["profile"][self.configuration["pro"]]["id"]:
                self.set_configuration_single(index)


class ControllerThreadsGroup(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration(config.Meta["ThreadGroup"])))

        # states
        self.MainInstanceRepresenter = [None] * config.ControllerConfig["GroupCount"]
        # initialising
        for group in range(config.ControllerConfig["GroupCount"]):
            self.MainInstanceRepresenter[group] = ThreadGPIOGroup(self.configuration["selection"][self.get_selected()]["mode"][group])
            self.MainInstanceRepresenter[group].enable_instances(self.get_group_state(group))
            self.MainInstanceRepresenter[group].set_instances(self.get_group_instances(group))

    def set_state(self, nr, state):
        self.in_use_map[nr] = state
        self.update_group(self.configuration["selection"][self.get_selected()]["membership"][nr])

    def update_group(self, nr):
        # current memberships
        current_instances = self.get_group_instances(nr)

        # update thread instances
        if self.MainInstanceRepresenter[nr].instances is not current_instances:
            self.MainInstanceRepresenter[nr].set_instances(current_instances)

        # set thread instances state
        self.MainInstanceRepresenter[nr].enable_instances(self.get_group_state(nr))

        # check if thread is still in use
        state = 0
        for index in range(config.ControllerConfig["PinCount"]):
            if self.configuration["selection"][self.get_selected()]["membership"][index] == nr and \
                    self.in_use_map[index]:
                state = 1
                break

        if state:
            # start thread
            if not self.MainInstanceRepresenter[nr].isAlive():
                self.MainInstanceRepresenter[nr].start()

            # update config
            self.MainInstanceRepresenter[nr].set_config(self.configuration["selection"][self.get_selected()]["mode"][nr])

            # run thread
            self.MainInstanceRepresenter[nr].restart()

            # update pins
            self.MainInstanceRepresenter[nr].activate_instance_in_use(1)
        else:
            # stop thread
            self.stop_instance(nr)

    def stop_instance(self, nr):
        if self.MainInstanceRepresenter[nr].running:
            self.MainInstanceRepresenter[nr].stop()
            while not self.MainInstanceRepresenter[nr].idle:
                sleep(0.0001)

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
                instances_list.append(InstancePins[nr])
        return instances_list

    def get_membership(self, nr):
        return self.configuration["selection"][self.get_selected()]["membership"][nr]

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
            self.stop_instance(group_a)
            self.update_group(group_a)
            self.stop_instance(group_b)
            self.update_group(group_b)

    def select_group(self, nr):
        self.configuration["group"] = nr

    def set_configuration_group(self, group):
        self.configuration["selection"][self.get_selected()]["mode"][group] = \
            self.configuration["profile"][self.configuration["pro"]]
        self.update_group(group)

    def set_configuration_current_group(self):
        self.set_configuration_group(self.configuration["group"])

    def update_instances_with_current_profile(self):
        for index in range(config.ControllerConfig["GroupCount"]):
            if self.MainInstanceRepresenter[index].configuration["id"] == \
                    self.configuration["profile"][self.configuration["pro"]]["id"]:
                self.update_group(index)


class ControllerLightshowpi(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration(config.Meta["lsp"])))
        self.dispatcher = CmdDispatcher()
        self.dispatcher.start()
        self.PreviousSettings = ""
        self.running = False

    def set_state(self, nr, state):
        self.in_use_map[nr] = state
        self.update_all()

    def select_pro(self, nr):
        self.configuration["pro"] = nr
        self.update_all()

    def update_instances_with_current_profile(self):
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
        if True in self.in_use_map:
            if self.update_target() or not self.running:
                # update state and config
                self.dispatcher.dispatch_cmd("sudo systemctl restart lightshowpi")
                self.running = True
        else:
            if self.running:
                self.dispatcher.dispatch_cmd("sudo systemctl kill lightshowpi")
                self.running = False

    def update_target(self):
        # only update lsp config file if a change was made
        current = self.get_target_text()
        if self.PreviousSettings != current:
            try:
                with open(config.lsp_settings["target"], "w") as f:
                    f.write(current)
                    self.PreviousSettings = current
                return True
            except Exception:
                pass
        return False

    def get_target_text(self):
        tmp = "[hardware]\n"
        tmp += ("gpio_pins = " + self.get_lsp_pins() + "\n")
        tmp += self.get_settings_text("pwm_range")

        if not self.get_settings("pin_modes") in ["onoff", "pwm"]:
            self.set_settings("pin_modes", config.CONFIGURATION["lsp"]["profile"][self.configuration["pro"]]["pin_modes"])

        tmp += self.get_settings_text("pin_modes")
        tmp += "[lightshow]\n"
        tmp += self.get_settings_text("decay_factor")
        tmp += self.get_settings_text("SD_low")
        tmp += self.get_settings_text("SD_high")
        tmp += self.get_settings_text("attenuate_pct")
        tmp += self.get_settings_text("light_delay")
        tmp += config.lsp_settings["stream"]

        return tmp

    def get_settings_text(self, key):
        return key + " = " + self.get_settings(key) + "\n"

    def get_settings(self, key):
        if self.configuration["profile"][self.configuration["pro"]][key] is not None:
            return self.configuration["profile"][self.configuration["pro"]][key]
        else:
            return config.CONFIGURATION["lsp"]["profile"][self.configuration["pro"]][key]

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
            if value and self.in_use_map[pin_nr]:
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
            if value and self.in_use_map[pin_nr]:
                try:
                    pins.append(pin_nr)
                except IndexError:
                    pass
            pin_nr += 1
        return pins

    @staticmethod
    def list_to_string(the_list):
        return str(the_list)[1:-1]


CtrlMono = ControllerMono()
CtrlSingle = ControllerThreadsSingle()
CtrlGroup = ControllerThreadsGroup()
CtrlLsp = ControllerLightshowpi()

CTRL = [CtrlMono, CtrlSingle, CtrlGroup, CtrlLsp]


class MasterController:

    def __init__(self):
        self.configuration = config.CONFIGURATION["master"]
        self.update_all()

    def set_master(self, ctrl, state):
        self.configuration["master_state"][ctrl] = state
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

    # choose pin controller in use by priority
    def get_controller_in_use(self, nr):
        ctrl, controller = None, None

        for highest_member in config.ControllerPriority:
            ctrl = config.Meta[highest_member]
            if self.configuration["master_state"][ctrl] and CTRL[ctrl].get_single_state(nr):
                controller = CTRL[ctrl]
                break

        return controller, ctrl

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
