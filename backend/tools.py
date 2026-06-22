from strands import tool

DEVICES_DB = {
    "hvac": {"name": "HVAC System", "is_on": True, "power_draw_w": 3500},
    "dishwasher": {"name": "Dishwasher", "is_on": False, "power_draw_w": 1800},
    "water_heater": {"name": "Water Heater", "is_on": False, "power_draw_w": 4500},
    "refrigerator": {"name": "Refrigerator", "is_on": True, "power_draw_w": 150},
    "lights_living": {"name": "Living Room Lights", "is_on": True, "power_draw_w": 60},
    "lights_bedroom": {"name": "Bedroom Lights", "is_on": False, "power_draw_w": 40},
}

@tool
def list_all_devices() -> str:
    """List all available smart devices with their status."""
    device_list = []
    total_power = 0
    active_count = 0
    
    for device_id, device_info in DEVICES_DB.items():
        status = "ON" if device_info["is_on"] else "OFF"
        device_list.append(f"• {device_info['name']}: {status} ({device_info['power_draw_w']}W)")
        
        if device_info["is_on"]:
            total_power += device_info["power_draw_w"]
            active_count += 1
    
    response = "📱 **All Devices:**\n\n" + "\n".join(device_list)
    response += f"\n\n**Summary:** {active_count} active, {total_power}W total consumption"
    return response

@tool
def get_device_status(device_name: str) -> str:
    """Get the current status of a specific device."""
    for device_id, device_info in DEVICES_DB.items():
        if device_name.lower() in device_info["name"].lower():
            status = "ON" if device_info["is_on"] else "OFF"
            return f"**{device_info['name']}**: {status} ({device_info['power_draw_w']}W)"
    return f"Device '{device_name}' not found."

@tool
def toggle_device(device_name: str, action: str) -> str:
    """Turn a device ON or OFF."""
    action = action.upper()
    for device_id, device_info in DEVICES_DB.items():
        if device_name.lower() in device_info["name"].lower():
            new_state = action == "ON"
            DEVICES_DB[device_id]["is_on"] = new_state
            return f"✅ **{device_info['name']} turned {action}**"
    return f"Device '{device_name}' not found."

@tool
def get_energy_saving_tips() -> str:
    """Provide energy-saving recommendations."""
    tips = [
        "💡 Use LED bulbs - 75% less energy",
        "❄️ Adjust thermostat 1-2 degrees",
        "🚰 Lower water heater to 120°F",
        "🔌 Unplug devices to stop phantom drain",
        "⏰ Shift usage to off-peak hours (9PM-6AM)",
    ]
    return "💰 **Energy Saving Tips:**\n\n" + "\n".join(tips)
