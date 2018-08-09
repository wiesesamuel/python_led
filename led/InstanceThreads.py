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

