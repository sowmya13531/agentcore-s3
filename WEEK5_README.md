# ⚡ VoltStream – Agentic AI Energy Intelligence Platform

> Multi-Agent AI System for Smart Device Control and Energy Optimization using Amazon Bedrock AgentCore, Strands Agents SDK, FastAPI, AWS Lambda, and Amazon Nova.

---

## 📖 Overview

VoltStream is an AI-powered Energy Intelligence Platform that enables users to control smart devices and receive personalized energy-saving recommendations through natural language conversations.

This project demonstrates how Agentic AI systems can be deployed to production using Amazon Bedrock AgentCore. The platform consists of two specialized AI agents:

* **Device Control Agent** – Manages and monitors IoT devices.
* **Energy Advice Agent** – Provides energy insights, trends, and optimization recommendations.

The system leverages the **Strands Agents SDK** for tool orchestration, **Amazon Bedrock Nova** for reasoning, and **Amazon Bedrock AgentCore** for managed deployment, observability, scaling, and session management. 

---

# 🚀 Features

### 🤖 Multi-Agent Architecture

#### Agent 1 – Device Control Agent

* Turn devices ON/OFF
* Check device status
* Handle multi-step device operations
* Uses tool calling through Strands SDK

#### Agent 2 – Energy Advice Agent

* Energy consumption summaries
* Usage trend analysis
* Personalized energy-saving recommendations
* RAG-enabled energy knowledge retrieval

---

### ☁️ AWS Production Deployment

* Amazon Bedrock AgentCore Runtime
* Amazon Bedrock Nova LLM
* AWS Lambda Integration
* Amazon ECR Container Registry
* AWS CodeBuild CI/CD
* CloudWatch Monitoring
* IAM-secured access
* Session tracking per invocation  

---

# 🏗️ Architecture

```text
                        ┌─────────────────────┐
                        │     React Frontend  │
                        └──────────┬──────────┘
                                   │ HTTPS
                                   ▼
                        ┌─────────────────────┐
                        │     FastAPI API     │
                        └──────────┬──────────┘
                                   │
                                   ▼
                   ┌──────────────────────────────┐
                   │      AWS Lambda Proxy        │
                   └──────────────┬───────────────┘
                                  │
                                  ▼
              ┌────────────────────────────────────────┐
              │ Amazon Bedrock AgentCore Runtime       │
              └────────────────────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │     agentcore_app.py    │
                    │      Router Agent       │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┴───────────────────┐
            ▼                                       ▼

 ┌─────────────────────┐               ┌─────────────────────┐
 │ Device Control Agent│               │ Energy Advice Agent │
 └─────────────────────┘               └─────────────────────┘
            │                                       │
            ▼                                       ▼

  get_device_status()                 get_energy_summary()
  toggle_device()                     get_energy_trends()
                                      get_saving_tips()

            │                                       │
            └──────────────┬────────────────────────┘
                           ▼

                  Amazon Bedrock Nova

                           │

                           ▼

                  CloudWatch Logs
                  Session Tracking
                  Observability
```

Based on the Week 5 AgentCore architecture and routing design.  

---

# 🧠 Agent Workflow

```text
User Prompt
     │
     ▼
AgentCore Runtime
     │
     ▼
Routing Entrypoint
(agentcore_app.py)
     │
     ├── Device Request
     │       ▼
     │ Device Agent
     │       ▼
     │ Device Tools
     │
     └── Energy Request
             ▼
        Advice Agent
             ▼
        Energy Tools

             ▼
       Amazon Bedrock

             ▼
        Final Response
```

The system follows the Agentic Loop:

```text
PLAN
  ↓
SELECT TOOL
  ↓
EXECUTE
  ↓
OBSERVE
  ↓
RESPOND
```



---

# 🛠️ Technology Stack

| Layer                | Technology               |
| -------------------- | ------------------------ |
| Frontend             | React.js                 |
| Backend              | FastAPI                  |
| AI Framework         | Strands Agents SDK       |
| LLM                  | Amazon Nova Lite         |
| Runtime              | Amazon Bedrock AgentCore |
| Deployment           | AWS CodeBuild            |
| Container Registry   | Amazon ECR               |
| Monitoring           | CloudWatch               |
| Authentication       | IAM                      |
| Knowledge Base       | ChromaDB                 |
| Programming Language | Python 3.11              |

 

---

# 📂 Project Structure

```text
VoltStream/
│
├── main.py
├── agentcore_app.py
├── requirements.txt
├── .bedrock_agentcore.yaml
│
├── agent/
│   ├── device_agent.py
│   ├── advice_agent.py
│   ├── device_tools.py
│   └── advice_tools.py
│
├── chroma_db/
├── data/
│
├── rag_pipeline.py
├── vector_store.py
├── bedrock_client.py
├── mock_data.py
│
├── frontend/
│
└── README.md
```



---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/sowmya13531/agentcore-s3.git

cd agentcore-s3
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

Or

```bash
pip install \
strands-agents \
strands-agents-tools \
boto3 \
fastapi \
uvicorn \
bedrock-agentcore \
bedrock-agentcore-starter-toolkit
```



---

# 🔐 AWS Prerequisites

* AWS Account
* Bedrock Access Enabled
* IAM Permissions
* AWS CLI Configured
* Python 3.11+
* AgentCore Toolkit Installed

Verify credentials:

```bash
python -c "import boto3; print(boto3.client('sts').get_caller_identity())"
```



---

# ☁️ Deploying to AgentCore

## Configure AgentCore

```bash
agentcore configure
```

Provide:

```text
Entrypoint: agentcore_app.py
Requirements File: requirements.txt
Deployment Type: Container
OAuth: No
Memory: Skip
```



---

## Deploy

```bash
agentcore deploy
```

This automatically:

1. Uploads source to S3
2. Builds ARM64 container via CodeBuild
3. Pushes image to ECR
4. Creates AgentCore Runtime
5. Configures CloudWatch
6. Generates Runtime ARN



---

# 🧪 Testing

## Device Control

```bash
agentcore invoke '{"prompt":"Turn off the Dishwasher"}'
```

```bash
agentcore invoke '{"prompt":"Turn ON device 200"}'
```

```bash
agentcore invoke '{"prompt":"Check status of AC"}'
```

---

## Energy Advice

```bash
agentcore invoke '{"prompt":"Give me energy saving tips","agent":"advice"}'
```

```bash
agentcore invoke '{"prompt":"Show me energy trends","agent":"advice"}'
```

```bash
agentcore invoke '{"prompt":"What is my total energy usage?","agent":"advice"}'
```



---

# 🔍 Monitoring

## Agent Status

```bash
agentcore status
```

## CloudWatch Logs

```bash
aws logs tail /aws/bedrock-agentcore/runtimes/<runtime-id> --follow
```

Monitor:

* Session IDs
* Request IDs
* Tool Selection
* Tool Execution
* Agent Responses
* Runtime Errors



---

# 🎯 Demo Scenarios

### Device Agent

```text
Turn off the Dishwasher
Turn ON device 200
Check status of AC
If device 300 is OFF, turn it ON
```

### Energy Advice Agent

```text
What is my total energy usage?
Show me energy trends
Give me energy saving tips
```



---

# 📊 What AgentCore Adds

| Local Agent         | AgentCore Runtime      |
| ------------------- | ---------------------- |
| Runs on laptop      | Runs 24/7 on AWS       |
| No session tracking | Automatic Session IDs  |
| Local logs          | CloudWatch Logs        |
| No autoscaling      | Managed scaling        |
| Manual monitoring   | Built-in observability |
| No IAM security     | IAM-secured runtime    |



---

# 🧩 Function Call vs Tool Call

### Function Call

Developer decides which function executes.

```python
toggle_device("Dishwasher", "OFF")
```

### Tool Call

LLM decides which tool to execute.

```text
User:
"Turn off the Dishwasher"

↓

LLM selects:
toggle_device()

↓

Strands executes tool
```

**Function Call = Developer Decides**
**Tool Call = LLM Decides**

 

---

# 🚀 Key Achievements

* Production-ready AI deployment on AWS
* Multi-agent architecture
* Intelligent routing system
* Tool-calling AI agents
* AgentCore runtime deployment
* CloudWatch observability
* IAM-secured infrastructure
* RAG-powered energy recommendations
* Automated CI/CD pipeline
* Session-aware agent execution



---



Week 4 & 5 Tasks. AI/ML Intern – Tachyon 2026

