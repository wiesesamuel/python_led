from lightstorm.config import ControllerConfig, EXTENSIONS
from .gpio_pin import GPIOPin


class Generate:

    def __init__(self):

        # generate instances for each pin in use
        self.instances = {}
        for pinNr in range(ControllerConfig["PinCount"]):
            self.instances[pinNr] = GPIOPin(pinNr)

        # initialize extensions
        for extension in EXTENSIONS:
            ext = None
            name = extension["name"]
            if name == "arduino":
                from lightstorm.pins.extension_arduino import ArduinoExtension
                ext = ArduinoExtension(
                    extension["pin_start"],
                    extension["pin_end"],
                    extension["serial_port"],
                    extension["serial_baud"],
                )
            if ext:
                pins = ext.initialize()
                for pin in pins:
                    self.instances[pin.pin_nr] = pin


InstancePins = Generate().instances
