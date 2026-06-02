import boto3

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-south-1"
)