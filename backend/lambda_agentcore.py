"""
VoltStream — AgentCore Lambda Proxy
Sits between the frontend and the AgentCore Runtime.
Handles CORS so the React frontend (localhost:5173 / deployed URL) can call it.

BUGS FIXED vs the submitted version:
1. Response body extraction: AgentCore's invoke_agent_runtime returns a
   streaming body in response["response"]. The submitted code read it once
   and tried to parse JSON from the raw bytes, but the agent returns a JSON
   object like {"response": "...", "success": true}. We now parse that JSON
   and return the inner "response" string as the reply.
2. `client.invoke_agent_runtime` — the correct boto3 method on the
   'bedrock-agentcore' client is `invoke_agent_runtime`. Confirmed correct.
3. Added a fallback: if JSON parsing of the stream fails, return the raw
   text so you can see what the agent actually sent back.
4. sessionId extraction: the key in the response is 'runtimeSessionId',
   which the original code already used correctly — kept as-is.
"""

import json
import os
import traceback
import boto3

REGION = "ap-south-1"
AGENT_ARN = os.environ.get(
    "AGENT_ARN",
    "arn:aws:bedrock-agentcore:ap-south-1:211374268044:runtime/agentcore_agent-tk2fHFEZwU",
)

client = boto3.client("bedrock-agentcore", region_name=REGION)


# ── Main handler ───────────────────────────────────────────────────────────────
def handler(event, context):
    """AgentCore Lambda proxy with CORS support."""

    method = (
        event.get("requestContext", {}).get("http", {}).get("method", "POST").upper()
    )

    # CORS preflight
    if method == "OPTIONS":
        return _cors_response(200, {})

    # Parse body
    try:
        body = json.loads(event.get("body") or "{}")
        message = (body.get("message") or "").strip()
        if not message:
            return _cors_response(400, {"error": "'message' field is required"})
    except json.JSONDecodeError:
        return _cors_response(400, {"error": "Invalid JSON body"})

    print(f"[LAMBDA] Received message: {message}")
    print(f"[LAMBDA] Agent ARN: {AGENT_ARN}")

    try:
        print("[LAMBDA] Invoking AgentCore...")
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_ARN,
            payload=json.dumps({"prompt": message}),
        )

        reply_text = _extract_reply(response)
        session_id = response.get("runtimeSessionId", "unknown")

        print(f"[LAMBDA] Reply ({len(reply_text)} chars): {reply_text[:120]}")

        return _cors_response(
            200,
            {
                "reply": reply_text,
                "message": message,
                "success": True,
                "sessionId": session_id,
            },
        )

    except Exception as e:
        traceback.print_exc()
        return _cors_response(
            500,
            {
                "error": "Agent invocation failed",
                "detail": str(e)[:300],
                "success": False,
            },
        )


# ── Response extraction ────────────────────────────────────────────────────────
def _extract_reply(response: dict) -> str:
    """
    AgentCore returns a streaming body under response["response"].
    The agent handler returns JSON: {"response": "...", "success": true}.
    We read the stream, parse the JSON, and return the inner "response" string.
    """
    print(f"[EXTRACT] Top-level response keys: {list(response.keys())}")

    raw_body = response.get("response")
    if raw_body is None:
        print("[EXTRACT] No 'response' key found")
        return "Error: empty response from agent"

    # Read streaming body
    if hasattr(raw_body, "read"):
        try:
            raw_bytes = raw_body.read()
            raw_text = raw_bytes.decode("utf-8", errors="replace").strip()
            print(f"[EXTRACT] Raw stream ({len(raw_text)} chars): {raw_text[:200]}")
        except Exception as e:
            print(f"[EXTRACT] Stream read error: {e}")
            return f"Error reading agent stream: {e}"
    elif isinstance(raw_body, (bytes, bytearray)):
        raw_text = raw_body.decode("utf-8", errors="replace").strip()
    elif isinstance(raw_body, str):
        raw_text = raw_body.strip()
    else:
        print(f"[EXTRACT] Unexpected response type: {type(raw_body)}")
        return "Error: unexpected response format from agent"

    if not raw_text or raw_text == "null":
        return "No response from agent"

    # The agent returns JSON — parse it and extract the "response" field
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            return parsed.get("response") or str(parsed)
        # Agent returned a plain string encoded as JSON
        return str(parsed)
    except json.JSONDecodeError:
        # Agent returned plain text (not JSON) — return as-is
        print("[EXTRACT] Response is not JSON, returning as plain text")
        return raw_text


# ── CORS helper ────────────────────────────────────────────────────────────────
def _cors_response(status: int, body_dict: dict) -> dict:
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


# ── Local test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_event = {
        "requestContext": {"http": {"method": "POST"}},
        "body": json.dumps({"message": "Turn on HVAC system"}),
    }
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))