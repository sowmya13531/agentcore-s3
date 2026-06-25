# ⚡ VoltStream – Agentic AI Device Control System

> An Agentic AI-powered Smart Device Control Platform built using AWS Bedrock, Strands Agents SDK, FastAPI, and Natural Language Tool Calling.

---

## 📖 Overview

VoltStream Week 4 introduces Agentic AI capabilities by enabling users to control smart devices through natural language commands.

Instead of hardcoded application logic, the system uses a Large Language Model (LLM) to reason about user intent and autonomously decide which tool to invoke. The platform demonstrates real-world Agentic AI concepts such as:

* Natural Language Device Control
* LLM-Driven Tool Selection
* Multi-Step Agentic Reasoning
* Stateful Device Simulation
* REST API Integration
* FastAPI Backend Services
* Browser-Based Device Control UI

The solution is powered by:

* AWS Bedrock
* Strands Agents SDK
* FastAPI
* Python Tool Calling
* Amazon Qwen Model Integration

This project serves as a foundation for production-grade AI agents that can reason, plan, and take actions using tools. 

---

# 🚀 Features

## 🤖 Agentic AI Device Control

Users interact using plain English commands:

```text
Turn ON device 200
Turn off the Dishwasher
Check status of device 300
```

The AI automatically:

1. Understands user intent
2. Selects the correct tool
3. Executes the action
4. Returns a natural language response

No hardcoded command routing is required. 

---

## 🔧 Tool Calling with Strands

The system exposes Python functions as tools using the `@tool` decorator.

### Available Tools

#### Status Tool

Checks current device status.

```python
status(device_id)
```

Returns:

```text
ON
OFF
```

#### Toggle Device Tool

Turns devices ON or OFF.

```python
toggle_device(device_id, state)
```

Returns:

```text
Device 200 turned ON
```



---

## 🧠 Multi-Step Agentic Reasoning

The agent can perform conditional reasoning.

Example:

```text
If device 300 is OFF, turn it ON
```

Execution Flow:

```text
Tool 1 → status(300)

Result → OFF

Tool 2 → toggle_device(300, ON)

Final Response:
Device 300 was OFF. I have turned it ON.
```

The LLM evaluates intermediate tool results before deciding the next action. 

---

## 💾 Stateful Device Simulation

Device states are maintained in memory:

```python
device_state = {
    "200": "ON",
    "Dishwasher": "OFF"
}
```

The state persists throughout the server session and updates after every tool execution. 

---

## 🌐 Browser-Based Interface

A lightweight HTML frontend provides:

* Natural language query input
* Device state visualization
* Real-time refresh
* API integration using Fetch API

Users can interact with the agent without needing Swagger or curl commands. 

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Browser UI     │
                    │    frontend.html    │
                    └──────────┬──────────┘
                               │
                               ▼

                  POST /api/v1/agent
                  GET  /api/v1/devices

                               │

                               ▼

                    ┌─────────────────────┐
                    │       FastAPI       │
                    │      Backend API    │
                    └──────────┬──────────┘
                               │
                               ▼

                    ┌─────────────────────┐
                    │    Strands Agent    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼

            status() Tool        toggle_device() Tool

                    │                     │
                    └──────────┬──────────┘
                               ▼

                     AWS Bedrock LLM
                 qwen.qwen3-coder-next

                               │
                               ▼

                       Natural Language
                           Response
```

Based on the Week 4 Agentic AI architecture. 

---

# 🧠 How Agentic AI Works

Traditional applications use hardcoded function calls.

```python
toggle_device("200", "ON")
```

Agentic AI works differently.

User Input:

```text
Turn ON device 200
```

Agent Workflow:

```text
User Query
     │
     ▼

FastAPI Endpoint

     ▼

Strands Agent

     ▼

LLM Reasoning

     ▼

Tool Selection

     ▼

Tool Execution

     ▼

Tool Result

     ▼

Natural Language Response
```

The LLM decides which tool should execute at runtime. 

---

# ⚙️ Technology Stack

## Backend

* FastAPI
* Uvicorn
* Python

## Agent Framework

* Strands Agents SDK
* Strands Tools

## AI Services

* AWS Bedrock
* Amazon Nova 2 Lite

## Frontend

* HTML
* CSS
* JavaScript

## Cloud Services

* AWS IAM
* AWS CLI

 

---

# 📂 Project Structure

```text
voltstream-agent/
│
├── main.py
├── requirements.txt
├── .gitignore
│
├── frontend/
│   └── index.html
│
└── README.md
```



---

# 🔌 API Endpoints

## POST /api/v1/agent

Natural language interface for device control.

### Example Request

```http
POST /api/v1/agent?query=Turn ON device 200
```

### Example Response

```json
{
  "response": "Device 200 turned ON"
}
```

---

## GET /api/v1/devices

Returns all device states.

### Example Response

```json
{
  "devices": {
    "200": "ON",
    "Dishwasher": "OFF"
  },
  "total": 2
}
```



---

# 🛠️ Installation

## Clone Repository

```bash
git clone https://github.com/sowmya13531/voltstream-agent.git

cd voltstream-agent
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

```txt
fastapi
uvicorn
strands-agents
strands-agents-tools
python-dotenv
```



---

# 🔐 AWS Configuration

Configure AWS credentials:

```bash
aws configure
```

Verify access:

```bash
aws sts get-caller-identity
```

Ensure access to:

* AWS Bedrock
* Bedrock Runtime
* Foundation Models



---

# ▶️ Run the Application

Start FastAPI:

```bash
uvicorn main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```



---

# 🧪 Testing

## Turn ON Device

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/agent?query=Turn%20ON%20device%20200"
```

Expected:

```json
{
  "response": "Device 200 turned ON"
}
```

---

## Check Device Status

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/agent?query=Check%20status%20of%20device%20200"
```

---

## Turn Off Dishwasher

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/agent?query=Turn%20off%20the%20Dishwasher"
```

---

## Conditional Command

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/agent?query=If%20device%20300%20is%20OFF%20turn%20it%20ON"
```

This triggers two tool calls:

```text
status()

toggle_device()
```

 

---

# 🎯 Demo Queries

```text
Turn ON device 200
Turn off the Dishwasher
Check status of device 200
What is the state of device 300?
If device 300 is OFF, turn it ON
Turn ON device 100 and device 200
```

Expected behaviors:

* Single tool execution
* Multi-tool reasoning
* State updates
* Natural language responses



---

# 🔍 Execution Trace Example

When the user sends:

```text
Turn ON device 200
```

Terminal Output:

```text
Tool #1: toggle_device

Input:
device_id='200'
state='ON'

Output:
Device 200 turned ON
```

This trace shows the exact tool selected and executed by the agent. 

---

# 🚨 Error Handling

Implemented protections for:

* Invalid AWS credentials
* Missing Bedrock access
* Unsupported models
* Agent invocation errors
* Streaming issues
* CORS failures

Recommended implementation:

```python
try:
    response = agent(query)
    return {"response": str(response)}
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Agent error: {str(e)}"
    )
```

 

---

# ⚠️ Current Limitations

| Limitation               | Future Improvement      |
| ------------------------ | ----------------------- |
| In-memory device storage | DynamoDB persistence    |
| No authentication        | JWT/API Key security    |
| Virtual devices only     | Real IoT integration    |
| No conversation history  | Session memory          |
| No streaming responses   | Async streaming         |
| Single-user state        | Multi-user architecture |



---

# 🔒 Security Best Practices

* Never commit AWS credentials
* Never commit `.env`
* Restrict CORS origins in production
* Add API rate limiting
* Validate query length
* Log agent requests for auditing

Recommended `.gitignore`:

```gitignore
__pycache__/
*.pyc
venv/
.venv/

.env
*.env

.aws/
.vscode/
.idea/
```

 

---

# 📈 Key Learnings

* Agentic AI Fundamentals
* Tool Calling with Strands
* AWS Bedrock Integration
* FastAPI REST APIs
* Multi-Step Agent Reasoning
* Stateful AI Systems
* Natural Language Interfaces
* LLM-Orchestrated Actions
* Execution Tracing
* Production AI Patterns



---



Tachyon AIML Internship 2026 – Week 4
Agentic AI & AWS Bedrock Track

