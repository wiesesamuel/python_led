from math import sin
from threading import Thread
from time import sleep, time

try:
    import noise
except Exception:
    from .gpio_debug import NOISE
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO


def check_value(value):
    if 0 < value < 100:
        return (value * value) / 100.0
    return 1


class GPIOThread(Thread):

    def __init__(self):
        super(GPIOThread, self).__init__()
        self.instance = None
        self.running = False
        self.idle = False
        self.configuration = None

    def set_config(self, config):
        self.configuration = config

    def set_state(self, value):
        if value:
            self.restart()
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


class ThreadGroup(GPIOThread):

    def __init__(self, instance):
        super(ThreadGroup, self).__init__()
        self.instance = instance
        self.start()

    def run(self):
        while True:
            self.wait()
            if self.configuration["mode"] == 0:
                self.sin()
            elif self.configuration["mode"] == 1:
                self.noise()


class ThreadSingle(GPIOThread):

    def __init__(self, instance):
        super(ThreadSingle, self).__init__()
        self.instance = instance
        self.running = False
        self.idle = False
        self.configuration = None
        self.start()

    def run(self):
        while True:
            self.wait()
            if self.configuration["mode"] == 0:
                self.sin()
            elif self.configuration["mode"] == 1:
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
