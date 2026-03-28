#!/usr/bin/env python3
"""
PostgreSQL Database Setup for Autonomous Ops Demo

This script helps set up the PostgreSQL database connection.
"""

import os
import sys

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def main():
    print_header("📊 PostgreSQL Setup for Autonomous Ops Demo")
    
    print("""
This demo can work in two ways:

1. 🟢 WITH PostgreSQL (Recommended)
   - More production-like architecture
   - Better for scaling
   - Shows enterprise capabilities to judges
   
2. 🟡 WITHOUT PostgreSQL (Fallback)
   - Uses JSON file storage (already working)
   - No database setup needed
   - Still fully functional demo

""")
    
    choice = input("Would you like to set up PostgreSQL? (yes/no): ").strip().lower()
    
    if choice not in ['yes', 'y']:
        print("""
✅ Skipping PostgreSQL setup.
   Your demo will use JSON file storage.
   Start the server: python run_server.py
        """)
        return
    
    print_header("🔧 PostgreSQL Setup Options")
    
    print("""
Choose your setup method:

1️⃣  Local PostgreSQL (if you have it installed)
2️⃣  Docker PostgreSQL (easiest if Docker installed)
3️⃣  Connection to existing PostgreSQL server
4️⃣  Skip for now (use JSON fallback)
    """)
    
    method = input("Choose option (1-4): ").strip()
    
    if method == "1":
        setup_local_postgres()
    elif method == "2":
        setup_docker_postgres()
    elif method == "3":
        setup_remote_postgres()
    else:
        print("\n✅ Continuing with JSON fallback.")


def setup_local_postgres():
    """Set up local PostgreSQL."""
    print_header("📦 Local PostgreSQL Setup")
    
    print("""
To use local PostgreSQL:

1. Install PostgreSQL:
   - Windows: https://www.postgresql.org/download/windows/
   - Mac: brew install postgresql
   - Linux: sudo apt-get install postgresql postgresql-contrib

2. Start PostgreSQL service:
   - Windows: Services → PostgreSQL Database Server → Start
   - Mac: brew services start postgresql
   - Linux: sudo systemctl start postgresql

3. Create the database:
   """)
    
    commands = """
# Connect to PostgreSQL
psql -U postgres

# Then run these commands:
CREATE DATABASE autonomous_ops;
\\c autonomous_ops

# Tables will be created automatically
    """
    
    print(commands)
    
    print("\n4. Set environment variables (optional, these are the defaults):")
    
    env_vars = """
# Linux/Mac .bashrc or .zshrc:
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=autonomous_ops
export DB_USER=postgres
export DB_PASSWORD=postgres

# Windows PowerShell:
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="autonomous_ops"
$env:DB_USER="postgres"
$env:DB_PASSWORD="postgres"
    """
    
    print(env_vars)
    
    print("\n5. Test connection:")
    print("   python run_server.py")
    print("\n   You should see: ✅ PostgreSQL connected: postgres@localhost:5432/autonomous_ops")


def setup_docker_postgres():
    """Set up PostgreSQL with Docker."""
    print_header("🐳 Docker PostgreSQL Setup")
    
    print("""
To use PostgreSQL in Docker:

1. Install Docker: https://www.docker.com/products/docker-desktop

2. Start PostgreSQL container:
   """)
    
    docker_cmd = """
docker run --name autonomous-ops-db \\
  -e POSTGRES_USER=postgres \\
  -e POSTGRES_PASSWORD=postgres \\
  -e POSTGRES_DB=autonomous_ops \\
  -p 5432:5432 \\
  -d postgres:15-alpine
    """
    
    print(docker_cmd)
    
    print("\n3. Verify container is running:")
    print("   docker ps")
    print("\n   You should see: autonomous-ops-db")
    
    print("\n4. Start the demo server:")
    print("   python run_server.py")
    print("\n   You should see: ✅ PostgreSQL connected: postgres@localhost:5432/autonomous_ops")
    
    print("\n5. When done, stop the container:")
    print("   docker stop autonomous-ops-db")
    print("\n   Or remove it completely:")
    print("   docker rm autonomous-ops-db")


def setup_remote_postgres():
    """Set up connection to remote PostgreSQL."""
    print_header("🌐 Remote PostgreSQL Setup")
    
    print("\nEnter your PostgreSQL connection details:\n")
    
    db_host = input("Database host (default: localhost): ").strip() or "localhost"
    db_port = input("Database port (default: 5432): ").strip() or "5432"
    db_name = input("Database name (default: autonomous_ops): ").strip() or "autonomous_ops"
    db_user = input("Username (default: postgres): ").strip() or "postgres"
    db_password = input("Password (default: postgres): ").strip() or "postgres"
    
    print("\n" + "="*70)
    print("Environment Variables to Set:")
    print("="*70 + "\n")
    
    print(f"DB_HOST={db_host}")
    print(f"DB_PORT={db_port}")
    print(f"DB_NAME={db_name}")
    print(f"DB_USER={db_user}")
    print(f"DB_PASSWORD={db_password}")
    
    # Provide shell commands
    print("\n\n📋 Copy-Paste Commands:\n")
    
    print("Linux/Mac (.bashrc or .zshrc):")
    print(f"""
export DB_HOST="{db_host}"
export DB_PORT="{db_port}"
export DB_NAME="{db_name}"
export DB_USER="{db_user}"
export DB_PASSWORD="{db_password}"
    """)
    
    print("Windows PowerShell:")
    print(f"""
$env:DB_HOST="{db_host}"
$env:DB_PORT="{db_port}"
$env:DB_NAME="{db_name}"
$env:DB_USER="{db_user}"
$env:DB_PASSWORD="{db_password}"
    """)
    
    print("\nOr set them in a .env file and load before running:")
    print("   python run_server.py")
    
    print("\n✅ Then test the connection:")
    print("   python run_server.py")
    print("\n   You should see: ✅ PostgreSQL connected")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Setup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
