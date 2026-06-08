from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import List
import json
from agent.strands_agent import agent


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

@app.get(
    "/api/v1/devices",
    response_model=List[DeviceResponse]
)
def get_devices():
    return MOCK_DEVICES


@app.patch(
    "/api/v1/devices/{device_id}",
    response_model=DeviceResponse
)
def update_device(
    device_id: str,
    update_data: DeviceUpdate
):
    for device in MOCK_DEVICES:
        if device.id == device_id:
            device.is_on = update_data.is_on
            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
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
# Agent API (Mock)
# -----------------------------------

@app.post(
    "/api/v1/agent",
    response_model=ChatResponse
)
def agent_endpoint(
    request: ChatRequest
):
    try:

        result = agent(
            request.message
        )

        return ChatResponse(
            reply=str(result)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
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