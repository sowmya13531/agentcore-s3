from bedrock_client import bedrock

response = bedrock.converse(
    modelId="global.amazon.nova-2-lite-v1:0",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": "Hello"
                }
            ]
        }
    ]
)

print(response["output"]["message"]["content"][0]["text"])