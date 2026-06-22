import json
import os

FILE = "devices.json"


def load_devices():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_devices(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)