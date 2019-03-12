from .mode import Mode
from time import sleep, time
from .noise import *


class ModeSingle(Mode):

    def __init__(self, instance, configuration):
        super(ModeSingle, self).__init__()
        self.instance = instance
        self.set_config(configuration)

    def run(self):
        while True:
            self.wait()
            self.set_state_instance(1)
            self.activate()
            if self.configuration["id"][0] == 0:
                self.sin()
            elif self.configuration["id"][0] == 1:
                self.noise()
            self.set_state_instance(0)

    def activate(self):
        self.configuration["timestamp"] = time()

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
            value = math.sin(elapsed * self.configuration["period"])

            # scale to [0, 1]
            value = (value + 1) * 0.5

            # scale to [min, max]
            value *= self.configuration["max"] - self.configuration["min"]
            value += self.configuration["min"]

            # set brightness
            self.instance.set_brightness(value)

            # delay
            sleep(self.configuration["delay"])

