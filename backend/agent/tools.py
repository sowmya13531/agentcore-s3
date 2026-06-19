from strands import tool
MOCK_DEVICES = {
    "dishwasher": {"id": "dishwasher", "name": "Dishwasher", "state": "OFF"},
    "lights": {"id": "lights", "name": "Lights", "state": "OFF"},
    # add whatever devices your mock_data.py had
}


@tool
def get_device_status(device_name: str):
    """Get current status of a device."""

    print(f"[TOOL] get_device_status called: {device_name}")

    for device in MOCK_DEVICES:
        if device.name.lower() == device_name.lower():
            return {
                "device": device.name,
                "is_on": device.is_on,
                "power_draw_w": device.power_draw_w
            }

    return {"error": f"Device '{device_name}' not found"}


@tool
def toggle_device(device_name: str, state: str):
    """Turn a device on or off."""

    print("=" * 50)
    print("TOOL EXECUTION")
    print(f"Device : {device_name}")
    print(f"Action : {state}")
    print("=" * 50)

    state = state.lower()

    if state not in ["on", "off"]:
        return {
            "success": False,
            "error": "State must be 'on' or 'off'"
        }

    for device in MOCK_DEVICES:
        if device.name.lower() == device_name.lower():

            device.is_on = (state == "on")

            return {
                "success": True,
                "device": device.name,
                "new_state": state
            }

    return {
        "success": False,
        "error": f"Device '{device_name}' not found"
    }