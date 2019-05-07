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
            self.a = a
            self.b = b
            pass

        def ChangeDutyCycle(self, x):
            self.x = x
            pass

        def ChangeFrequency(self, y):
            self.y = y
            pass

        def start(self, x):
            print(x)
            pass

        def stop(self):
            print(self)
            pass
