from config import ControllerConfig, PinConfig
try:
    import RPi.GPIO as GPIO
except Exception:
    from .gpio_debug import GPIO


class Pin:
    state = 0
    running = 0
    brightness = PinConfig["brightness"]["default"]
    frequency = PinConfig["frequency"]["default"]

    def __init__(self, pin_nr):
        self.pinNr = pin_nr
        GPIO.setwarnings(False)
        if PinConfig["GPIO_mode"] == "BCM":
            GPIO.setmode(GPIO.BCM)
        elif PinConfig["GPIO_mode"] == "BOARD":
            GPIO.setmode(GPIO.BOARD)
        else:
            raise ValueError("GPIO_mode has to be 'BCM' or 'BOARD'! '" + PinConfig["GPIO_mode"] + "' is not allowed")
        GPIO.setup(pin_nr, GPIO.OUT)
        self.instance = GPIO.PWM(pin_nr, self.frequency)

    def set_state(self, value):
        self.state = value
        self.update()

    def set_brightness(self, value):
        if (PinConfig["brightness"]["min"] - 1) < value < (PinConfig["brightness"]["max"] + 1):
            self.brightness = value
            self.update()

    def set_frequency(self, value):
        if (PinConfig["frequency"]["min"] - 1) < value < (PinConfig["frequency"]["max"] + 1):
            self.frequency = value
            self.update()

    def update(self):
        if self.state:
            if self.running:
                self.instance.ChangeDutyCycle(self.brightness / PinConfig["factor"])
                self.instance.ChangeFrequency(self.frequency)
            else:
                self.instance.start(self.brightness / PinConfig["factor"])
                self.instance.ChangeFrequency(self.frequency)
                self.running = 1
        else:
            self.instance.stop()
            self.running = 0


class Pins:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self):
        # generate instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.Instances[pinNr] = Pin(pinNr)
            else:
                raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                 ControllerConfig["PinCount"] + ")")


InstancePins = Pins().Instances
