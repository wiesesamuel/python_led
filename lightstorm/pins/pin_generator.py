from lightstorm.config import PinConfig
from .gpio_pin import GPIOPin

def initialise_arduinos():
    from serial import Serial
    from ..helper import load_json, save_json

    arduinos = []
    baud = 500000

    # handshake with arduinos
    ttys = "/dev/ttyUSB0 /dev/ttyUSB1 /dev/ttyUSB2 /dev/ttyUSB3 /dev/ttyUSB4 /dev/ttyUSB5 /dev/ttyUSB6 /dev/tty0 /dev/tty1 /dev/tty2 /dev/tty3 /dev/tty4"
    for tty in ttys.split(" "):
        print(tty)
        print("\n")
        try:
            serial = Serial(tty, baud, timeout=0.01)
            tmp = [0xAA, 0xAA, 0, 9, 0]
            serial.reset_input_buffer()
            msg = tmp + [sum(tmp) % 256]
            print("serial write " + str(msg))

            print("\n")
            serial.write(msg)
            res = serial.read()
            print("serial read " + str(res))
            print("\n")

            if (res):
                arduinos.append({
                    "serial_port": tty,
                    "id": res,
                    "serial_baud": baud,
                    "enabled": False,
                    "name": "arduino_default_name",
                    "range": [100, 101],

                })

        except Exception as e:
            print(e)
            print("\n")
            serial = None

    # load configfile for arduinos
    exists, json = load_json("arduino")
    if exists:

        # update arduino serial ports
        enabled = []
        for arduino in arduinos:
            found = False
            for entity in json:
                if entity["id"] == arduino["id"]:
                    entity["serial_port"] = arduino["serial_port"]
                    entity["serial_baud"] = arduino["serial_baud"]
                    found = True
                    break
            if not found:
                json.append(arduino)
            enabled.append(arduino["id"])

        # enable connected arduinos
        for entity in json:
            entity["enabled"] = (entity["id"] in enabled)

        save_json(json, "arduino")
        return json
    else:
        save_json(arduinos, "arduino")
        from sys import exit
        exit("New arduino config, please adjust each pin range and restart")


class Generate:

    def __init__(self):
        arduinos = initialise_arduinos()

        # generate instances for each pin in use
        self.instances = {}
        for member in PinConfig["AllocationMap"]:
            name = member["name"]
            if name == "GPIO":
                for nr in range(member["range"][0], member["range"][1]):
                    self.instances[nr] = GPIOPin(nr)

        for arduino in arduinos:
            from lightstorm.pins.extension_arduino import ArduinoExtension
            if arduino["enabled"]:
                ext = ArduinoExtension(
                    arduino["range"][0],
                    arduino["range"][1],
                    arduino["serial_port"],
                    arduino["serial_baud"],
                )
                for pin in ext.initialize():
                    self.instances[pin.pin_nr] = pin


InstancePins = Generate().instances
