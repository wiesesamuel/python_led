from lightstorm.config import PinConfig
from .gpio_pin import GPIOPin

def initialise_arduinos():
    from serial import Serial
    from ..helper import load_json, save_json

    arduinos = []
    baud = 500000

    # handshake with arduinos
    ttys = "/dev/tty /dev/tty19 /dev/tty3 /dev/tty40 /dev/tty51 /dev/tty62 /dev/tty0 /dev/tty2 /dev/tty30 /dev/tty41 /dev/tty52 /dev/tty63 /dev/tty1 /dev/tty20 /dev/tty31 /dev/tty42 /dev/tty53 /dev/tty7 /dev/tty10 /dev/tty21 /dev/tty32 /dev/tty43 /dev/tty54 /dev/tty8 /dev/tty11 /dev/tty22 /dev/tty33 /dev/tty44 /dev/tty55 /dev/tty9 /dev/tty12 /dev/tty23 /dev/tty34 /dev/tty45 /dev/tty56 /dev/ttyAMA0 /dev/tty13 /dev/tty24 /dev/tty35 /dev/tty46 /dev/tty57 /dev/ttyprintk /dev/tty14 /dev/tty25 /dev/tty36 /dev/tty47 /dev/tty58 /dev/tty15 /dev/tty26 /dev/tty37 /dev/tty48 /dev/tty59 /dev/tty16 /dev/tty27 /dev/tty38 /dev/tty49 /dev/tty6 /dev/tty17 /dev/tty28 /dev/tty39 /dev/tty5 /dev/tty60 /dev/tty18 /dev/tty29 /dev/tty4 /dev/tty50 /dev/tty61"
    for tty in ttys.split(" "):
        print(tty)
        try:
            serial = Serial(tty, baud, timeout=0.01)
            tmp = [0xAA, 0xAA, 0, 'r', 0]
            serial.reset_input_buffer()
            msg = tmp + [sum(tmp) % 256]
            print("serial write " + str(msg))
            serial.write(msg)
            res = serial.read()
            print("serial read " + str(res))
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
