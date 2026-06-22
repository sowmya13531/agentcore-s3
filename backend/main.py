from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import List, Optional
from pydantic import BaseModel
import json
import time
from datetime import datetime
from services.agentcore_client import invoke_agentcore
from agent.strands_agent import agent
from device_db import DEVICES_DB
from device_store import save_devices

from rag.vector_store import collection
from bedrock_client import bedrock
from rag.rag_pipeline import build_index, retrieve_chunks

from models import (
    LivePowerStatus,
    EnergyDataPoint,
    DeviceResponse,
    DeviceUpdate,
    BillingSummary,
    ChatRequest,
    ChatResponse
)

from mock_data import (
    MOCK_DASHBOARD_LIVE,
    MOCK_ANALYTICS_HISTORY,
    MOCK_DEVICES,
    MOCK_BILLING_SUMMARY
)

# -----------------------------------
# Response Models
# -----------------------------------

class AgentResponse(BaseModel):
    """Agent response with metadata"""
    reply: str
    message: str
    success: bool
    session_id: str
    execution_time_ms: float
    timestamp: str


# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI(
    title="VoltStream API",
    version="1.0.0",
    description="Backend API for VoltStream Smart Energy Platform"
)

# -----------------------------------
# Build RAG Index at Startup
# -----------------------------------

@app.on_event("startup")
def startup_event():
    try:
        build_index()
    except Exception as e:
        print("Index build failed:", str(e))

# -----------------------------------
# CORS Configuration
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Root Route
# -----------------------------------

@app.get("/")
def root():
    return {
        "message": "VoltStream API is running successfully"
    }

# -----------------------------------
# Dashboard APIs
# -----------------------------------

@app.get(
    "/api/v1/dashboard/live",
    response_model=LivePowerStatus
)
def get_live_dashboard():
    return MOCK_DASHBOARD_LIVE

# -----------------------------------
# Analytics APIs
# -----------------------------------

@app.get(
    "/api/v1/analytics/history",
    response_model=List[EnergyDataPoint]
)
def get_analytics_history(
    period: str = Query(
        default="daily",
        pattern="^(daily|weekly|monthly)$"
    )
):
    if period in MOCK_ANALYTICS_HISTORY:
        return MOCK_ANALYTICS_HISTORY[period]

    raise HTTPException(
        status_code=400,
        detail="Invalid period"
    )

# -----------------------------------
# Device APIs
# -----------------------------------

@app.get("/api/v1/devices")
def get_devices():

    return [
        DeviceResponse(
            id=device["id"],
            name=device["name"],
            type=device["type"],
            power_draw_w=device["power_draw_w"],
            is_on=device["is_on"]
        )
        for device in DEVICES_DB.values()
    ]


@app.patch("/api/v1/devices/{device_id}")
def update_device(
    device_id: str,
    update_data: DeviceUpdate
):

    if device_id not in DEVICES_DB:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    
    DEVICES_DB[device_id]["is_on"] = update_data.is_on

    save_devices(DEVICES_DB)

    device = DEVICES_DB[device_id]

    return DeviceResponse(
        id=device["id"],
        name=device["name"],
        type=device["type"],
        power_draw_w=device["power_draw_w"],
        is_on=device["is_on"]
    )

# -----------------------------------
# Billing APIs
# -----------------------------------

@app.get(
    "/api/v1/billing/summary",
    response_model=BillingSummary
)
def get_billing_summary():
    return MOCK_BILLING_SUMMARY

# -----------------------------------
# CHAT API (Bedrock)
# -----------------------------------

@app.post(
    "/api/v1/chat",
    response_model=ChatResponse
)
def chat_endpoint(request: ChatRequest):

    prompt = f"""
You are VoltStream AI Copilot.

You help users with:
- Energy consumption
- Electricity
- Solar energy
- Smart devices
- Billing
- Energy savings

Answer clearly and professionally.

User Question:
{request.message}
"""

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:

        response = bedrock.invoke_model(
            modelId="global.amazon.nova-2-lite-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(
            response["body"].read()
        )

        reply = (
            result.get("output", {})
            .get("message", {})
            .get("content", [{}])[0]
            .get("text", "No response")
        )

        return ChatResponse(
            reply=reply
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# QA API (RAG)
# -----------------------------------

@app.post(
    "/api/v1/qa",
    response_model=ChatResponse
)
def qa_endpoint(request: ChatRequest):

    question = request.message

    try:

        chunks = retrieve_chunks(question)

        if not chunks:
            return ChatResponse(
                reply="I don't have that information"
            )

        context = "\n".join(chunks[:3])

        prompt = f"""
You are an AI assistant for the energy domain.

RULES:
- Use ONLY the context below
- If answer is not in context, respond EXACTLY:
"I don't have that information"
- Do NOT explain anything
- Do NOT mention context

Context:
{context}

Question:
{question}
"""

        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = bedrock.invoke_model(
            modelId="global.amazon.nova-2-lite-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(
            response["body"].read()
        )

        answer = (
            result.get("output", {})
            .get("message", {})
            .get("content", [{}])[0]
            .get("text", "No response")
        )

        return ChatResponse(
            reply=answer
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# Agent API (with Metadata)
# -----------------------------------
@app.post(
    "/api/v1/agent",
    response_model=AgentResponse
)
def agent_endpoint(request: ChatRequest):
    """
    Invoke AI Agent via Lambda → AgentCore
    Returns response with metadata (session_id, execution time, etc.)
    """

    start_time = time.time()

    try:
        # Call Lambda → AgentCore
        result = invoke_agentcore(request.message)

        print("\n=== AGENT RESULT ===")
        print(result)
        print("====================\n")

        reply = result.get(
            "reply",
            "No response received"
        )

        # Extract session id from Lambda response
        session_id = (
            result.get("sessionId")
            or result.get("runtimeSessionId")
            or result.get("session_id")
            or "unknown"
        )

        # Handle JSON reply if agent returns JSON string
        try:
            parsed = json.loads(reply)

            if isinstance(parsed, dict):
                reply = (
                    parsed.get("response")
                    or parsed.get("reply")
                    or reply
                )

        except Exception:
            pass

        execution_time_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        return AgentResponse(
            reply=reply,
            message=request.message,
            success=result.get("success", True),
            session_id=session_id,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:

        execution_time_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={
                "X-Execution-Time": str(execution_time_ms)
            }
        )

# -----------------------------------
# Local Development Server
# -----------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

# -----------------------------------
# AWS Lambda Handler
# -----------------------------------

handler = Mangum(app)