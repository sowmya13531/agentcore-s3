"""
VoltStream — AgentCore Lambda Proxy (WORKING VERSION)
Correctly reads the response StreamingBody field
"""

import json
import os
import boto3

REGION = "ap-south-1"
AGENT_ARN = os.environ.get(
    "AGENT_ARN",
    "arn:aws:bedrock-agentcore:ap-south-1:211374268044:runtime/agentcore_agent-tk2fHFEZwU"
)

client = boto3.client("bedrock-agentcore", region_name=REGION)


def handler(event, context):
    """AgentCore Lambda proxy - reads response StreamingBody"""
    
    # Handle CORS preflight
    method = event.get("requestContext", {}).get("http", {}).get("method", "POST").upper()
    if method == "OPTIONS":
        return _resp(200, {})
    
    # Parse request
    try:
        body = json.loads(event.get("body") or "{}")
        message = (body.get("message") or "").strip()
        if not message:
            return _resp(400, {"error": "'message' field is required"})
    except json.JSONDecodeError:
        return _resp(400, {"error": "Invalid JSON body"})
    
    print(f"[HANDLER] Invoking agent: {message}")
    
    try:
        # Invoke agent
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_ARN,
            payload=json.dumps({"prompt": message})
        )
        
        print(f"[HANDLER] Response received, keys: {list(response.keys())}")
        
        # Extract the actual response from the 'response' StreamingBody field
        reply_text = ""
        
        if "response" in response:
            # The actual agent response is in the 'response' field (StreamingBody)
            response_stream = response["response"]
            print(f"[HANDLER] Found 'response' field: {type(response_stream)}")
            
            if hasattr(response_stream, "read"):
                # Read the stream
                raw_data = response_stream.read()
                reply_text = raw_data.decode("utf-8", errors="replace")
                print(f"[HANDLER] Read response stream, length: {len(reply_text)}")
        
        if not reply_text:
            reply_text = "Agent did not return a response"
        
        print(f"[HANDLER] Final reply: {reply_text[:200]}")
        
        return _resp(200, {
            "reply": reply_text,
            "message": message,
            "success": True
        })
    
    except Exception as e:
        print(f"[HANDLER] ERROR: {str(e)}")
        error_msg = str(e)
        
        if "not authorized" in error_msg or "AccessDenied" in error_msg:
            return _resp(403, {"error": "Not authorized"})
        
        if "404" in error_msg or "not found" in error_msg:
            return _resp(404, {"error": "Agent not found"})
        
        return _resp(500, {"error": "Invocation failed", "detail": error_msg[:200]})


def _resp(status, body_dict):
    """Format HTTP response"""
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(body_dict),
    }