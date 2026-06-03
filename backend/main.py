from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import List
import json

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
    ChatResponse,
    QARequest
)

from mock_data import (
    MOCK_DASHBOARD_LIVE,
    MOCK_ANALYTICS_HISTORY,
    MOCK_DEVICES,
    MOCK_BILLING_SUMMARY
)

app = FastAPI(
    title="VoltStream API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup index
@app.on_event("startup")
def startup_event():
    try:
        build_index()
    except Exception as e:
        print("Index error:", e)

@app.get("/")
def root():
    return {"message": "VoltStream running"}

# ---------------- DASHBOARD ----------------
@app.get("/api/v1/dashboard/live", response_model=LivePowerStatus)
def get_live_dashboard():
    return MOCK_DASHBOARD_LIVE

# ---------------- CHAT ----------------
@app.post("/api/v1/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    prompt = request.message

    body = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": request.message}]
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

        result = json.loads(response["body"].read())

        reply = (
            result.get("output", {})
            .get("message", {})
            .get("content", [{}])[0]
            .get("text", "No response")
        )

        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- QA (RAG) ----------------
@app.post("/api/v1/qa", response_model=ChatResponse)
def qa_endpoint(request: QARequest):

    question = request.question

    try:
        chunks = retrieve_chunks(question)

        if not chunks:
            return ChatResponse(reply="I don't have that information")

        context = "\n".join(chunks[:3])

        prompt = f"""
You are an AI assistant for energy domain.

RULES:
- Use ONLY context
- If not found, say EXACTLY:
I don't have that information

Context:
{context}

Question:
{question}
"""

        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
        }

        response = bedrock.invoke_model(
            modelId="global.amazon.nova-2-lite-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())

        answer = (
            result.get("output", {})
            .get("message", {})
            .get("content", [{}])[0]
            .get("text", "No response")
        )

        return ChatResponse(reply=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


handler = Mangum(app)