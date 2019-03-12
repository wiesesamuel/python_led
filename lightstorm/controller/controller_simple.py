from .controller import *


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
