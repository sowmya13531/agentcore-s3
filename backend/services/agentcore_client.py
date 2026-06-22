import requests

LAMBDA_URL = "https://tebxukyxen552d6wtlzpnnudle0arvqy.lambda-url.ap-south-1.on.aws/"


def invoke_agentcore(message: str):

    response = requests.post(
        LAMBDA_URL,
        json={
            "message": message
        },
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    print("\n=== LAMBDA RESPONSE ===")
    print(result)
    print("=======================\n")

    return result