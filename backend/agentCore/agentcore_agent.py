from bedrock_agentcore import BedrockAgentCoreApp
from coordinator_agent import handle_query

app = BedrockAgentCoreApp()


@app.entrypoint
async def handler(request):

    prompt = request.get("prompt", "").strip()

    if not prompt:
        return {
            "response": "No prompt provided",
            "success": False
        }

    try:

        response = handle_query(prompt)

        return {
            "response": response,
            "success": True
        }

    except Exception as e:

        return {
            "response": str(e),
            "success": False
        }


if __name__ == "__main__":
    app.run()