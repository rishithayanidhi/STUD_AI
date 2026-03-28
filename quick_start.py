#!/usr/bin/env python
"""
Quick start script - Setup and launch Autonomous Ops Demo with Ollama.
"""

import os
import subprocess
import sys
import time
import requests
from pathlib import Path

def print_header(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}\n")

def check_docker():
    """Check if Docker is installed."""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except:
        return False

def start_ollama():
    """Start Ollama Docker container."""
    print("Starting Ollama...")
    
    # Check if already running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✓ Ollama already running")
            return True
    except:
        pass
    
    # Start container
    if not check_docker():
        print("✗ Docker not found. Please install Docker Desktop.")
        return False
    
    try:
        # Stop if already exists
        subprocess.run(["docker", "stop", "ollama"], capture_output=True)
        subprocess.run(["docker", "rm", "ollama"], capture_output=True)
        
        # Start fresh
        subprocess.run([
            "docker", "run", "-d",
            "--name", "ollama",
            "-p", "11434:11434",
            "ollama/ollama"
        ], check=True)
        
        print("✓ Ollama container started")
        
        # Wait for it to be ready
        print("  Waiting for Ollama to be ready...", end="", flush=True)
        for i in range(30):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print(" ✓")
                    return True
            except:
                pass
            time.sleep(1)
            print(".", end="", flush=True)
        
        print(" ✗")
        return False
    except Exception as e:
        print(f"✗ Error starting Ollama: {e}")
        return False

def pull_model():
    """Pull Llama3 model."""
    print("Pulling Llama3 model (this may take 5-10 minutes on first run)...")
    
    try:
        result = subprocess.run([
            "docker", "exec", "ollama",
            "ollama", "pull", "llama3"
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✓ Model pulled successfully")
            return True
        else:
            print(f"✗ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def setup_venv():
    """Setup Python virtual environment."""
    print("Setting up Python environment...")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✓ Virtual environment already exists")
    else:
        try:
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print("✓ Virtual environment created")
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    # Detect OS and get pip path
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip"
    else:
        pip_path = venv_path / "bin" / "pip"
    
    # Install requirements
    print("Installing dependencies...")
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_system():
    """Test the system setup."""
    print("Testing system...")
    
    # Test Ollama connection
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama is running")
        else:
            print("✗ Ollama connection failed")
            return False
    except:
        print("✗ Ollama not responding at http://localhost:11434")
        return False
    
    # Test Python imports
    try:
        import fastapi
        import requests
        import pydantic
        print("✓ Python dependencies loaded")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    return True

def main():
    print_header("Autonomous Ops Demo - Quick Start")
    
    # Step 1: Start Ollama
    print_header("Step 1: Starting Ollama")
    if not start_ollama():
        print("✗ Failed to start Ollama. Continuing anyway...")
    
    # Step 2: Pull model
    print_header("Step 2: Pulling Llama3 Model")
    if not pull_model():
        print("⚠️  Model pull failed. You can pull manually later.")
    
    # Step 3: Setup Python environment
    print_header("Step 3: Setting Up Python Environment")
    if not setup_venv():
        print("✗ Failed to setup Python environment.")
        sys.exit(1)
    
    # Step 4: Test system
    print_header("Step 4: Testing System")
    if not test_system():
        print("✗ System test failed.")
        sys.exit(1)
    
    # Success!
    print_header("✓ Setup Complete!")
    print("""
Next steps:

1. Start the API server:
   python run_server.py

2. Open browser:
   http://localhost:8000

3. Submit a test ticket and watch the AI classify it!

Optional: Test Ollama directly
   python test_ollama.py

To configure:
   - Edit .env for custom Ollama URL/model
   - Edit tools.py to add custom actions
   - Edit main.py to customize API endpoints

For more information:
   - OLLAMA_SETUP.md - Detailed Ollama setup
   - ARCHITECTURE_COMPLETE.md - Full architecture
   - MIGRATION_OPENAI_TO_OLLAMA.md - Migration guide
    """)

if __name__ == "__main__":
    main()
