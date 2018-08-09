from time import sleep
from .InstancePins import InstancePins
from .InstanceThreads import InstancesThreadSingle, InstancesThreadGroup


class Master:

    def __init__(self):
        c0 = ControllerMono(InstancePins)
        c1 = ControllerThreadsSingle(InstancesThreadSingle(InstancePins).Instances)
        c2 = ControllerThreadsGroup(InstancesThreadGroup(InstancePins).Instances)
        self.controller = [c0, c1, c2]
        self.pieces = len(InstancePins)
        self.monitor = [[0, 0, 0]] * self.pieces
        self.master_state = [0, 0, 0]

    def set_master(self, meta, value):
        if self.master_state[meta] != value:
            self.master_state[meta] = value
            self.update_all_controller()

    def update_all_controller(self):
        if self.master_state[0]:
            # update ControllerMono
            self.update_single_controller(0)
            if self.master_state[2]:
                if self.master_state[1]:
                    # manipulate pins in ControllerSingle if there's a conflict with ControllerGroup
                    for pin in range(self.pieces):
                        if self.monitor[pin][1] and self.monitor[pin][2]:
                            self.controller[1].set_single(pin, 0)
                            self.controller[2].set_single(pin, 1)
                        else:
                            # update ControllerSingle and ControllerGroup
                            self.controller[1].set_single(pin, self.monitor[pin][1])
                            self.controller[2].set_single(pin, self.monitor[pin][2])
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
            self.controller[meta].set_single(pin, self.monitor[pin][meta])
        self.controller[meta].set_master(self.master_state[meta])

    def flip_single(self, meta, pin):
        return 0


class ControllerMono:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance
        self.state = [0] * len(instance)

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update_single(nr)

    def flip_single(self, nr):
        self.state[nr] = not self.state[nr]
        self.update_single(nr)

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.state[nr]:
                value = 0
                break
        for nr in group:
            self.state[nr] = value
            self.update_single(nr)

    def update_all(self):
        for nr in range(len(self.instance)):
            self.update_single(nr)

    def update_single(self, nr):
        if self.master_state and self.state[nr]:
            self.instance[nr].set_state(1)
        else:
            self.instance[nr].set_state(0)

    def get_state_pin(self, pin):
        return self.state[pin]


class ControllerThreadsSingle:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance  # list with objects
        self.pieces = len(instance)
        self.state = [0] * self.pieces

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update_single(nr)

    def flip_single(self, nr):
        self.state[nr] = not self.state[nr]
        self.update_single(nr)

    def unify_group(self, group):
        value = 1
        for nr in group:
            if self.state[nr]:
                value = 0
                break
        for nr in group:
            self.state[nr] = value
            self.update_single(nr)

    def update_single(self, nr):
        if self.master_state and self.state[nr]:
            if self.instance[nr].isAlive():
                self.instance[nr].restart()
            else:
                self.instance[nr].start()
                self.instance[nr].restart()
        else:
            self.stop_instance(self.instance[nr])

    def update_all(self):
        for nr in range(self.pieces):
            self.update_single(nr)

    @staticmethod
    def stop_instance(instance):
        if instance.running:
            instance.stop()
            while not instance.idle:
                sleep(0.0001)

    def get_state_pin(self, pin):
        return self.state[pin]


class ControllerThreadsGroup:
    master_state = 0

    def __init__(self, instance):
        self.instance = instance    # list with lists with objects
        self.pieces = len(instance)
        self.state = [] * self.pieces
        self.group = []
        self.groupPin = []
        for list in instance:
            self.group.append([0] * len(list))
            tmpList = []
            for inst in list:
                tmpList.append(inst.pinNr)
            self.groupPin.append(tmpList)

    def get_state_pin(self, pin):
        stateNr = 0
        for list in self.groupPin:
            groupNr = 0
            for nr in list:
                if nr == pin:
                    if self.state[stateNr] and self.group[groupNr]:
                        return 1
                    else:
                        return 0
                groupNr += 1
            stateNr += 1

    def set_master(self, state):
        if self.master_state != state:
            self.master_state = state
            self.update_all()

    def set_single(self, nr, state):
        self.state[nr] = state
        self.update_group(nr)

    def flip_single(self, nr):
        self.state[nr] = not self.state[nr]
        self.update_group(nr)

    def unify_group(self, group):
        values = [1] * len(self.state)
        for pin in group:
            stateNr = 0
            for list in self.groupPin:
                groupNr = 0
                for nr in list:
                    if nr == pin:
                        if self.group[groupNr]:
                            values[stateNr] = 0
                            break
                    groupNr += 1
                stateNr += 1

        count = 0
        for value in values:
            self.state[count] = value
            self.update_group(count)

    def update_group(self, nr):
        if self.master_state and self.state[nr]:
            if self.instance[nr].isAlive():
                self.instance[nr].restart()
            else:
                self.instance[nr].start()
                self.instance[nr].restart()
        else:
            self.stop_instance(self.instance[nr])

    def update_all(self):
        for nr in range(self.pieces):
            self.update_group(nr)

    @staticmethod
    def stop_instance(instance):
        if instance.running:
            instance.stop()
            while not instance.idle:
                sleep(0.0001)
