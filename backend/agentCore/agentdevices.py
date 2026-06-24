# agentdevices.py

import json
import os
import boto3
from botocore.exceptions import ClientError

# ============================================================================
# S3 CONFIGURATION
# ============================================================================

BUCKET_NAME = "voltstream-device-store"

FILE_KEY = "devices.json"

s3 = boto3.client("s3")

print(f"BUCKET_NAME = {BUCKET_NAME}")
print(f"FILE_KEY = {FILE_KEY}")


# ============================================================================
# LOAD DEVICES FROM S3
# ============================================================================

def load_devices():
    """
    Load devices from S3.
    Returns a dictionary of devices.
    """

    try:
        print(f"Loading devices from s3://{BUCKET_NAME}/{FILE_KEY}")

        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=FILE_KEY
        )

        content = response["Body"].read().decode("utf-8")

        print("Raw S3 content:")
        print(content)

        devices = json.loads(content)

        print(f"Loaded {len(devices)} devices")

        return devices

    except ClientError as e:
        print(f"S3 ClientError: {e}")
        return {}

    except Exception as e:
        print(f"S3 load error: {e}")
        return {}


# ============================================================================
# SAVE DEVICES TO S3
# ============================================================================

def save_devices(devices):
    """
    Save updated devices back to S3.
    """

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_KEY,
            Body=json.dumps(devices, indent=2),
            ContentType="application/json"
        )

        print(
            f"Saved {len(devices)} devices "
            f"to s3://{BUCKET_NAME}/{FILE_KEY}"
        )

        return True

    except ClientError as e:
        print(f"S3 ClientError while saving: {e}")
        return False

    except Exception as e:
        print(f"S3 save error: {e}")
        return False


# ============================================================================
# OPTIONAL HEALTH CHECK
# ============================================================================

def test_s3_connection():
    """
    Useful for debugging AgentCore startup.
    """

    try:
        s3.head_bucket(Bucket=BUCKET_NAME)

        print("✅ S3 bucket accessible")

        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            MaxKeys=10
        )

        keys = [
            obj["Key"]
            for obj in response.get("Contents", [])
        ]

        print("Files in bucket:")
        print(keys)

        return True

    except Exception as e:
        print(f"❌ S3 connection failed: {e}")
        return False


# ============================================================================
# LOCAL TEST
# ============================================================================

if __name__ == "__main__":

    test_s3_connection()

    devices = load_devices()

    print("\nDevices loaded:")
    print(json.dumps(devices, indent=2))