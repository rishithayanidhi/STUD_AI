#!/usr/bin/env python3
"""
Simple wrapper to run the FastAPI server from anywhere.
"""
import os
import sys
from pathlib import Path

# Get the directory where this script is located
demo_dir = Path(__file__).parent.absolute()

# Change to demo directory
os.chdir(demo_dir)
sys.path.insert(0, str(demo_dir))

# Now import and run
from main import app
import uvicorn

if __name__ == "__main__":
    print(f"🚀 Starting Autonomous Ops Demo API from {demo_dir}")
    print(f"📖 API docs: http://localhost:8000/docs")
    print(f"🌐 Frontend: http://localhost:8000")
    print("Press Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
