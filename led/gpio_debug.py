class GPIO:
    BCM = 0
    OUT = 0
    BOARD = 0
    Board = 0

    @staticmethod
    def cleanup():
        pass

    @staticmethod
    def setwarnings(a1):
        pass

    @staticmethod
    def setmode(a1):
        pass

    @staticmethod
    def setup(a1, a2):
        pass

    @staticmethod
    def output(a1, a2):
        pass

    @staticmethod
    def PWM(a1, a2):
        pass

    class PWM:

        def __init__(self, a, b):
            pass

        @staticmethod
        def ChangeDutyCycle(x):
            pass

        @staticmethod
        def ChangeFrequency(y):
            pass

        @staticmethod
        def start(x):
            pass

        @staticmethod
        def stop():
            pass

class NOISE:
    @staticmethod
    def pnoise1(a, b):
        pass
