from defaults import Settings, PROJECT_DIR, JSON_FILES, CONFIGURATION
import json
import os
from time import sleep


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


def load_json(target):
    try:
        with open(JSON_FILES[target], "r") as f:
            return 1, json.load(f)
    except Exception:
        return 0, 0


def save_json(dic):
    if Settings["save-json"]:
        with open(os.path.join(PROJECT_DIR, dic["name"] + ".json"), "w") as f:
            json.dump(dic, f, indent=4)


def save_json(dic, ctrl, nr):
    if Settings["save-json"]:
        with open(os.path.join(PROJECT_DIR, str(ctrl) + "_" + str(nr) + ".json"), "w") as f:
            json.dump(dic, f, indent=4)


def stop_instance(instance):
    if instance.running:
        instance.stop()
        while not instance.idle:
            sleep(0.0001)


def load_configuration(conf):
    if Settings["load-json"]:
        result = load_json(conf)
        if result[0]:
            return result[1]
    return dict(CONFIGURATION[conf])
