# Migration Guide: OpenAI → Ollama (Local LLM)

## Why Migrate to Ollama?

| Aspect            | OpenAI                         | Ollama                 |
| ----------------- | ------------------------------ | ---------------------- |
| **Cost**          | $0.0005 per request (~$150/mo) | Free ($0/mo)           |
| **API Key**       | Required                       | Not needed             |
| **Data Privacy**  | External API calls             | Runs locally           |
| **Models**        | Closed (GPT-3.5, GPT-4)        | Open (Llama3, Mistral) |
| **Latency**       | ~1-2s (network)                | 2-5s (local)           |
| **Offline**       | ✗ Requires internet            | ✓ Works offline        |
| **Customization** | Limited                        | Full model control     |

## What Changed

### 1. Dependencies

```diff
- openai==1.3.0
+ ollama==0.1.24
+ langgraph==0.2.0
+ langchain==0.1.0
+ redis==5.0.1
```

### 2. Environment Variables

```bash
# Before (OpenAI)
OPENAI_API_KEY=sk-...

# After (Ollama)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3  # or mistral
```

### 3. Agent Code

```python
# Before
from openai import OpenAI
client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...]
)

# After
import requests
def get_ollama_client():
    return {
        "url": "http://localhost:11434",
        "model": "llama3"
    }

response = requests.post(
    f"{client['url']}/api/generate",
    json={"model": client['model'], "prompt": prompt}
)
```

## Migration Steps

### Step 1: Setup Ollama (5 minutes)

```bash
# Option A: Docker (Recommended)
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec ollama ollama pull llama3

# Option B: Direct
# Download from https://ollama.ai and run app
ollama pull llama3
```

### Step 2: Update Dependencies

```bash
pip install -r requirements.txt
# This includes ollama library (though we use direct HTTP requests)
```

### Step 3: Update Environment

```bash
# .env file
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
# Remove: OPENAI_API_KEY
```

### Step 4: Test Integration

```bash
python test_ollama.py
```

### Step 5: Start System

```bash
python run_server.py
```

## Verification Checklist

- [ ] Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Model pulled: `docker exec ollama ollama list`
- [ ] Test passes: `python test_ollama.py`
- [ ] API works: `python test_api.py`
- [ ] Demo works: Submit ticket at `http://localhost:8000`

## Model Selection

### Best Overall: Llama3

- **Reasoning**: Excellent for operations context
- **Speed**: ~3-5 seconds
- **VRAM**: 6-8GB (GPU) / 8-10GB (CPU fallback)
- **Cost**: Free

```bash
docker exec ollama ollama pull llama3
```

### Best for Speed: Mistral

- **Reasoning**: Good for JSON classification
- **Speed**: ~1-3 seconds
- **VRAM**: 4-6GB
- **Cost**: Free

```bash
docker exec ollama ollama pull mistral
```

### Best for Quality: Neural Chat

- **Reasoning**: Great conversational ability
- **Speed**: ~2-4 seconds
- **VRAM**: 5-7GB
- **Cost**: Free

```bash
docker exec ollama ollama pull neural-chat
```

## Performance Tuning

### GPU Acceleration

```bash
# NVIDIA
docker run --gpus all -p 11434:11434 ollama/ollama

# AMD (ROCm)
docker run --device=/dev/kfd --device=/dev/dri -p 11434:11434 ollama/ollama

# Check GPU usage
nvidia-smi watch -n 1
```

### Response Tuning

```python
# In agent.py - adjust these for speed/quality tradeoff
response = requests.post(
    f"{client['url']}/api/generate",
    json={
        "model": client['model'],
        "prompt": prompt,
        "stream": False,
        "temperature": 0.3,      # Lower = more deterministic
        "top_p": 0.9,            # Nucleus sampling
        "top_k": 40,             # Top-K filtering
        "num_predict": 200,      # Max tokens (faster if lower)
    }
)
```

### Memory Management

```bash
# Monitor memory
docker stats ollama

# Reduce memory usage
# 1. Use smaller model: mistral instead of llama3
# 2. Configure quantization: ollama pull mistral:latest
# 3. Unload unused models: ollama serve --num-parallel 1
```

## Troubleshooting

### Ollama Not Responding

```bash
# Check if running
docker ps | grep ollama

# Start if stopped
docker start ollama

# View logs
docker logs ollama

# Restart clean
docker stop ollama
docker rm ollama
docker run -d -p 11434:11434 ollama/ollama
```

### Model Not Found

```bash
# List available models
docker exec ollama ollama list

# Pull missing model
docker exec ollama ollama pull llama3

# Check download progress
docker logs ollama
```

### Slow Response / High CPU

```bash
# 1. Switch to smaller model
OLLAMA_MODEL=mistral

# 2. Use GPU acceleration
docker run --gpus all ...

# 3. Optimize prompt size
# Shorter prompts = faster responses

# 4. Check system resources
# Free up RAM/disk space
```

### JSON Parse Errors

````python
# Issue: Ollama sometimes returns text before JSON
# Solution in agent.py already handles this:

if "```json" in response_text:
    response_text = response_text.split("```json")[1].split("```")[0].strip()
elif "```" in response_text:
    response_text = response_text.split("```")[1].split("```")[0].strip()

result = json.loads(response_text)
````

## Rollback to OpenAI (if needed)

If you need to revert to OpenAI:

```bash
# 1. Install OpenAI
pip install openai==1.3.0

# 2. Restore agent.py from git
git checkout agent.py

# 3. Set API key
export OPENAI_API_KEY=sk-...

# 4. Restart
python run_server.py
```

## Advanced: Custom Model Training

You can fine-tune models for your specific operations context:

```bash
# Option 1: Use Ollama with custom model
docker exec ollama ollama create my-ops-model --from llama3

# Option 2: Run your own Ollama instance with tuned model
docker run -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
```

## Integration with Other Tools

### LangGraph Workflow

```python
# tools.py can now be extended with agent workflow
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Define agent workflow
workflow = StateGraph(AgentState)
workflow.add_node("llm", agent_node)
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge("llm", "tools")
```

### Slack Integration

```python
# Send ticket classification to Slack
slack_client.chat_postMessage(
    channel="#ops",
    text=f"New {classification['priority']} ticket: {issue}",
    blocks=[...]
)
```

### Redis Queue Integration

```python
# Queue tickets for async processing
redis_client.lpush("ticket-queue", json.dumps(ticket))

# Worker processes
for ticket in redis_queue:
    decision = process_ticket(ticket)
    store_decision(decision)
```

## Cost Savings Example

### Before (OpenAI)

- 100 tickets/day
- $0.0005 per request
- $50/month
- $600/year

### After (Ollama)

- 100 tickets/day
- $0/cost
- $0/month
- $0/year

**Annual Savings: $600**
Plus: No API limits, full data privacy, offline capability!

## Next Steps

1. Follow the setup steps above
2. Run `test_ollama.py` to verify
3. Submit a ticket to test end-to-end
4. Monitor logs: `docker logs ollama -f`
5. Customize agent behavior as needed

## Support

- Ollama docs: https://ollama.ai
- Model list: https://ollama.ai/library
- GitHub issues: https://github.com/ollama/ollama
