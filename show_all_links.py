#!/usr/bin/env python
"""
Display all URLs and links needed for STUAI Autonomous Ops.
Organized by service and environment configuration.
"""

import os
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title: str):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {title}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def print_item(name: str, url: str, description: str = ""):
    """Print a URL item."""
    print(f"{Colors.GREEN}✓{Colors.ENDC} {Colors.BOLD}{name}{Colors.ENDC}")
    print(f"  URL: {Colors.CYAN}{url}{Colors.ENDC}")
    if description:
        print(f"  {description}")
    print()

def get_local_urls() -> List[Tuple[str, str, str]]:
    """Get local service URLs."""
    return [
        ("Ollama API", "http://localhost:11434", "Local LLM inference"),
        ("FastAPI Server", "http://localhost:8000", "Main application"),
        ("FastAPI Docs", "http://localhost:8000/docs", "Swagger UI documentation"),
        ("FastAPI ReDoc", "http://localhost:8000/redoc", "Alternative API docs"),
        ("PostgreSQL", "postgresql://localhost:5432/autonomous_ops", "Database connection"),
        ("Redis", "redis://localhost:6379/0", "Message queue"),
        ("ChromaDB", "http://localhost:8000/chroma", "Vector database (embedded)"),
        ("pgAdmin", "http://localhost:5050", "PostgreSQL admin tool"),
    ]

def get_fastapi_endpoints() -> Dict[str, List[Tuple[str, str]]]:
    """Get FastAPI endpoints."""
    return {
        "Ticket Management": [
            ("POST /ticket", "Submit a new ticket"),
            ("GET /memory/tickets", "Get all tickets"),
            ("GET /memory/search?query=text", "Search tickets"),
        ],
        "System Status": [
            ("GET /health", "Health check"),
            ("GET /stats", "Backend statistics"),
        ],
        "Real-time": [
            ("WebSocket /ws", "WebSocket for live updates"),
        ],
    }

def get_github_urls() -> List[Tuple[str, str, str]]:
    """Get GitHub API URLs."""
    return [
        ("GitHub API", "https://api.github.com", "Base endpoint"),
        ("Create Issue", "https://api.github.com/repos/{owner}/{repo}/issues", "POST method"),
        ("Add Comment", "https://api.github.com/repos/{owner}/{repo}/issues/{number}/comments", "POST method"),
        ("Update Issue", "https://api.github.com/repos/{owner}/{repo}/issues/{number}", "PATCH method"),
        ("Personal Token", "https://github.com/settings/tokens", "Generate/manage tokens"),
        ("Create App Token", "https://github.com/settings/personal-access-tokens/new", "Create PAT"),
    ]

def get_slack_urls() -> List[Tuple[str, str, str]]:
    """Get Slack API URLs."""
    return [
        ("Slack API", "https://slack.com/api/", "Base endpoint"),
        ("Post Message", "https://slack.com/api/chat.postMessage", "Send message"),
        ("View Apps", "https://api.slack.com/apps", "Create/manage apps"),
        ("Create App", "https://api.slack.com/apps?new_app=1", "New bot app"),
        ("Scopes Docs", "https://api.slack.com/scopes", "Available permissions"),
        ("Incoming Webhooks", "https://api.slack.com/messaging/webhooks", "Webhook setup"),
    ]

def get_other_services() -> List[Tuple[str, str, str]]:
    """Get other external service URLs."""
    return [
        ("PagerDuty Events", "https://events.pagerduty.com/v2/enqueue", "Trigger incidents"),
        ("PagerDuty API", "https://api.pagerduty.com/", "Event operations"),
        ("Jira Cloud", "https://your-domain.atlassian.net/rest/api/3/", "Jira REST API"),
        ("Gmail SMTP", "smtp://smtp.gmail.com:587", "Email service"),
        ("Gmail Settings", "https://myaccount.google.com/apppasswords", "App password setup"),
        ("OpenAI (deprecated)", "https://api.openai.com/v1/", "For reference only"),
    ]

def get_documentation_urls() -> List[Tuple[str, str]]:
    """Get documentation URLs."""
    return [
        ("Ollama Docs", "https://ollama.ai"),
        ("FastAPI Docs", "https://fastapi.tiangolo.com"),
        ("PostgreSQL Docs", "https://www.postgresql.org/docs/"),
        ("Redis Docs", "https://redis.io/docs/"),
        ("LangGraph Docs", "https://langchain-ai.github.io/langgraph/"),
        ("GitHub API", "https://docs.github.com/rest"),
        ("Slack API", "https://api.slack.com/docs"),
    ]

def get_env_variables() -> Dict[str, str]:
    """Get current environment variable values."""
    env_vars = {
        "OLLAMA_URL": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama3"),
        "DATABASE_URL": os.getenv("DATABASE_URL", "postgresql://localhost:5432/autonomous_ops"),
        "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN", "NOT SET"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "NOT SET"),
        "HOST": os.getenv("HOST", "0.0.0.0"),
        "PORT": os.getenv("PORT", "8000"),
    }
    return env_vars

def print_links():
    """Print all links and URLs."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          STUAI Autonomous Ops - Complete URL Reference            ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(Colors.ENDC)

    # Local Services
    print_section("🖥️  LOCAL SERVICES (Required)")
    for name, url, desc in get_local_urls():
        print_item(name, url, desc)

    # FastAPI Endpoints
    print_section("🔌 FASTAPI ENDPOINTS")
    endpoints = get_fastapi_endpoints()
    for category, items in endpoints.items():
        print(f"{Colors.BOLD}{category}{Colors.ENDC}")
        for endpoint, description in items:
            print(f"  {Colors.GREEN}→{Colors.ENDC} {Colors.CYAN}http://localhost:8000{endpoint}{Colors.ENDC}")
            print(f"    {description}\n")

    # GitHub
    print_section("🐙 GITHUB API (Optional)")
    for name, url, desc in get_github_urls():
        print_item(name, url, desc)

    # Slack
    print_section("💬 SLACK API (Optional)")
    for name, url, desc in get_slack_urls():
        print_item(name, url, desc)

    # Other Services
    print_section("🔗 OTHER EXTERNAL SERVICES (Optional)")
    for name, url, desc in get_other_services():
        print_item(name, url, desc)

    # Environment Variables
    print_section("🔐 ENVIRONMENT VARIABLES (Current Values)")
    env_vars = get_env_variables()
    for key, value in env_vars.items():
        if "TOKEN" in key or "PASSWORD" in key:
            display_value = f"{Colors.YELLOW}{'*' * 20}{Colors.ENDC}"
        else:
            display_value = Colors.CYAN + value + Colors.ENDC
        print(f"  {Colors.BOLD}{key:20}{Colors.ENDC} = {display_value}")
    print()

    # Documentation
    print_section("📚 DOCUMENTATION & GUIDES")
    for name, url in get_documentation_urls():
        print(f"  {Colors.GREEN}→{Colors.ENDC} {Colors.BOLD}{name:25}{Colors.ENDC} {Colors.CYAN}{url}{Colors.ENDC}\n")

    # Quick Commands
    print_section("⚡ QUICK START COMMANDS")
    commands = [
        ("Start Ollama", "docker run -d -p 11434:11434 ollama/ollama"),
        ("Pull Model", "docker exec ollama ollama pull llama3"),
        ("Start FastAPI", "python run_server.py"),
        ("View Config", "python config_view.py"),
        ("Test API", "python test_api.py"),
        ("Test Ollama", "python test_ollama.py"),
    ]
    for name, cmd in commands:
        print(f"  {Colors.BOLD}{name:20}{Colors.ENDC}")
        print(f"  {Colors.CYAN}  $ {cmd}{Colors.ENDC}\n")

    # Test URLs
    print_section("🧪 TEST THESE URLS")
    test_urls = [
        ("Ollama Status", "curl http://localhost:11434/api/tags", "Check if Ollama running"),
        ("FastAPI Health", "curl http://localhost:8000/health", "Check if API running"),
        ("API Docs", "http://localhost:8000/docs", "Interactive API explorer"),
        ("Submit Ticket", 'curl -X POST http://localhost:8000/ticket -H "Content-Type: application/json" -d \'{"issue":"test"}\'', "Submit test ticket"),
    ]
    for name, url, note in test_urls:
        print(f"  {Colors.BOLD}{name}{Colors.ENDC}")
        print(f"    {Colors.CYAN}{url}{Colors.ENDC}")
        print(f"    Note: {note}\n")

    # File Reference
    print_section("📂 LOCAL PROJECT FILES WITH DOCS")
    files = [
        ("agent.py", "Dynamic Ollama agent with env config"),
        ("main.py", "FastAPI server with all endpoints"),
        ("memory.py", "PostgreSQL + JSON storage"),
        ("tools.py", "Autonomous action execution"),
        ("config_view.py", "View current configuration"),
        (".env.example", "Configuration template"),
        ("OLLAMA_SETUP.md", "Ollama installation guide"),
        ("ARCHITECTURE_COMPLETE.md", "Full system architecture"),
    ]
    for fname, description in files:
        print(f"  {Colors.GREEN}✓{Colors.ENDC} {Colors.BOLD}{fname:30}{Colors.ENDC} {description}\n")

    # Summary
    print_section("📋 SUMMARY")
    print(f"""
{Colors.GREEN}✓ Minimum Setup (works offline):{Colors.ENDC}
  - Ollama: http://localhost:11434
  - FastAPI: http://localhost:8000
  - JSON storage (no database needed)

{Colors.GREEN}✓ Production Setup:{Colors.ENDC}
  - Add PostgreSQL: postgresql://localhost:5432
  - Add Redis: redis://localhost:6379
  - Configure integrations: GitHub, Slack, etc.

{Colors.GREEN}✓ Configuration:{Colors.ENDC}
  - Edit .env file in STUAI folder
  - Run: python config_view.py
  - Restart: python run_server.py

{Colors.GREEN}✓ Testing:{Colors.ENDC}
  - API: http://localhost:8000/docs
  - Ollama: curl http://localhost:11434/api/tags
  - Backend: python test_api.py

{Colors.BOLD}Ready to start? Run: python quick_start.py{Colors.ENDC}
    """)

if __name__ == "__main__":
    print_links()
