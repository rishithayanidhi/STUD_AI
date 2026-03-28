# Autonomous Ops Demo

Demo-level autonomous workflow: Ticket → AI decision → Tool execution → Memory → Response

## Quick Start (JSON Default)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the API
python run_server.py

# 3. Open browser
http://localhost:8000
```

## Optional: PostgreSQL Backend

Want to impress judges with enterprise architecture?

```bash
# Quick setup with Docker (2 minutes)
python quick_postgres.py

# Then restart API - it'll auto-detect PostgreSQL
python run_server.py

# Verify with:
curl http://localhost:8000/stats | jq
```

See [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for full guide.

## Files

| File               | Purpose                     |
| ------------------ | --------------------------- |
| `main.py`          | FastAPI server              |
| `agent.py`         | AI reasoning agent (OpenAI) |
| `tools.py`         | Tool execution engine       |
| `memory.py`        | PostgreSQL + JSON storage   |
| `index.html`       | Beautiful UI                |
| `requirements.txt` | Python dependencies         |

## Storage Options

| Storage        | Setup          | Enterprise | Status       |
| -------------- | -------------- | ---------- | ------------ |
| **JSON**       | None           | ✓          | ✅ Ready now |
| **PostgreSQL** | Docker/Install | ✓✓✓        | ✅ Optional  |
| **Firebase**   | Cloud          | ✓✓         | Coming soon  |

## Expected Output

```json
{
  "issue": "Production API failing with 500 error affecting payments",
  "classification": {
    "category": "Incident",
    "priority": "High",
    "team": "Backend",
    "suggested_action": "Page on-call engineer and create incident ticket"
  },
  "actions_executed": [
    "Alert sent: HIGH PRIORITY",
    "Assigned to Backend Team",
    "Stored in knowledge base"
  ]
}
```

## Demo Narrative

See `agent.md` for full judge delivery script.
