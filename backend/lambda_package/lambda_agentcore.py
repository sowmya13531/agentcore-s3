"""
VoltStream — AgentCore Lambda Proxy (Fixed v2)
Properly extracts actual agent response text from AgentCore
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
    """AgentCore Lambda proxy - extracts actual text response"""
    
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
    
    print(f"[LAMBDA] Invoking AgentCore with message: {message}")
    
    try:
        # Invoke AgentCore
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_ARN,
            payload=json.dumps({"prompt": message})
        )
        
        print(f"[LAMBDA] Response keys: {list(response.keys())}")
        
        # Extract text response
        reply_text = _extract_response_text(response)
        
        print(f"[LAMBDA] Extracted reply: {reply_text[:100]}")
        
        return _resp(200, {
            "reply": reply_text,
            "message": message,
            "success": True,
            "runtimeSessionId": response.get("runtimeSessionId", "unknown")
        })
    
    except Exception as e:
        print(f"[LAMBDA] ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        return _resp(500, {
            "error": "Agent invocation failed",
            "detail": str(e)[:200]
        })


def _extract_response_text(response):
    """
    Extract actual response text from AgentCore runtime
    Handles streaming response body
    """
    
    print(f"[EXTRACT] Starting response extraction")
    print(f"[EXTRACT] Response keys: {list(response.keys())}")
    
    # Method 1: Direct 'response' field (main response)
    if "response" in response:
        print(f"[EXTRACT] Found 'response' field")
        output = response["response"]
        print(f"[EXTRACT] Response type: {type(output)}")
        
        # Handle streaming body
        if hasattr(output, "read"):
            try:
                data = output.read()
                text = data.decode("utf-8", errors="replace").strip()
                
                print(f"[EXTRACT] Stream read: {len(text)} chars")
                print(f"[EXTRACT] Content: {text[:100]}")
                
                if text and text != "null" and not text.startswith("{"):
                    # Plain text response
                    print(f"[EXTRACT] Returning as plain text")
                    return text
                
                if text:
                    # Try to parse as JSON
                    try:
                        parsed = json.loads(text)
                        print(f"[EXTRACT] Parsed as JSON")
                        
                        # Extract from nested response
                        if isinstance(parsed, dict):
                            for key in ['response', 'message', 'reply', 'text', 'content']:
                                if key in parsed and isinstance(parsed[key], str):
                                    print(f"[EXTRACT] Found key '{key}'")
                                    return parsed[key]
                        
                        # Return JSON string
                        print(f"[EXTRACT] Returning as JSON string")
                        return json.dumps(parsed)
                    except json.JSONDecodeError:
                        print(f"[EXTRACT] Not JSON, returning as text")
                        return text
                        
            except Exception as e:
                print(f"[EXTRACT] Error reading stream: {e}")
        
        elif isinstance(output, str):
            print(f"[EXTRACT] Response is string")
            return output if output.strip() else "No response text"
    
    # Method 2: Check other response fields
    for field in ["output", "body", "data", "message", "result"]:
        if field in response:
            value = response[field]
            print(f"[EXTRACT] Checking field '{field}'")
            
            if hasattr(value, "read"):
                try:
                    text = value.read().decode("utf-8", errors="replace").strip()
                    if text:
                        return text
                except:
                    pass
            
            elif isinstance(value, str) and value.strip():
                return value
    
    # Method 3: Last resort
    print(f"[EXTRACT] Could not extract response - returning error message")
    return "Error: Could not extract response from AgentCore"


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