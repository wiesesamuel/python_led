class Pin:

    def __init__(self, pin_nr):
        self.pin_nr = pin_nr

    def set_state(self, value):
        raise NotImplementedError

    def set_brightness(self, value):
        raise NotImplementedError

    def set_frequency(self, value):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError
