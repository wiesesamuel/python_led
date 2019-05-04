try:
    import RPi.GPIO as GPIO
except Exception as e:
    print(e)
    from .gpio_debug import GPIO
from .pin import Pin
from lightstorm.config import PinConfig


class GPIOPin(Pin):

    def __init__(self, pin_nr):
        super().__init__(pin_nr)

        # set defaults
        self.state = 0
        self.running = 0
        self.brightness = PinConfig["brightness"]["default"]
        self.frequency = PinConfig["frequency"]["default"]

        # setup pin
        GPIO.setwarnings(False)
        if PinConfig["GPIO_mode"] == "BCM":
            GPIO.setmode(GPIO.BCM)
        elif PinConfig["GPIO_mode"] == "BOARD":
            GPIO.setmode(GPIO.BOARD)
        else:
            raise ValueError("GPIO_mode has to be 'BCM' or 'BOARD'! '" + PinConfig["GPIO_mode"] + "' is not allowed")
        GPIO.setup(pin_nr, GPIO.OUT)

        # get instance
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
