from serial import Serial
from .extension import Extension
from threading import Lock
from .arduino_pin import ArduinoPin


class ArduinoExtension(Extension):

    def __init__(self, pin_start, pin_end, serial_port: str, serial_baud: int):
        super().__init__()
        self.pin_start = pin_start
        self.pin_end = pin_end
        self.serial_port = serial_port
        self.serial_baud = serial_baud
        self.serial = None
        self.get_serial()
        self.lock = Lock()

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
        self.lock.acquire()
        serial = self.get_serial()
        try:
            if serial:
                for n in range(5):
                    tmp = [0xAA, 0xAA, nr, cmd, len(data)] + data
                    serial.reset_input_buffer()
                    serial.write(tmp + [sum(tmp) % 256])
                    if not reliable:
                        break
                    res = serial.read()
                    if not len(res) or res[0] > 0:
                        break
        except Exception as e:
            print(e)
            self.serial = None
        self.lock.release()
