from config import ControllerConfig, PinConfig
from math import sin
from threading import Thread
from time import sleep, time
from .InstancePins import InstancePins
try:
    import noise
except Exception:
    from .gpio_debug import NOISE


def check_value(value):
    if 0 < value <= 100:
        return (value * value) / 100.0
    return 0.1


class ControllerThreadsGroup:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance    # list with lists with objects
        self.pieces = len(instance)
        self.state = [] * self.pieces
        self.group = []
        for list in instance:
            self.group.append([0] * len(list))

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
        for nr in group:
            stateNr = 0
            for list in self.instance:
                groupNr = 0
                for pin in list:
                    if pin.pinNr == nr:
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

    @staticmethod
    def stop_instance(instance):
        if instance.running:
            instance.stop()
            while not instance.idle:
                sleep(0.0001)


class ControllerThreadsSingle:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance    # list with objects
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
                sleep(1)
            self.idle = False


class ThreadGPIOGroup(ThreadGPIO):

    def __init__(self, instance):
        super(ThreadGPIOGroup, self).__init__()
        self.instance = instance
        self.start()

    def run(self):
        while True:
            self.wait()
            if self.configuration["name"] == 0:
                self.sin()
            elif self.configuration["name"] == 1:
                self.noise()


class ThreadGPIOSingle(ThreadGPIO):

    def __init__(self, instances):
        super(ThreadGPIOSingle, self).__init__()
        self.instances = instances

    def run(self):
        while True:
            self.wait()
            if self.configuration["name"] == "sin":
                self.sin()
            elif self.configuration["name"] == "noise":
                self.noise()

    def noise(self):
        while self.running:
            # get elapsed
            elapsed = time() - self.configuration["timestamp"]

            # get noise
            value = noise.pnoise1(
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
            value = sin(elapsed * self.configuration["periode"])

            # scale to [0, 1]
            value = (value + 1) * 0.5

            # scale to [min, max]
            value *= self.configuration["max"] - self.configuration["min"]
            value += self.configuration["min"]

            # set brightness
            self.instance.set_brightness(value)

            # delay
            sleep(self.configuration["delay"])


class InstancesThreadSingle:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self, PinInstances):
        # generate Thread instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.Instances[pinNr] = ThreadGPIOSingle(PinInstances[pinNr])
            else:
                raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                 ControllerConfig["PinCount"] + ")")
        for instance in self.Instances:
            if instance is None:
                self.instance = ThreadFake()


class InstancesThreadGroup:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self, PinInstances):
        # generate Thread instances for each stripe group declared
        count = 0
        for stripe in ControllerConfig["Group"]:
            tmpInstanceMap = []
            for pinNr in stripe:
                if pinNr < ControllerConfig["PinCount"]:
                    tmpInstanceMap.append(PinInstances[pinNr])
                else:
                    raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                     ControllerConfig["PinCount"] + ")")
            self.Instances[count] = ThreadGPIOGroup(tmpInstanceMap)
            count += 1
        for instance in self.Instances:
            if instance is None:
                self.instance = ThreadFake()
        if False:
            for nr in range(ControllerConfig["PinCount"]):
                if self.Instances[nr] is None:
                    self.Instances[nr] = ThreadFake()


Single = ControllerThreadsSingle(InstancesThreadSingle(InstancePins).Instances)
Group = ControllerThreadsGroup(InstancesThreadGroup(InstancePins).Instances)
