# Ollama Local LLM Setup Guide

## Overview

This autonomous ops system now uses **Ollama** for local LLM inference instead of OpenAI. This gives you:

- ✅ Zero API costs (runs locally)
- ✅ Full data privacy (no external calls)
- ✅ Open models: Llama3, Mistral, Neural Chat
- ✅ Fast inference with GPU support

## Quick Start (5 minutes)

### Option A: Docker (Recommended)

```bash
# Pull and run Ollama with Llama3
docker pull ollama/ollama
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec ollama ollama pull llama3
```

### Option B: Direct Installation

1. Download: https://ollama.ai
2. Install and run the app
3. Pull a model:
   ```bash
   ollama pull llama3
   # or
   ollama pull mistral
   ```

### Option C: Python Script Setup

```python
# setup_ollama.py - runs in the background
import os
import subprocess

# Download and start Ollama
subprocess.run([
    "docker", "run", "-d",
    "--name", "ollama",
    "-p", "11434:11434",
    "ollama/ollama"
])

# Pull llama3 model
subprocess.run([
    "docker", "exec", "ollama",
    "ollama", "pull", "llama3"
])

print("✓ Ollama running at http://localhost:11434")
```

## Verify Setup

```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test classification
python test_ollama.py
```

## Environment Variables

```bash
# .env file
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3  # or mistral, neural-chat
```

## Available Models

- **llama3** (8B) - Best for operations contexts, excellent reasoning
- **mistral** (7B) - Fast, good at JSON output
- **neural-chat** (7B) - Optimized for conversations

## Performance Tips

- Use GPU: `docker run --gpus all -p 11434:11434 ollama/ollama`
- First run pulls model (5-10 min), subsequent runs are instant
- Classification response: ~2-5 seconds depending on model/hardware

## Integration Points

- **agent.py**: Uses `requests` to call Ollama API
- **main.py**: Works seamlessly, automatic fallback to mock
- **LangGraph support**: Can be added for agent orchestration workflows

## Costs Comparison

| Method         | Setup   | Per Call | Monthly |
| -------------- | ------- | -------- | ------- |
| OpenAI GPT-3.5 | API key | $0.0005  | $150+   |
| Ollama Llama3  | Free    | $0       | $0      |

## Troubleshooting

**"Ollama not available at http://localhost:11434"**

```bash
# Check if running
docker ps | grep ollama

# Start if stopped
docker start ollama

# Check logs
docker logs ollama
```

**System out of memory**

```bash
# Use smaller model
docker exec ollama ollama pull mistral

# Set OLLAMA_MODEL=mistral in .env
```

**GPU not detected**

```bash
# Verify GPU support
nvidia-smi  # For NVIDIA
rocm-smi    # For AMD

# Run with GPU
docker run --gpus all -p 11434:11434 ollama/ollama
```

## Next Steps

1. Start Ollama: `docker run -d -p 11434:11434 ollama/ollama`
2. Pull model: `docker exec ollama ollama pull llama3`
3. Run demo: `python run_server.py`
4. Test: `python test_api.py`
