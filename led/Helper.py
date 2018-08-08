from config import Settings, PROJECT_DIR
import json
import os


def println(string):
    if Settings["verbose"]:
        print(string)


def get_boolean(string):
    if string == "0":
        return 1, 0
    if string == "1":
        return 1, 1
    println("ERROR! Boolean Expected, Argument has no effect!")
    return 0


def get_json(source):
    with open(source, "r") as f:
        return json.load(f)


def save_json(dic):
    if Settings["save-json"]:
        with open(os.path.join(PROJECT_DIR, dic["name"] + ".json"), "w") as f:
            json.dump(dic, f, indent=4)
