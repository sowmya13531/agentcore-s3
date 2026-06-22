"""
VoltStream AgentCore Agent - Week 5
Proper Strands Agent with BedrockAgentCoreApp
Based on official Week 5 guide
"""

from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool  # CORRECT: from strands.tools, NOT bedrock_agentcore
from bedrock_agentcore import BedrockAgentCoreApp


# Initialize the AgentCore app wrapper
app = BedrockAgentCoreApp()

# device_db.py

DEVICES_DB = {
    "dev-1": {
        "id": "dev-1",
        "name": "HVAC System",
        "type": "climate",
        "power_draw_w": 3500,
        "is_on": True,
    },
    "dev-2": {
        "id": "dev-2",
        "name": "Water Heater",
        "type": "appliance",
        "power_draw_w": 4500,
        "is_on": False,
    },
    "dev-3": {
        "id": "dev-3",
        "name": "Pool Pump",
        "type": "appliance",
        "power_draw_w": 1500,
        "is_on": True,
    },
    "dev-4": {
        "id": "dev-4",
        "name": "EV Charger",
        "type": "vehicle",
        "power_draw_w": 7200,
        "is_on": False,
    },
    "dev-5": {
        "id": "dev-5",
        "name": "Living Room Lights",
        "type": "lighting",
        "power_draw_w": 150,
        "is_on": True,
    },
    "dev-6": {
        "id": "dev-6",
        "name": "Refrigerator",
        "type": "appliance",
        "power_draw_w": 800,
        "is_on": True,
    },
    "dev-7": {
        "id": "dev-7",
        "name": "Dishwasher",
        "type": "appliance",
        "power_draw_w": 1200,
        "is_on": True,
    },
}

# In-memory device state store


# ============================================================================
# TASK 1: TOGGLE DEVICE
# ============================================================================
@tool
def toggle_device(device_name: str, action: str) -> str:
    """
    Turn a device ON or OFF.
    Checks current state first - if already in requested state, confirms without changing.
    
    Args:
        device_name: Name of the device to control
        action: Either "ON" to turn on or "OFF" to turn off
    
    Returns:
        Status message confirming the device action or current state
    """
    action = action.upper()
    if action not in ["ON", "OFF"]:
        return f"Invalid action. Please use 'ON' or 'OFF'."
    
    for device_id, device_info in DEVICES_DB.items():
        if device_name.lower() in device_info["name"].lower():
            current_state = device_info["is_on"]
            desired_state = action == "ON"
            
            # Check if device is already in the requested state
            if current_state == desired_state:
                status_word = "already ON" if action == "ON" else "already OFF"
                return f"ℹ️ **{device_info['name']} is {status_word}**"
            
            # Toggle to new state
            DEVICES_DB[device_id]["is_on"] = desired_state
            save_devices(DEVICES_DB)
            return f"✅ **{device_info['name']} turned {action}**"
    
    return f"❌ Device '{device_name}' not found."


# ============================================================================
# TASK 2: ENERGY ADVISOR - GET ENERGY SAVING TIPS
# ============================================================================
@tool
def get_energy_saving_tips() -> str:
    """
    Provide energy-saving recommendations to help reduce electricity bills.
    Returns actionable tips based on industry best practices.
    
    Returns:
        String with formatted energy-saving recommendations
    """
    tips = [
        "💡 **Lighting**: Replace with LED bulbs - saves 75% energy",
        "❄️ **HVAC**: Adjust thermostat 1-2 degrees - saves 1-2% per degree",
        "🚰 **Water Heater**: Lower to 120°F - saves 3-5% per 10°F",
        "🍽️ **Appliances**: Run with full loads only",
        "🔌 **Standby Power**: Unplug devices - eliminates phantom drain",
        "⏰ **Peak Hours**: Shift usage to 9PM-6AM for lower rates",
    ]
    return "💰 **Energy Saving Tips:**\n\n" + "\n".join(tips)


# ============================================================================
# SUPPORTING TOOLS
# ============================================================================
@tool
def get_device_status(device_name: str) -> str:
    """Get the current status of a specific device."""
    for device_id, device_info in DEVICES_DB.items():
        if device_name.lower() in device_info["name"].lower():
            status = "ON" if device_info["is_on"] else "OFF"
            return f"**{device_info['name']}**: {status} ({device_info['power_draw_w']}W)"
    return f"Device '{device_name}' not found."


@tool
def list_all_devices() -> str:
    """List all available smart devices with their current status."""
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
    response += f"\n\n**Summary:** {active_count} active, {total_power}W total"
    return response


@tool
def get_energy_consumption_breakdown() -> str:
    """Get breakdown of current energy consumption by active devices."""
    active_devices = [(d['name'], d['power_draw_w']) for d in DEVICES_DB.values() if d['is_on']]
    if not active_devices:
        return "No devices are currently on."
    
    active_devices.sort(key=lambda x: x[1], reverse=True)
    response = "⚡ **Energy Consumption:**\n\n"
    total = sum(p for _, p in active_devices)
    
    for name, power in active_devices:
        response += f"• {name}: {power}W\n"
    
    response += f"\n**Total: {total}W ({total/1000:.2f}kW)**"
    return response


# ============================================================================
# STRANDS AGENT WITH BEDROCK
# ============================================================================
model = BedrockModel(
    model_id="global.amazon.nova-2-lite-v1:0",
    region_name="ap-south-1"
)

strands_agent = Agent(
    model=model,

    system_prompt="""
You are VoltStream Energy Management Agent.

You have access to tools and MUST use them.

AVAILABLE TOOLS:

1. toggle_device(device_name, action)
2. get_device_status(device_name)
3. list_all_devices()
4. get_energy_saving_tips()
5. get_energy_consumption_breakdown()

IMPORTANT RULES:

- NEVER invent device information.
- NEVER claim you cannot perform an action if a tool exists.
- ALWAYS use tools before answering.

WHEN TO USE TOOLS:

list_all_devices()
- list all devices
- show all devices
- show device status
- list status of all devices
- what devices are available
- what devices do I have
- which devices are running
- which devices are on
- show running devices

get_device_status(device_name)
- status of HVAC
- check refrigerator
- is dishwasher on
- check a specific device

toggle_device(device_name, action)
- turn on
- turn off
- switch on
- switch off

get_energy_saving_tips()
- reduce electricity bill
- save power
- energy saving tips

get_energy_consumption_breakdown()
- energy usage
- power usage
- consumption breakdown

If a user asks for ALL devices, ALWAYS call list_all_devices().
Do not ask the user for individual device names.
""",

    tools=[
        toggle_device,
        get_energy_saving_tips,
        get_device_status,
        list_all_devices,
        get_energy_consumption_breakdown,
    ]
)



# ============================================================================
# AGENTCORE ENTRYPOINT - Called by AWS on each invocation
# ============================================================================
@app.entrypoint
async def handler(request):
    """
    Handle incoming requests from AgentCore Runtime.
    
    Args:
        request: Dictionary with 'prompt' key
    
    Returns:
        Dictionary with 'response' key containing agent output
    """
    prompt = request.get("prompt", "").strip()
    
    if not prompt:
        return {"response": "No prompt provided"}
    
    try:
        # Invoke Strands agent - it handles tool selection automatically
        result = strands_agent(prompt)
        
        # Extract text from result
        response_text = str(result)
        if hasattr(result, 'text'):
            response_text = result.text
        
        return {"response": response_text, "success": True}
    
    except Exception as e:
        return {
            "response": f"Error processing request: {str(e)}",
            "success": False
        }


if __name__ == "__main__":
    app.run()