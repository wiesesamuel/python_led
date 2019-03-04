from .config import ControllerConfig, PinConfig
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
        self.pin_nr = pin_nr
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
        if PinConfig["brightness"]["min"] < value < PinConfig["brightness"]["max"]:
            self.brightness = value
            self.update()

    def set_frequency(self, value):
        if PinConfig["frequency"]["min"] < value < PinConfig["frequency"]["max"]:
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

    def debug(self):
        return ("Pin " + str(self.pin_nr) + " has value " + str(self.running))


class Pins:
    Instances = []

    def __init__(self):
        # generate instances for each pin in use
        for pinNr in range(ControllerConfig["PinCount"]):
            self.Instances.append(Pin(pinNr))


InstancePins = Pins().Instances
