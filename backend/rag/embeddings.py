import json
from bedrock_client import bedrock

def get_embedding(text):
    body = {
        "inputText": text
    }

    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    return result["embedding"]