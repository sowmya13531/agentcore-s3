from strands import Agent
from strands.tools import tool
from strands.models import BedrockModel

from .tools import (get_energy_saving_tips, get_energy_consumption_breakdown, estimate_monthly_cost)


model = BedrockModel(
    model_id="global.amazon.nova-2-lite-v1:0",
    region_name="ap-south-1"
)

energy_agent = Agent(
    model=model,
    system_prompt="""
You are Energy Advisor Agent.

Responsibilities:
- Energy tips
- Consumption analysis
- Power optimization
- cost estimations and savings

Always use tools.
only provide information based on tool outputs.
generate or summarize response within 50 words.
""",
    tools=[
        get_energy_saving_tips, get_energy_consumption_breakdown,
        estimate_monthly_cost
    ]
)