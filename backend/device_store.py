# device_store.py

import json
import boto3
import os

s3 = boto3.client("s3")

BUCKET_NAME = "voltstream-device-store"
FILE_KEY = "devices.json"

print("BUCKET_NAME =", BUCKET_NAME)
def load_devices():
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=FILE_KEY
        )

        return json.loads(
            response["Body"].read().decode("utf-8")
        )

    except Exception as e:
        print(f"S3 load error: {e}")
        return {}

def save_devices(devices):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=FILE_KEY,
        Body=json.dumps(devices, indent=2),
        ContentType="application/json"
    )