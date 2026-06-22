from strands import tool

# Mock device database
MOCK_DEVICES = {
    "hvac": {
        "id": "hvac",
        "name": "HVAC System",
        "state": "OFF"
    },
    "water_heater": {
        "id": "water_heater",
        "name": "Water Heater",
        "state": "OFF"
    },
    "pool_pump": {
        "id": "pool_pump",
        "name": "Pool Pump",
        "state": "OFF"
    },
    "ev_charger": {
        "id": "ev_charger",
        "name": "EV Charger",
        "state": "OFF"
    },
    "living_room_lights": {
        "id": "living_room_lights",
        "name": "Living Room Lights",
        "state": "OFF"
    },
    "refrigerator": {
        "id": "refrigerator",
        "name": "Refrigerator",
        "state": "ON"
    },
    "dishwasher": {
        "id": "dishwasher",
        "name": "Dishwasher",
        "state": "OFF"
    }
}


def _find_device(device_name: str):
    """Helper function to locate a device."""

    device_name = device_name.lower().strip()

    for device in MOCK_DEVICES.values():

        if (
            device["name"].lower() == device_name
            or device["id"].lower() == device_name
            or device_name in device["name"].lower()
        ):
            return device

    return None


@tool
def get_device_status(device_name: str):
    """
    Get current status of a specific device.
    """

    print(f"[TOOL] get_device_status called: {device_name}")

    device = _find_device(device_name)

    if not device:
        return {
            "success": False,
            "error": f"Device '{device_name}' not found"
        }

    return {
        "success": True,
        "device": device["name"],
        "state": device["state"]
    }


@tool
def toggle_device(device_name: str, state: str):
    """
    Turn a device ON or OFF.
    """

    print("=" * 50)
    print("TOOL EXECUTION")
    print(f"Device : {device_name}")
    print(f"Action : {state}")
    print("=" * 50)

    device = _find_device(device_name)

    if not device:
        return {
            "success": False,
            "error": f"Device '{device_name}' not found"
        }

    state = state.upper()

    if state not in ["ON", "OFF"]:
        return {
            "success": False,
            "error": "State must be ON or OFF"
        }

    device["state"] = state

    return {
        "success": True,
        "device": device["name"],
        "new_state": state
    }


@tool
def list_all_devices() -> str:
    """List all available smart devices with their current status."""

    print("LIST_ALL_DEVICES TOOL CALLED")

    device_list = []
    total_power = 0
    active_count = 0

    for device_id, device_info in DEVICES_DB.items():

        status = "ON" if device_info["is_on"] else "OFF"

        device_list.append(
            f"• {device_info['name']}: {status} ({device_info['power_draw_w']}W)"
        )

        if device_info["is_on"]:
            total_power += device_info["power_draw_w"]
            active_count += 1

    response = "📱 All Devices:\n\n"
    response += "\n".join(device_list)
    response += (
        f"\n\nSummary: {active_count} active, "
        f"{total_power}W total"
    )

    return response