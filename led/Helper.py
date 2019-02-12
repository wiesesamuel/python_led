from defaults import Settings, PROJECT_DIR, Meta, CONFIGURATION
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


def load_json(ctrl):
    try:
        with open(os.path.join(PROJECT_DIR, str(ctrl) + ".json"), "r") as f:
            return 1, json.load(f)
    except Exception:
        return 0, 0


def save_json(dic, ctrl):
    if Settings["save-json"]:
        with open(os.path.join(PROJECT_DIR, str(ctrl) + ".json"), "w") as f:
            json.dump(dic, f, indent=4)


def load_configuration(json_id):
    print("load " + str(json_id))
    if Settings["load-json"]:
        result = load_json(json_id)
        if result[0]:
            print(result[1])
            return result[1]
    for name, id in Meta.items():
        print(name)
        print(id)
        if id == json_id:
            return dict(CONFIGURATION[name])
