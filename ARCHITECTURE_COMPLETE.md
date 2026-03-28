# Autonomous Ops Architecture - Complete Stack

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  • React Dashboard (optional)                                   │
│  • HTML/JS web interface (index.html)                           │
│  • Real-time ticket submission & status                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  API ORCHESTRATION (FastAPI)                    │
├─────────────────────────────────────────────────────────────────┤
│  • POST /ticket - Receive & queue tickets                       │
│  • GET /status/{ticket_id} - Check processing status            │
│  • GET /memory/search - Query knowledge base                    │
│  • WebSocket /ws - Real-time updates                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
┌────────────────────────┐  ┌──────────────────┐
│   QUEUE SYSTEM         │  │  AGENT LAYER     │
│   (Redis)              │  │  (LangGraph)     │
├────────────────────────┤  ├──────────────────┤
│ • Priority queuing     │  │ Workflow:        │
│ • Async processing     │  │ 1. Parse ticket  │
│ • Retry logic          │  │ 2. Query memory  │
│ • Rate limiting        │  │ 3. LLM inference │
└────────────────────────┘  │ 4. Decision      │
                            │ 5. Execute tools │
                            └────────┬─────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
            ┌──────────────────────┐        ┌────────────────┐
            │   LOCAL LLM LAYER    │        │ TOOL EXECUTION │
            │   (Ollama)           │        │     ENGINE     │
            ├──────────────────────┤        ├────────────────┤
            │ Models:              │        │ • send_alert   │
            │ • Llama3 (8B)        │        │ • create_ticket│
            │ • Mistral (7B)       │        │ • assign_team  │
            │ • Neural Chat        │        │ • update_kb    │
            │                      │        │ • webhook call │
            │ GPU Optimized        │        │ • slack notify │
            │ (Docker/local)       │        │ • github issue │
            └──────────────────────┘        └────────┬───────┘
                                                     │
                    ┌────────────────────────────────┘
                    ▼
        ┌────────────────────────────┐
        │  MEMORY & LEARNING LAYER   │
        ├────────────────────────────┤
        │  PostgreSQL (Primary):     │
        │  • tickets table           │
        │  • actions_log table       │
        │  • Full-text search        │
        │                            │
        │  ChromaDB (Vector Search): │
        │  • Ticket embeddings       │
        │  • Semantic similarity     │
        │  • Knowledge base search   │
        │                            │
        │  JSON (Fallback):          │
        │  • Auto-fallback ready     │
        │  • Local file storage      │
        └────────────────────────────┘
```

## Component Details

### 1. FastAPI Server (main.py)

```python
# Framework: FastAPI 0.104.1
# ASGI Server: Uvicorn 0.24.0
# Purpose: Central API orchestration

Key Endpoints:
  POST /ticket
    - Receives ticket JSON
    - Queues to Redis
    - Returns ticket_id immediately
    - Async processing begins

  GET /status/{ticket_id}
    - Polls processing status
    - Returns decision & actions
    - Real-time progress updates

  WebSocket /ws
    - Push updates to client
    - Live classification stream
    - Action notifications
```

### 2. Agent Orchestration (LangGraph)

```python
# Framework: LangGraph + LangChain
# Purpose: Agent workflow control

Workflow State Machine:
  1. RECEIVE → Parse ticket, validate data
  2. SEARCH → Query PostgreSQL & ChromaDB for similar tickets
  3. REASON → Call Ollama for LLM classification
  4. DECIDE → Determine actions based on confidence
  5. EXECUTE → Run tool actions (alerts, tickets, webhooks)
  6. MEMORY → Store results in PostgreSQL + ChromaDB
  7. NOTIFY → Send updates (Slack, GitHub, webhooks)

Error Handling:
  - Automatic retry on failure
  - Fallback to mock classification
  - Circuit breaker for external APIs
```

### 3. Local LLM Inference (Ollama)

```yaml
Ollama Configuration:
  - URL: http://localhost:11434 (default)
  - Deployment: Docker container

Model Selection:
  Llama3 (Recommended):
    - Size: 8B parameters
    - Speed: ~2-5 sec/response
    - Reasoning: Excellent
    - Context: 8K tokens
    - VRAM: 6-8GB

  Mistral:
    - Size: 7B parameters
    - Speed: ~1-3 sec/response
    - JSON Output: Optimized
    - Context: 8K tokens
    - VRAM: 4-6GB

  Neural Chat:
    - Size: 7B parameters
    - Speed: ~1-3 sec/response
    - Dialogue: Optimized
    - Context: 8K tokens
    - VRAM: 4-6GB

Deployment Options:
  1. Docker: docker run -p 11434:11434 ollama/ollama
  2. Local: Download from ollama.ai
  3. Remote: Cloud instance (AWS, GCP, Azure)
```

### 4. Tool Execution Engine (tools.py)

```python
# Class: ExecutionEngine
# Purpose: Autonomous action execution

Available Tools:
  1. send_alert()
     - Slack integration
     - Email notifications
     - PagerDuty escalation

  2. create_jira_ticket()
     - Create issue
     - Set priority
     - Add watchers

  3. assign_ticket()
     - Determine team owner
     - Auto-assign to on-call
     - Send notification

  4. store_knowledge_base()
     - Add to ChromaDB
     - Generate embeddings
     - Enable future searches

  5. webhook_integration()
     - HTTP POST to custom endpoints
     - GitHub webhooks
     - Slack notifications
     - Custom APIs

Tool Logging:
  - Every action logged with timestamp
  - Execution result stored
  - Audit trail in database
```

### 5. Memory System (memory.py)

```yaml
Storage Architecture:

PostgreSQL (Primary):
  Tables:
    - tickets
      * ticket_id (UUID)
      * issue (text)
      * priority (enum)
      * category (enum)
      * team (text)
      * confidence (float 0-1)
      * decision (JSONB)
      * created_at (timestamp)
      * updated_at (timestamp)

    - actions_log
      * action_id (UUID)
      * ticket_id (FK)
      * action_type (text)
      * result (JSONB)
      * executed_at (timestamp)

  Indexes:
    - Full-text search on issue
    - Timestamp for analytics
    - Priority/category for filtering

ChromaDB (Vector Memory):
  - Embeddings model: sentence-transformers
  - Store: Ticket embeddings
  - Purpose: Semantic similarity search
  - Use case: "Find similar past issues"

JSON Fallback:
  - File: tickets.json
  - Auto-activate if PostgreSQL unavailable
  - Preserves all functionality
  - Automatic upgrade when DB available
```

### 6. Queue System (Redis)

```yaml
Purpose: Async task processing

Queue Structure:
  - Priority queues: critical, high, normal, low
  - Worker pool: Process tickets in parallel
  - Retry logic: Failed tasks requeue with backoff
  - Rate limiting: Prevent API throttling

Use Cases:
  - Queue incoming tickets
  - Background LLM inference
  - Batch webhooks
  - Memory synchronization
```

### 7. Integrations

#### GitHub Integration

```python
# PyGithub library
# Actions:
# - Create issues
# - Add labels
# - Post comments
# - Request reviews
```

#### Slack Integration

```python
# slack-sdk library
# Actions:
# - Send alerts
# - Post decisions
# - Thread replies
# - Interactive buttons
```

#### SMTP/Email

```python
# Built-in smtplib
# Actions:
# - Send alerts
# - Escalations
# - Daily reports
```

#### Webhooks

```python
# Generic HTTP POST integration
# Actions:
# - Call external APIs
# - Custom business logic
# - Third-party systems
```

## Data Flow Example

```
REQUEST:
  Ticket: "Production API returning 500 errors"
    ↓
FASTAPI:
  - Validate JSON
  - Assign ticket_id: uuid-1234
  - Queue to Redis
  - Response: {ticket_id, status: "queued"}
    ↓
QUEUE (Redis):
  - Priority: HIGH (contains "500")
  - Move to high-priority worker
    ↓
AGENT (LangGraph):
  1. PARSE: Extract issue text
  2. SEARCH: Query similar issues
     - PostgreSQL: Find related incidents
     - ChromaDB: Find semantically similar
  3. REASON: Call Ollama
     - Prompt: "Classify this ticket..."
     - Model: llama3
     - Response: {category: "Incident", priority: "Critical", team: "Backend"}
  4. DECIDE: Confidence > 0.8? Execute actions
  5. EXECUTE: Tools
     - send_alert → Slack channel
     - create_jira_ticket → Backend project
     - assign_ticket → On-call engineer
     - store_knowledge_base → ChromaDB
  6. MEMORY: Store decision in PostgreSQL
  7. NOTIFY: Send update to WebSocket
    ↓
FRONTEND:
  - Real-time update: Classification complete
  - Alert sent to Backend team
  - Jira ticket created
  - On-call paged
```

## Deployment Options

### Option 1: Local Development

```bash
# All components on laptop
ollama pull llama3
docker run -d -p 5432:5432 postgres:15
docker run -d -p 6379:6379 redis:7
python run_server.py
```

### Option 2: Docker Compose

```yaml
services:
  api:
    image: autonomous-ops-demo
  ollama:
    image: ollama/ollama
  postgres:
    image: postgres:15
  redis:
    image: redis:7
  chromadb:
    image: chromadb/chromadb
```

### Option 3: Cloud Deployment

```
AWS/GCP/Azure:
  - FastAPI on Cloud Run / Lambda
  - Ollama on EC2 / Compute Engine
  - RDS for PostgreSQL
  - ElastiCache for Redis
  - Environment variables for config
```

## Performance Metrics

| Component            | Latency  | Throughput | Cost         |
| -------------------- | -------- | ---------- | ------------ |
| FastAPI              | <10ms    | 1000 req/s | Free         |
| Ollama (Llama3)      | 2-5s     | 1 req/s    | $0/mo        |
| PostgreSQL Query     | <50ms    | Variable   | $0-30/mo     |
| ChromaDB Search      | <200ms   | 100 req/s  | Free         |
| Redis Queue          | <5ms     | 10k req/s  | $0-15/mo     |
| **Total End-to-End** | **3-6s** | Per queue  | **$0-50/mo** |

## Tech Stack Summary

| Layer      | Technology            | Version | Purpose            |
| ---------- | --------------------- | ------- | ------------------ |
| API        | FastAPI               | 0.104.1 | REST orchestration |
| Server     | Uvicorn               | 0.24.0  | ASGI application   |
| Agent      | LangGraph             | 0.2.0   | Workflow control   |
| Chain      | LangChain             | 0.1.0   | Agent components   |
| LLM        | Ollama                | 0.1.24  | Local inference    |
| Models     | Llama3/Mistral        | Latest  | AI reasoning       |
| Embeddings | Sentence-Transformers | 2.2.2   | Vector DB          |
| Vector DB  | ChromaDB              | 0.4.14  | Semantic search    |
| SQL DB     | PostgreSQL            | 15      | Persistent store   |
| Driver     | psycopg2              | 2.9.9   | DB connection      |
| Queue      | Redis                 | 5.0.1   | Async tasks        |
| GitHub     | PyGithub              | 2.1.1   | Issue/PR ops       |
| Slack      | slack-sdk             | 3.23.0  | Notifications      |
| HTTP       | requests              | 2.31.0  | API calls          |
| Validation | Pydantic              | 2.5.0   | Data validation    |
| Config     | python-dotenv         | 1.0.0   | Environment        |

## Next Steps

1. **Setup Ollama**: `docker run -d -p 11434:11434 ollama/ollama`
2. **Pull Model**: `docker exec ollama ollama pull llama3`
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Configure PostgreSQL**: `python setup_postgres.py` (optional)
5. **Start Server**: `python run_server.py`
6. **Test System**: `python test_api.py`

See `OLLAMA_SETUP.md` for detailed setup instructions.
