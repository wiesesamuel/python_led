from lightstorm.config import PinConfig, EXTENSIONS
from .gpio_pin import GPIOPin


class Generate:

    def __init__(self):

        # generate instances for each pin in use
        self.instances = {}
        for member in PinConfig["AllocationMap"]:
            name = member["name"]
            if name == "GPIO":
                for nr in range(member["range"][0], member["range"][1]):
                    self.instances[nr] = GPIOPin(nr)
            elif name == "Arduino":
                from lightstorm.pins.extension_arduino import ArduinoExtension
                ext = ArduinoExtension(
                    member["range"][0],
                    member["range"][1],
                    EXTENSIONS[name]["serial_port"],
                    EXTENSIONS[name]["serial_baud"],
                )
                for pin in ext.initialize():
                    self.instances[pin.pin_nr] = pin


InstancePins = Generate().instances
