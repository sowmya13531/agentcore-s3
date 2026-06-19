from strands import tool

MOCK_DEVICES = [
    {"id": "dev-1", "name": "HVAC System",        "type": "climate",   "power_draw_w": 3500, "is_on": True},
    {"id": "dev-2", "name": "Water Heater",        "type": "appliance", "power_draw_w": 4500, "is_on": False},
    {"id": "dev-3", "name": "Pool Pump",           "type": "appliance", "power_draw_w": 1500, "is_on": True},
    {"id": "dev-4", "name": "EV Charger",          "type": "vehicle",   "power_draw_w": 7200, "is_on": False},
    {"id": "dev-5", "name": "Living Room Lights",  "type": "lighting",  "power_draw_w": 150,  "is_on": True},
    {"id": "dev-6", "name": "Refrigerator",        "type": "appliance", "power_draw_w": 800,  "is_on": True},
    {"id": "dev-7", "name": "Dishwasher",          "type": "appliance", "power_draw_w": 1200, "is_on": True},
]

@tool
def get_device_status(device_name: str) -> dict:
    """Get the current on/off status and power draw of a device by name."""
    print(f"[TOOL] get_device_status called: {device_name}")
    for device in MOCK_DEVICES:
        if device["name"].lower() == device_name.lower():
            return {
                "device": device["name"],
                "is_on": device["is_on"],
                "power_draw_w": device["power_draw_w"]
            }
    return {"error": f"Device '{device_name}' not found"}

@tool
def toggle_device(device_name: str, state: str) -> dict:
    """Turn a device on or off. State must be 'on' or 'off'."""
    print(f"[TOOL] toggle_device called: {device_name} -> {state}")
    state = state.lower()
    if state not in ["on", "off"]:
        return {"success": False, "error": "State must be 'on' or 'off'"}
    for device in MOCK_DEVICES:
        if device["name"].lower() == device_name.lower():
            device["is_on"] = (state == "on")
            return {"success": True, "device": device["name"], "new_state": state}
    return {"success": False, "error": f"Device '{device_name}' not found"}