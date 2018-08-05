from .Instance_Generator import Instance
from config import ControllerConfig, InstanceControll

class InstanceController:

    def __init__(self, states):
        i = 0
        for part in states:
            self.States[i] = part
            i += 1

    def set_instance(self, instanceNr, groupNr):
        pins = []
        for i in Instance[instanceNr][groupNr].instance:
            pins.append(i.pin_nr)
        pin = groupNr

        if instanceNr > 1:
            pin =  ControllerConfig[]

    def setState(self, instanceNr, value):
        InstanceControll["InstanceStates"][instanceNr] = value

    def    
