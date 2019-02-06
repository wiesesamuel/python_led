from math import sin
from threading import Thread
from time import sleep, time
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
            if self.configuration["id"][0] == 0:
                self.sin()
            elif self.configuration["id"][0] == 1:
                self.noise()
            self.instance.set_state(0)

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
        self.instances = [None]
        self.configuration = configuration

    def set_instances(self, instances):
        self.instances = instances

    def add_instance(self, instance):
        self.instances.append(instance)

    def remove_instance(self, instance):
        if instance in self.instances:
            self.instances.remove(instance)

    def enable_instaces(self, list):
        self.configuration["state"] = list

    def run(self):
        while True:
            self.wait()
            if self.configuration["id"][0] == 0:
                self.sin()
            elif self.configuration["id"][0] == 1:
                self.noise()

    def noise(self):
        while self.running:
            for instance in self.instances:
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
                instance.set_brightness(value)

                # delay
                sleep(self.configuration["delay"])

    def sin(self):
        while self.running:
            for instance in self.instances:
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

