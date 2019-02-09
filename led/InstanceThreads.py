from math import sin
from threading import Thread
from time import sleep, time
from Noise import noise


def check_value(value):
    if 0 < value <= 100:
        return (value * value) / 100.0
    return 0.1


class ThreadFake:
    running = 0
    idle = 1

    @staticmethod
    def set_state(a):
        pass

    @staticmethod
    def restart():
        pass

    @staticmethod
    def stop():
        pass


class ThreadGPIO(Thread):

    def __init__(self):
        super(ThreadGPIO, self).__init__()
        self.running = False
        self.idle = False
        self.configuration = None

    def set_config(self, config):
        self.configuration = config

    def set_state(self, value):
        if value:
            if self.isAlive():
                self.restart()
            else:
                self.start()
        else:
            self.stop()

    def restart(self):
        self.running = True

    def stop(self):
        self.running = False

    def wait(self):
        if not self.running:
            self.idle = True
            while not self.running:
                sleep(0.01)
            self.idle = False


class ThreadGPIOSingle(ThreadGPIO):

    def __init__(self, instance, configuration):
        super(ThreadGPIOSingle, self).__init__()
        self.instance = instance
        self.set_config(configuration)

    def run(self):
        while True:
            self.wait()
            self.set_state_instance(1)
            self.configuration["timestamp"] = time()
            if self.configuration["id"][0] == 0:
                self.sin()
            elif self.configuration["id"][0] == 1:
                self.noise()
            self.set_state_instance(0)

    def set_state_instance(self, state):
        self.instance.set_state(state)

    def noise(self):
        while self.running:

            # get elapsed
            elapsed = time() - self.configuration["timestamp"]

            # get noise
            value = noise(
                elapsed * self.configuration["factor"],
                self.configuration["octave"]
            )

            # scale to [0, 1]
            value = (value + 1) * 0.5

            # do the flip flap
            for _ in range(self.configuration["high"]):
                value *= value

            # scale to [min, max]
            value *= self.configuration["max"] - self.configuration["min"]
            value += self.configuration["min"]

            # set brightness
            self.instance.set_brightness(value)

            # delay
            sleep(self.configuration["delay"])

    def sin(self):
        while self.running:
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
            self.instance.set_brightness(value)

            # delay
            sleep(self.configuration["delay"])


class ThreadGPIOGroup(ThreadGPIO):

    def __init__(self, configuration):
        super(ThreadGPIOGroup, self).__init__()
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

