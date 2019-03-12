from lightstorm import config

from .controller_simple import ControllerMono
from .controller_single_mode import ControllerThreadsSingle
from .controller_group_mode import ControllerThreadsGroup
from .controller_lightshowpi import ControllerLightshowpi

CtrlMono = ControllerMono()
CtrlSingle = ControllerThreadsSingle()
CtrlGroup = ControllerThreadsGroup()
CtrlLsp = ControllerLightshowpi()

CTRL = [CtrlMono, CtrlSingle, CtrlGroup, CtrlLsp]


class MasterController:

    def __init__(self):
        self.configuration = config.CONFIGURATION["master"]
        self.update_all()

    def set_master(self, ctrl, state):
        self.configuration["master_state"][ctrl] = state
        self.update_all()

    def flip_master(self, ctrl):
        self.set_master(ctrl, not self.configuration["master_state"][ctrl])

    def set_single(self, ctrl, nr, state):
        CTRL[ctrl].set_single(nr, state)
        self.update_single(nr)

    def flip_single(self, ctrl, nr):
        self.set_single(ctrl, nr, not CTRL[ctrl].get_single_state(nr))

    def unify_group(self, ctrl, group):
        value = 1
        for nr in group:
            if CTRL[ctrl].get_single_state(nr):
                value = 0
                break
        for nr in group:
            self.set_single(ctrl, nr, value)

    def update_all(self):
        for nr in range(config.ControllerConfig["PinCount"]):
            self.update_single(nr)

    def update_single(self, nr):
        controller, index = self.get_controller_in_use(nr)
        # shut other controller pin off
        for ctrl in CTRL:
            if ctrl is not controller:
                ctrl.set_state(nr, 0)

        if controller is not None:
            controller.set_state(nr, 1)
            self.configuration["state"][nr] = index
        else:
            self.configuration["state"][nr] = -1

    # choose pin controller in use by priority
    def get_controller_in_use(self, nr):
        ctrl, controller = None, None

        for highest_member in config.ControllerPriority:
            ctrl = config.Meta[highest_member]
            if self.configuration["master_state"][ctrl] and CTRL[ctrl].get_single_state(nr):
                controller = CTRL[ctrl]
                break

        return controller, ctrl

    def change_profile(self, ctrl, nr):
        CTRL[ctrl].select_profile(nr)
        self.update_all()

    def get_single_state(self, ctrl, nr):
        in_use = 0
        if self.configuration["state"][nr] == ctrl:
            in_use = 1
        # return on, inUse
        return CTRL[ctrl].get_single_state(nr), in_use


CtrlMaster = MasterController()
