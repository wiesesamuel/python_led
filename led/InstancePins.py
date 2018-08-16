from config import ControllerConfig, PinConfig
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
        elif PinConfig["GPIO_mode"] == "BOARD":
            GPIO.setmode(GPIO.BOARD)
        else:
            raise ValueError("GPIO_mode has to be 'BCM' or 'BOARD'! '" + PinConfig["GPIO_mode"] + "' is not allowed")
        GPIO.setup(pin_nr, GPIO.OUT)
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
        if self.state and not self.blocked:
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


class Pins:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self):
        # generate instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.Instances[pinNr] = Pin(pinNr)
            else:
                raise ValueError("The pin(" + pinNr + ") in 'PinsInUse' is higher than 'PinCount'(" +
                                 ControllerConfig["PinCount"] + ")")


InstancePins = Pins().Instances


class Master:

    def __init__(self):
        self.pieces = len(InstancePins)
        c0 = ControllerMono(InstancePins)
        c1 = ControllerThreadsSingle(InstancesThreadSingle(InstancePins).Instances)
        c2 = ControllerThreadsGroup(InstancesThreadGroup(InstancePins).Instances)
        c3 = ControllerLightshowpi(lsp_settings, lsp_profile[lsp_settings["default_profile"]], self.pieces)
        self.controller = [c0, c1, c2, c3]
        self.monitor = [[0, 0, 0, 0]] * self.pieces
        self.master_state = [0, 0, 0, 0]

    def set_master(self, meta, value):
        if self.master_state[meta] != value:
            self.master_state[meta] = value
            self.update_all_controller()

    def flip_master(self, meta):
        self.set_master(meta, not self.master_state[meta])

    def update_all_controller(self):
        if self.master_state[0]:
            # update ControllerMono
            self.update_single_controller(0)
            if self.master_state[2]:
                if self.master_state[1]:
                    # manipulate pins in ControllerSingle if there's a conflict with ControllerGroup
                    for pin in range(self.pieces):
                        if self.monitor[pin][1] and self.monitor[pin][2]:
                            self.set_single(1, pin, 0)
                            self.set_single(2, pin, 1)
                            #self.controller[1].set_single(pin, 0)
                            #self.controller[2].set_single(pin, 1)
                        else:
                            # update ControllerSingle and ControllerGroup
                            self.set_single(1, pin, self.monitor[pin][1])
                            self.set_single(2, pin, self.monitor[pin][2])
                            #self.controller[1].set_single(pin, self.monitor[pin][1])
                            #self.controller[2].set_single(pin, self.monitor[pin][2])
                    self.controller[1].set_master(1)
                    self.controller[2].set_master(1)
                else:
                    self.controller[1].set_master(0)
                    # update ControllerGroup
                    self.update_single_controller(2)
            else:
                self.controller[2].set_master(0)
                if self.master_state[1]:
                    # update ControllerSingle
                    self.update_single_controller(1)
                else:
                    self.controller[1].set_master(0)
        # shut all down
        else:
            for i in range(3):
                self.controller[i].set_master(0)

    def update_single_controller(self, meta):
        for pin in range(self.pieces):
            self.set_single(meta, pin, self.monitor[pin][meta])
            #self.controller[meta].set_single(pin, self.monitor[pin][meta])
        self.controller[meta].set_master(self.master_state[meta])

    def set_single(self, meta, pin, value):
        # check if lsp uses the pin
        if self.master_state[3] and self.monitor[pin][3]:
            value = 0
            # maybe add kill meta = 1,2
        self.controller[meta].set_single(pin, value)

    def update_single_pin(self, meta, pin):
        if self.master_state[0]:
            # manipulate pins in ControllerSingle if there's a conflict with ControllerGroup
            if meta and self.monitor[pin][1] and self.monitor[pin][2]:
                self.set_single(1, pin, 0)
                self.set_single(2, pin, 1)
                #self.controller[1].set_single(pin, 0)
                #self.controller[2].set_single(pin, 1)
            else:
                # update
                self.set_single(meta, pin, self.monitor[pin][meta])
                #self.controller[meta].set_single(pin, self.monitor[pin][meta])
        # shut all down
        else:
            for i in range(3):
                self.controller[i].set_master(0)

    def set_pin_state(self, meta, pin, value):
        self.monitor[pin][meta] = value
        self.update_single_pin(meta, pin)

    def flip_single(self, meta, pin):
        self.set_pin_state(meta, pin, not self.monitor[pin][meta])

    def unify_group(self, meta, group):
        value = 1
        for nr in group:
            if self.monitor[nr][meta]:
                value = 0
                break
        for nr in group:
            self.monitor[nr][meta] = value
            self.update_single_pin(meta, nr)
