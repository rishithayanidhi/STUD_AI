#!/usr/bin/env python
"""
STUAI Autonomous Ops - Main launcher with menu.
Choose what to run: setup, demo, test, or server.
"""

import os
import sys
import subprocess
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Display main menu."""
    clear_screen()
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  STUAI - Autonomous Ops Demo Launcher                     ║
    ╚════════════════════════════════════════════════════════════╝
    
    What do you want to do?
    
    1. 🚀 Quick Setup (Install Ollama + Python dependencies)
    2. 🔧 Start FastAPI Server (http://localhost:8000)
    3. 🧪 Run Tests (API, Ollama, End-to-end)
    4. 📊 Show System Status
    5. 📚 View Documentation
    6. 🎯 Run Demo Script
    7. ✅ Pre-Demo Checklist
    8. 🐳 Docker Setup (advanced)
    
    0. ❌ Exit
    
    """)

def run_quick_setup():
    """Run quick_start.py"""
    print("\n▶️  Running Quick Setup...\n")
    subprocess.run([sys.executable, "quick_start.py"])

def run_server():
    """Run FastAPI server"""
    print("\n▶️  Starting FastAPI Server...\n")
    print("    📍 Access at: http://localhost:8000")
    print("    🛑 Press Ctrl+C to stop\n")
    subprocess.run([sys.executable, "run_server.py"])

def run_tests():
    """Show test options"""
    clear_screen()
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                      Test Options                          ║
    ╚════════════════════════════════════════════════════════════╝
    
    1. 🧪 Test Ollama Integration
    2. 🌐 Test API Endpoints
    3. 📝 Full End-to-End Test
    4. 📊 Test Statistics
    5. 🔙 Back to Main Menu
    
    """)
    
    choice = input("Choose test (1-5): ").strip()
    
    if choice == "1":
        print("\n▶️  Testing Ollama...\n")
        subprocess.run([sys.executable, "test_ollama.py"])
    elif choice == "2":
        print("\n▶️  Testing API...\n")
        subprocess.run([sys.executable, "test_api.py"])
    elif choice == "3":
        print("\n▶️  Running End-to-End Test...\n")
        subprocess.run([sys.executable, "test_demo.py"])
    elif choice == "4":
        print("\n▶️  Testing Statistics...\n")
        subprocess.run([sys.executable, "test_stats.py"])
    elif choice == "5":
        return
    
    input("\n✓ Press Enter to continue...")

def show_status():
    """Show system status"""
    print("\n▶️  Checking System Status...\n")
    subprocess.run([sys.executable, "SUMMARY.py"])
    input("\n✓ Press Enter to continue...")

def view_docs():
    """Show documentation options"""
    clear_screen()
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                   Documentation                            ║
    ╚════════════════════════════════════════════════════════════╝
    
    1. 📖 Main README
    2. 🚀 Ollama Setup Guide
    3. 🏗️  Complete Architecture
    4. 📊 Project Structure
    5. 🔄 Migration Guide (OpenAI → Ollama)
    6. 🗄️  PostgreSQL Complete Guide
    7. 🎯 Ready for Judges
    8. 📋 File Manifest
    9. 📝 Changes & Updates
    10. 🔙 Back to Main Menu
    
    """)
    
    docs = {
        "1": "README.md",
        "2": "OLLAMA_SETUP.md",
        "3": "ARCHITECTURE_COMPLETE.md",
        "4": "STRUCTURE.md",
        "5": "MIGRATION_OPENAI_TO_OLLAMA.md",
        "6": "POSTGRES_COMPLETE.md",
        "7": "READY_FOR_JUDGES.md",
        "8": "FILE_MANIFEST.md",
        "9": "CHANGES.md",
    }
    
    choice = input("Choose document (1-10): ").strip()
    
    if choice in docs:
        print(f"\n📖 Opening {docs[choice]}...\n")
        subprocess.run([
            "cmd" if os.name == "nt" else "open",
            docs[choice]
        ] if os.name == "nt" else ["less", docs[choice]])
    elif choice == "10":
        return
    
    input("\n✓ Press Enter to continue...")

def run_demo():
    """Run demo script"""
    print("\n▶️  Running Demo Script...\n")
    subprocess.run([sys.executable, "DEMO_SCRIPT.py"])

def run_checklist():
    """Run demo checklist"""
    print("\n▶️  Running Pre-Demo Checklist...\n")
    subprocess.run([sys.executable, "DEMO_CHECKLIST.py"])

def docker_setup():
    """Show docker setup info"""
    clear_screen()
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                   Docker Setup                             ║
    ╚════════════════════════════════════════════════════════════╝
    
    Run these commands to set up Ollama with Docker:
    
    1. Start Ollama:
       docker run -d --name ollama -p 11434:11434 ollama/ollama
    
    2. Pull Llama3 model:
       docker exec ollama ollama pull llama3
    
    3. Verify it's working:
       curl http://localhost:11434/api/tags
    
    For GPU acceleration:
       docker run --gpus all -d --name ollama -p 11434:11434 ollama/ollama
    
    Stop Ollama:
       docker stop ollama
    
    Remove Ollama:
       docker rm ollama
    
    """)
    input("✓ Press Enter to continue...")

def main():
    """Main menu loop"""
    while True:
        print_menu()
        choice = input("Enter your choice (0-8): ").strip()
        
        if choice == "1":
            run_quick_setup()
        elif choice == "2":
            run_server()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            show_status()
        elif choice == "5":
            view_docs()
        elif choice == "6":
            run_demo()
        elif choice == "7":
            run_checklist()
        elif choice == "8":
            docker_setup()
        elif choice == "0":
            print("\n👋 Goodbye!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Press Enter and try again...")
            input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...\n")
        sys.exit(0)
