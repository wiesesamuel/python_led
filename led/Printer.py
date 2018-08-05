from config import Settings


class Printer:

    @staticmethod
    def println(string):
        if Settings["verbose"]:
            print(string)


printer = Printer
