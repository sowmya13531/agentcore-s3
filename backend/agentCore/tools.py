"""VoltStream Agent Tools"""
from strands import tool
from .agentdevices import load_devices, save_devices


@tool
def list_all_devices() -> str:
    """List all available smart devices with their status."""
    device_list = []
    total_power = 0
    active_count = 0
    devices = load_devices()
    for device_id, device_info in devices.items():
        status = "ON" if device_info["is_on"] else "OFF"
        device_list.append(f"• {device_info['name']}: {status} ({device_info['power_draw_w']}W)")
        if device_info["is_on"]:
            total_power += device_info["power_draw_w"]
            active_count += 1
    response = "📱 **All Devices:**\n\n" + "\n".join(device_list)
    response += f"\n\n**Summary:** {active_count} active, {total_power}W total"
    return response

@tool
def get_device_status(device_name: str) -> str:
    """Get the current status of a specific device."""
    devices = load_devices()
    for device_id, device_info in devices.items():
        if device_name.lower() in device_info["name"].lower():
            status = "ON" if device_info["is_on"] else "OFF"
            return f"**{device_info['name']}**: {status} ({device_info['power_draw_w']}W)"
    return f"Device '{device_name}' not found."

@tool
def toggle_device(device_name: str, action: str) -> str:
    """Turn a device ON or OFF."""
    action = action.upper()
    if action not in ["ON", "OFF"]:
        return f"Invalid action. Use ON or OFF."
    devices = load_devices()
    for device_id, device_info in devices.items():
        if device_name.lower() in device_info["name"].lower():
            new_state = action == "ON"
            devices[device_id]["is_on"] = new_state
            save_devices(devices)
            return f"✅ **{device_info['name']} turned {action}**"
    return f"Device '{device_name}' not found."

@tool
def execute_device_actions(actions: list[dict]) -> str:
    """
    Execute multiple device actions.

    Example:
    [
      {"device":"Water Heater","action":"ON"},
      {"device":"HVAC System","action":"OFF"}
    ]
    """

    devices = load_devices()

    results = []

    for item in actions:

        device_name = item["device"]
        action = item["action"].upper()

        for device_id, device_info in devices.items():

            if device_name.lower() in device_info["name"].lower():

                devices[device_id]["is_on"] = (
                    action == "ON"
                )

                results.append(
                    f"{device_info['name']} -> {action}"
                )

                break

    save_devices(devices)

    return "\n".join(results)

@tool
def get_energy_consumption_breakdown() -> str:
    """Get breakdown of energy consumption by device."""
    devices = load_devices()
    active_devices = [(d['name'], d['power_draw_w']) for d in devices.values() if d['is_on']]
    if not active_devices:
        return "No devices are currently on."
    active_devices.sort(key=lambda x: x[1], reverse=True)
    response = "⚡ **Energy Consumption:**\n\n"
    total = sum(p for _, p in active_devices)
    for name, power in active_devices:
        response += f"• {name}: {power}W\n"
    response += f"\n**Total: {total}W ({total/1000:.2f}kW)**"
    return response

@tool
def toggle_multiple_devices(device_names: list[str], action: str) -> str:
    """
    Turn multiple devices ON or OFF.
    """

    action = action.upper()

    if action not in ["ON", "OFF"]:
        return "Action must be ON or OFF"

    updated = []

    for device_name in device_names:
        devices = load_devices()
        for device_id, device_info in devices.items():

            if device_name.lower() in device_info["name"].lower():

                devices[device_id]["is_on"] = action == "ON"

                updated.append(device_info["name"])

                break

    save_devices(devices)

    return f"Updated devices: {', '.join(updated)}"


@tool
def get_energy_saving_tips() -> str:
    """Provide energy-saving recommendations."""
    tips = [
        "💡 **Lighting**: Replace with LED bulbs - saves 75% energy",
        "❄️ **HVAC**: Adjust thermostat 1-2 degrees - saves 1-2% per degree",
        "🚰 **Water Heater**: Lower to 120°F - saves 3-5% per 10°F",
        "🍽️ **Appliances**: Run with full loads only",
        "🔌 **Standby Power**: Unplug devices - eliminates phantom drain",
        "⏰ **Peak Hours**: Shift usage to 9PM-6AM for lower rates",
    ]
    return "💰 **Energy Saving Tips:**\n\n" + "\n".join(tips)

@tool
def estimate_monthly_cost(cost_per_kwh: float = 0.15) -> str:
    """Estimate monthly electricity cost."""
    
    devices = load_devices()
    active_power_w = sum(
        d["power_draw_w"]
        for d in devices.values()
        if d["is_on"]
    )

    active_power_kw = active_power_w / 1000

    daily_kwh = active_power_kw * 8
    monthly_kwh = daily_kwh * 30
    monthly_cost = monthly_kwh * cost_per_kwh

    response = "💵 **Monthly Cost Estimate:**\n\n"
    response += f"• Current Power: {active_power_kw:.2f} kW\n"
    response += f"• Daily Usage: {daily_kwh:.2f} kWh\n"
    response += f"• Monthly Usage: {monthly_kwh:.2f} kWh\n"
    response += f"• Estimated Cost: ${monthly_cost:.2f}\n"
    response += f"\n(Based on ${cost_per_kwh}/kWh)"

    return response
