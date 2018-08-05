from config import Settings


def println(string):
    if Settings["verbose"]:
        print(string)


def getBoolean(string):
    if string == "0":
        return 1, 0
    if string == "1":
        return 1, 1
    println("ERROR! Boolean Expected, Argument has no effect!")
    return 0
