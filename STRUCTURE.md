# Autonomous Ops Demo - Project Root

## 📁 Directory Structure

All project files are now directly in the STUAI folder:

```
STUAI/
├── .venv/                          # Python virtual environment
├── .vscode/                        # VS Code configuration
│   └── settings.json              # Workspace settings
├── .github/                        # GitHub workflows
├── STUAI.code-workspace           # Workspace file (open this in VS Code)
│
├── Core Application Files
├── agent.py                        # Ollama LLM integration
├── main.py                         # FastAPI server
├── tools.py                        # Tool execution engine
├── memory.py                       # PostgreSQL + JSON storage
├── index.html                      # Web UI
├── run_server.py                   # Server launcher
│
├── Configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
│
├── Testing
├── test_api.py                     # API endpoint tests
├── test_demo.py                    # End-to-end tests
├── test_ollama.py                  # Ollama integration test
├── test_stats.py                   # Stats tests
│
├── Automation & Setup
├── quick_start.py                  # Quick setup script
├── quick_postgres.py               # PostgreSQL setup
├── setup_postgres.py               # Detailed DB setup
├── SUMMARY.py                      # Status display
├── DEMO_SCRIPT.py                  # Demo walkthrough
├── DEMO_CHECKLIST.py               # Pre-demo checklist
│
├── Documentation
├── README.md                       # Main README
├── OLLAMA_SETUP.md                 # Ollama installation
├── MIGRATION_OPENAI_TO_OLLAMA.md   # Migration guide
├── ARCHITECTURE_COMPLETE.md        # Full architecture
├── POSTGRES_COMPLETE.md            # PostgreSQL guide
├── POSTGRES_INTEGRATION_SUMMARY.md # DB integration
├── POSTGRESQL_SETUP.md             # DB setup steps
├── CHANGES.md                      # Change log
├── FILE_MANIFEST.md                # File descriptions
├── READY_FOR_JUDGES.md             # Judge presentation guide
│
├── Data Files
├── tickets.json                    # Local memory storage
└── __pycache__/                    # Python cache
```

## 🚀 Quick Start

1. **Open Workspace**: Open `STUAI.code-workspace` in VS Code
2. **Activate Environment**: 
   ```bash
   .venv\Scripts\Activate
   ```
3. **Install Ollama** (first time):
   ```bash
   python quick_start.py
   ```
4. **Start Server**:
   ```bash
   python run_server.py
   ```
5. **Access Demo**: Open http://localhost:8000

## 📋 Setup Instructions

### Option A: Full Auto Setup
```bash
python quick_start.py
```
This will:
- Start Ollama with Docker
- Pull Llama3 model
- Install Python dependencies
- Run tests

### Option B: Manual Setup

1. **Ollama** (required):
   ```bash
   docker run -d -p 11434:11434 ollama/ollama
   docker exec ollama ollama pull llama3
   ```

2. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration** (optional):
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

4. **PostgreSQL** (optional, for production):
   ```bash
   python setup_postgres.py
   # OR: python quick_postgres.py (3-min setup)
   ```

## 🧪 Testing

```bash
# Test Ollama integration
python test_ollama.py

# Test API endpoints
python test_api.py

# Full end-to-end test
python test_demo.py

# Check backend status
python test_stats.py
```

## 🎯 Demo Preparation

```bash
# Pre-demo checklist
python DEMO_CHECKLIST.py

# Run demo script
python DEMO_SCRIPT.py

# See judge presentation steps
cat READY_FOR_JUDGES.md
```

## 📖 Documentation

- **Starting Out**: `README.md` → `OLLAMA_SETUP.md` → `quick_start.py`
- **Understanding Stack**: `ARCHITECTURE_COMPLETE.md`
- **From OpenAI?**: `MIGRATION_OPENAI_TO_OLLAMA.md`
- **PostgreSQL Setup**: `POSTGRES_COMPLETE.md`
- **Demo Guide**: `READY_FOR_JUDGES.md`
- **File Reference**: `FILE_MANIFEST.md`

## ⚙️ Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit as needed:
```env
# Ollama configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost:5432/autonomous_ops

# API Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🔧 Development

### VS Code Setup
- Open `STUAI.code-workspace` for proper configuration
- Python interpreter: `.venv/Scripts/python.exe` (auto-configured)
- Debugging: Use launch configs in `.vscode/launch.json`

### Running Tests
```bash
# From terminal
python test_api.py

# Or in VS Code
# Press F5 → Select "Test API"
```

### Adding Features
1. Edit relevant file (agent.py, tools.py, etc.)
2. Run tests: `python test_api.py`
3. Check status: `python SUMMARY.py`

## 📊 Architecture Overview

```
Browser
  ↓
FastAPI (main.py:8000)
  ├→ Agent (agent.py + Ollama)
  ├→ Tools (tools.py)
  ├→ Memory (memory.py + PostgreSQL)
  └→ UI (index.html)
```

## 🚢 Deployment

### Local Development
```bash
python run_server.py
# Access: http://localhost:8000
```

### With Docker (Production)
```bash
docker build -t autonomous-ops .
docker run -p 8000:8000 -p 11434:11434 autonomous-ops
```

### Cloud Deployment
See `READY_FOR_JUDGES.md` for cloud deployment options.

## 📞 Troubleshooting

**Ollama not responding?**
```bash
docker logs ollama
docker restart ollama
```

**Python import errors?**
```bash
pip install -r requirements.txt
```

**Database connection failed?**
```bash
# Falls back to JSON automatically
# Or setup DB: python setup_postgres.py
```

## 📝 Key Files

| File | Purpose |
|------|---------|
| `agent.py` | Ollama LLM reasoning |
| `main.py` | FastAPI orchestration |
| `tools.py` | Autonomous action execution |
| `memory.py` | Persistent storage + learning |
| `index.html` | Web interface |
| `requirements.txt` | Python dependencies |
| `STUAI.code-workspace` | VS Code workspace (open this!) |

## ✅ Status

- ✅ Ollama integration complete
- ✅ Local LLM inference working
- ✅ PostgreSQL support (optional)
- ✅ Full documentation
- ✅ Test suite ready
- ✅ Demo scripts prepared
- ✅ Judge presentation ready

## 🎓 Learning Resources

- [Ollama Documentation](https://ollama.ai)
- [FastAPI Tutorial](https://fastapi.tiangolo.com)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [PostgreSQL Guide](https://www.postgresql.org/docs/)

---

**Ready to go!** Start with `python quick_start.py` or open `STUAI.code-workspace` in VS Code.
