from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="arn:aws:bedrock:ap-south-1:211374268044:inference-profile/apac.anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name="ap-south-1"
)

agent = Agent(model=model)

print(agent("Hello"))