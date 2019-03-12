from.pin import Pin


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
