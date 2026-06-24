from strands import Agent
from strands.tools import tool
from strands.models import BedrockModel
from .tools import list_all_devices, toggle_device, get_device_status, toggle_multiple_devices, execute_device_actions

model = BedrockModel(
    model_id="global.amazon.nova-2-lite-v1:0",
    region_name="ap-south-1"
)

device_agent = Agent(
    model=model,
    system_prompt="""
    You are Device Control Agent.

    Responsibilities:
    - List devices
    - Get device status
    - Turn devices ON/OFF

    Always use tools.
    don't proceed without using tools for device operations.
    """,
    tools=[
        list_all_devices,
        get_device_status,
        toggle_device, 
        toggle_multiple_devices, 
        execute_device_actions
    ]
)
