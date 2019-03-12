from .mode import Mode
from time import sleep, time
from math import sin


class ModeGroup(Mode):

    def __init__(self, configuration):
        super(ModeGroup, self).__init__()
        self.set_config(configuration)
        self.instances = [None]
        self.in_use = [None]

    def set_instances(self, instances):
        self.instances = instances

    def enable_instances(self, list):
        self.in_use = list

    def activate_instance_in_use(self, value):
        if value:
            # only activate pins in use
            ind = 0
            for i in self.instances:
                i.set_state(self.in_use[ind])
                ind += 1
        # deactivate all
        else:
            for i in self.instances:
                i.set_state(0)
                i.set_brightness(99)

    def get_instances_in_use(self):
        using = []
        ind = 0
        for instance in self.instances:
            if self.in_use[ind]:
                using.append(instance)
            ind += 1
        return using

    def run(self):
        while True:
            self.wait()

            # set pins up
            self.activate_instance_in_use(1)
            print("running Thread Group: " + str(self.configuration))

            # update timestamp
            self.configuration["timestamp"] = time()

            # run light mode
            if self.configuration["id"][1] == 0:
                while self.running:
                    self.sin(self.get_instances_in_use())
            elif self.configuration["id"][1] == 1:
                while self.running:
                    self.recursive(self.get_instances_in_use(), self.sin)
            elif self.configuration["id"][1] == 2:
                while self.running:
                    self.row_flow()
            self.activate_instance_in_use(0)
            print("stopped Thread Group: " + str(self.configuration))

    def row_flow(self):
        pass

    def recursive(self, instances, method):
        if self.running:
            for instance in instances:
                if len(instances):
                    self.recursive(instances[:-1], method)
                print("loop")
                method(instance)

    def sin(self, instances):
        for instance in instances:
            elapsed = time() - self.configuration["timestamp"]

            while self.running and elapsed < self.configuration["timeCycle"]:

                # get elapsed
                elapsed = time() - self.configuration["timestamp"]

                # get sinus
                value = sin(elapsed * self.configuration["period"])

                # scale to [0, 1]
                value = (value + 1) * 0.5

                # scale to [min, max]
                value *= self.configuration["max"] - self.configuration["min"]
                value += self.configuration["min"]

                # set brightness
                instance.set_brightness(value)

                # delay
                sleep(self.configuration["delay"])

