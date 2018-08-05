from config import ControllerConfig, PinConfig
from .Helper import println
from .Threads import ThreadSingle, ThreadGroup
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
        else:
            GPIO.setmode(GPIO.BOARD)
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
        else:
            self.instance.stop()


class InstancePin:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self):
        # generate instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.Instances[pinNr] = Pin(pinNr)
            else:
                println("A pin in 'PinsInUse' is higher than 'PinCount'")


class InstancePinThread:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self, PinInstances):
        # generate Thread instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.Instances[pinNr] = ThreadSingle(PinInstances[pinNr])
            else:
                println("A pin in 'PinsInUse' is higher than 'PinCount'")


class InstanceStripeThread:
    Instances = [None] * len(ControllerConfig["Stripes"])

    def __init__(self, PinInstances):
        # generate Thread instances for each stripe group declared
        count = 0
        for stripe in ControllerConfig["Stripes"]:
            tmpInstanceMap = []
            for pinNr in stripe:
                if pinNr < ControllerConfig["PinCount"]:
                    tmpInstanceMap.append(PinInstances[pinNr])
                else:
                    println("A pin in 'Stripes' is higher than 'PinCount'")
            self.Instances[count] = ThreadGroup(tmpInstanceMap)
            count += 1


class InstanceColorThread:
    Instances = [None] * len(ControllerConfig["Colors"])

    def __init__(self, PinInstances):
        # generate Thread instances for each color group declared
        count = 0
        for color in ControllerConfig["Colors"]:
            tmpInstanceMap = []
            for pinNr in color:
                if pinNr < ControllerConfig["PinCount"]:
                    tmpInstanceMap.append(PinInstances[pinNr])
                else:
                    println("A pin in 'Color' is higher than 'PinCount'")
            self.Instances[count] = ThreadGroup(tmpInstanceMap)
            count += 1


Instances = InstancePin().Instances
InstancesThreadSingle = InstancePinThread(Instances).Instances
InstancesThreadStripe = InstanceStripeThread(Instances).Instances
InstancesThreadColor = InstanceColorThread(Instances).Instances
Instance = [Instances, InstancesThreadSingle, InstancesThreadStripe, InstancesThreadColor]
