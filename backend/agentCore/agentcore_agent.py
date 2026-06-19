from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore import BedrockAgentCoreApp

from tools import get_device_status, toggle_device

app = BedrockAgentCoreApp()

model = BedrockModel(
    model_id="global.amazon.nova-2-lite-v1:0",
    region_name="ap-south-1"
)

agent = Agent(
    model=model,
    tools=[get_device_status, toggle_device],
    system_prompt="You are VoltStream Device Control Agent. Always use tools. Respond in plain text only."
)

@app.entrypoint
def handler(request):
    prompt = request.get("prompt", "")
    result = agent(prompt)
    return {"response": str(result)}

if __name__ == "__main__":
    app.run()