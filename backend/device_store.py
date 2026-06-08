import json

FILE = "devices.json"

def load_devices():
    with open(FILE, "r") as f:
        return json.load(f)

def save_devices(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)