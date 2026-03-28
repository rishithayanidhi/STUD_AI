#!/usr/bin/env python3
"""
PostgreSQL Quick Start for Autonomous Ops Demo

This script helps you get PostgreSQL running in seconds.
"""

import subprocess
import sys
import os


def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def check_docker():
    """Check if Docker is installed."""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except:
        return False


def start_postgres_docker():
    """Start PostgreSQL using Docker (easiest method)."""
    print_header("🐳 Starting PostgreSQL with Docker")
    
    container_name = "autonomous-ops-db"
    
    # Check if container already exists
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={container_name}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if container_name in result.stdout:
            print(f"Container '{container_name}' already exists.")
            if "Up" in result.stdout:
                print("✅ Container is already running!\n")
                return True
            else:
                print("Starting existing container...")
                subprocess.run(["docker", "start", container_name], check=True)
                print("✅ Container started!\n")
                return True
    except Exception as e:
        print(f"Note: {e}")
    
    # Create new container
    print("Creating new PostgreSQL container...")
    
    try:
        subprocess.run([
            "docker", "run",
            "--name", container_name,
            "-e", "POSTGRES_USER=postgres",
            "-e", "POSTGRES_PASSWORD=postgres",
            "-e", "POSTGRES_DB=autonomous_ops",
            "-p", "5432:5432",
            "-d",
            "postgres:15-alpine"
        ], check=True, capture_output=True)
        
        print("✅ PostgreSQL container started!\n")
        print("Connection String:")
        print("  postgresql://postgres:postgres@localhost:5432/autonomous_ops\n")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.decode() if e.stderr else str(e)}")
        return False


def main():
    print_header("PostgreSQL Quick Start")
    
    print("""
Your demo supports BOTH PostgreSQL and JSON storage:
  
  • JSON: Works right now ✅
  • PostgreSQL: Optional, makes demo look enterprise-grade 🚀
  
Choose your path:
""")
    
    choice = input("Start PostgreSQL? (yes/no/skip): ").strip().lower()
    
    if choice in ["skip", "n", "no"]:
        print("""
✅ Continuing with JSON storage.
   Your demo works perfectly fine!
   
   To use it: python run_server.py
        """)
        return
    
    if choice not in ["yes", "y"]:
        print("❓ Please enter 'yes' or 'no'")
        main()
        return
    
    # Check if Docker is available
    has_docker = check_docker()
    
    if has_docker:
        print("Docker found. Using Docker method (easiest).\n")
        if start_postgres_docker():
            print_header("✅ PostgreSQL Ready!")
            print("""
Next steps:

1. Start your API:
   python run_server.py
   
   You should see:
   ✅ PostgreSQL connected: postgres@localhost:5432/autonomous_ops

2. Verify in another terminal:
   curl http://localhost:8000/stats | jq

3. When done, stop PostgreSQL:
   docker stop autonomous-ops-db
   
   Or remove it:
   docker rm autonomous-ops-db
            """)
            return
        else:
            print("⚠️  Docker startup failed. See error above.")
            return
    
    else:
        print_header("⚠️  Docker Not Found")
        print("""
For PostgreSQL without Docker, you'll need to install it manually:

Windows: https://www.postgresql.org/download/windows/
macOS:   brew install postgresql
Linux:   sudo apt-get install postgresql

After installing, create the database:
  psql -U postgres
  CREATE DATABASE autonomous_ops;
  \\q

Then:
  python run_server.py

Or use online PostgreSQL:
  Heroku Postgres
  AWS RDS
  Google Cloud SQL
  
Set environment variables:
  export DB_HOST="your-host.com"
  export DB_USER="your-user"
  export DB_PASSWORD="your-password"
  
  python run_server.py
        """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
