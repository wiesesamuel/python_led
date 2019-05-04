from lightstorm.pins.pin_generator import InstancePins
from lightstorm.helper import load_configuration
from lightstorm import config


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
            for name, value in self.configuration["profile"][self.configuration["pro"]].items():
                if name not in blacklist:
                    blacklist.append(name)
                    if values is not "":
                        if name in config.config_profile_string:
                            self.configuration["profile"][self.configuration["pro"]][name] = values
                        else:
                            self.configuration["profile"][self.configuration["pro"]][name] = float(values)
                    break
