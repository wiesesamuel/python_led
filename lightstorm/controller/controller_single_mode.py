from .controller import *
from time import sleep
from .threadHandler.mode_single import ModeSingle


class ControllerThreadsSingle(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration(config.Meta["ThreadSingle"])))

        # generate Thread instances for each pin in use
        self.MainInstanceRepresenter = []
        for pinNr in range(config.ControllerConfig["PinCount"]):
            self.MainInstanceRepresenter.append(
                ModeSingle(
                    InstancePins[pinNr],
                    self.configuration["profile"][self.configuration["pro"]]
                )
            )

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

