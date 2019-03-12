from .controller import *
from .threadHandler.cmddispatcher import CmdDispatcher


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
            return self.list_to_string(self.convert_to_wpi("BCMtoWPI"))
        if config.lsp_settings["GPIO_mode"] == "BOARD":
            return self.list_to_string(self.convert_to_wpi("BOARDtoWPI"))
        # User uses WiringPi
        return self.list_to_string(self.convert_to_pins())

    def convert_to_wpi(self, source):
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
