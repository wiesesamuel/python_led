from .controller import *
from time import sleep
from .threadHandler.mode_group import ModeGroup


class ControllerThreadsGroup(Controller):

    def __init__(self):
        super().__init__(dict(load_configuration(config.Meta["ThreadGroup"])))

        # states
        self.MainInstanceRepresenter = [None] * config.ControllerConfig["GroupCount"]

        # initialising
        for group in range(config.ControllerConfig["GroupCount"]):
            self.MainInstanceRepresenter[group] = ModeGroup(
                self.configuration["selection"][self.get_selected()]["mode"][group])
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
        for index in config.ControllerConfig["PinsInUse"]:
            if self.configuration["selection"][self.get_selected()]["membership"][index] == nr and \
                    self.in_use_map[index]:
                state = 1
                break

        if state:
            # start thread
            if not self.MainInstanceRepresenter[nr].isAlive():
                self.MainInstanceRepresenter[nr].start()

            # update config
            self.MainInstanceRepresenter[nr].set_config(
                self.configuration["selection"][self.get_selected()]["mode"][nr]
            )

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
