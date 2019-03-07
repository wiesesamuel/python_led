from serial import Serial
from .extension import Extension
from .instance_pins import Pin


class ArduinoPin(Pin):

    def __init__(self, ext, pin_nr):
        super().__init__(pin_nr)
        self.ext = ext
        self.state = 0
        self.brightness = 0
        self.frequency = 0
        self.pin_nr_ext = pin_nr - ext.pin_start

    def set_state(self, value):
        self.state = value
        self.update()

    def set_brightness(self, value):
        self.brightness = value
        self.ext.write(self.pin_nr_ext, 0, [int(value)])

    def set_frequency(self, value):
        self.frequency = value
        self.ext.write(self.pin_nr_ext, 1, [min(value, 255)])

    def update(self):
        if self.state:
            self.ext.write(self.pin_nr_ext, 0, [int(self.brightness)])
            self.ext.write(self.pin_nr_ext, 1, [min(self.frequency, 255)])
        else:
            self.ext.write(self.pin_nr_ext, 0, [0])


class ArduinoExtension(Extension):

    def __init__(self, pin_start, pin_end, serial_port: str, serial_baud: int):
        super().__init__()
        self.pin_start = pin_start
        self.pin_end = pin_end
        self.serial_port = serial_port
        self.serial_baud = serial_baud
        self.serial = None
        self.get_serial()

    def initialize(self):
        pins = []
        for pin in range(self.pin_start, self.pin_end + 1):
            pins.append(ArduinoPin(self, pin))
        return pins

    def get_serial(self):
        try:
            if not self.serial or not self.serial.is_open:
                self.serial = Serial(self.serial_port, self.serial_baud, timeout=0.01)
            return self.serial
        except Exception as e:
            self.serial = None
            print(e)

    def write(self, nr, cmd, data, reliable=True):
        serial = self.get_serial()
        try:
            if serial:
                for n in range(5):
                    tmp = [0xAA, 0xAA, nr, cmd, len(data)] + data
                    serial.reset_input_buffer()
                    serial.write(tmp)
                    serial.write([sum(tmp) % 256])
                    if not reliable:
                        break
                    res = serial.read()
                    if not len(res) or res[0] > 0:
                        break
        except Exception as e:
            str(e)
            self.serial = None
