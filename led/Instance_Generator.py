from config import ControllerConfig
from .pin import Pin
from .Printer import printer
from .Pin_Thread import PinThread
from .Group_Thread import GroupThread


class InstancePin:
    Instances = [None] * ControllerConfig["PinCount"]

    def __init__(self):
        # generate instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.Instances[pinNr] = Pin(pinNr)
            else:
                printer.println("A pin in 'PinsInUse' is higher than 'PinCount'")


class InstancePinThread:
    InstancesPin = [None] * ControllerConfig["PinCount"]

    def __init__(self, PinInstances):
        # generate Thread instances for each pin in use
        for pinNr in ControllerConfig["PinsInUse"]:
            if pinNr < ControllerConfig["PinCount"]:
                self.InstancesPin[pinNr] = PinThread(PinInstances[pinNr])
            else:
                printer.println("A pin in 'PinsInUse' is higher than 'PinCount'")


class InstanceStripeThread:
    InstancesStripe = [None] * len(ControllerConfig["Stripes"])

    def __init__(self, PinInstances):
        # generate Thread instances for each stripe group declared
        count = 0
        for stripe in ControllerConfig["Stripes"]:
            tmpInstanceMap = []
            for pinNr in stripe:
                if pinNr < ControllerConfig["PinCount"]:
                    tmpInstanceMap.append(PinInstances[pinNr])
                else:
                    printer.println("A pin in 'Stripes' is higher than 'PinCount'")
            self.InstancesStripe[count] = GroupThread(tmpInstanceMap)
            count += 1


class InstanceColorThread:
    InstancesColor = [None] * len(ControllerConfig["Colors"])

    def __init__(self, PinInstances):
        # generate Thread instances for each color group declared
        count = 0
        for color in ControllerConfig["Colors"]:
            tmpInstanceMap = []
            for pinNr in color:
                if pinNr < ControllerConfig["PinCount"]:
                    tmpInstanceMap.append(PinInstances[pinNr])
                else:
                    printer.println("A pin in 'Color' is higher than 'PinCount'")
            self.InstancesColor[count] = GroupThread(tmpInstanceMap)
            count += 1


Instances = InstancePin().Instances
InstancesPin = InstancePinThread(Instances).InstancesPin
InstancesStripe = InstanceStripeThread(Instances).InstancesStripe
InstancesColor = InstanceColorThread(Instances).InstancesColor
Instance = [Instances, InstancesPin, InstancesStripe, InstancesColor]
