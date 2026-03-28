#!/usr/bin/env python
"""
Display and manage agent configuration.
Shows all customizable settings loaded from environment variables.
"""

import os

# Load configuration from environment (same as agent.py)
CONFIG = {
    "ollama": {
        "url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "model": os.getenv("OLLAMA_MODEL", "llama3"),
        "temperature": float(os.getenv("OLLAMA_TEMPERATURE", "0.3")),
        "timeout": int(os.getenv("OLLAMA_TIMEOUT", "30")),
    },
    "classification": {
        "priority_keywords": {
            "Critical": os.getenv("CRITICAL_KEYWORDS", "failing,500,down,outage,critical,emergency").split(","),
            "High": os.getenv("HIGH_KEYWORDS", "error,bug,issue,broken").split(","),
            "Medium": os.getenv("MEDIUM_KEYWORDS", "slow,performance,degraded").split(","),
            "Low": os.getenv("LOW_KEYWORDS", "feature,enhancement,improvement").split(","),
        },
        "team_assignments": {
            "Backend / Payments": os.getenv("PAYMENTS_KEYWORDS", "payment,billing,transaction,invoice").split(","),
            "Backend": os.getenv("BACKEND_KEYWORDS", "api,server,database,service").split(","),
            "Frontend": os.getenv("FRONTEND_KEYWORDS", "ui,page,layout,button,styling").split(","),
            "DevOps": os.getenv("DEVOPS_KEYWORDS", "deploy,infrastructure,kubernetes,docker,ci/cd").split(","),
            "Operations": os.getenv("OPERATIONS_KEYWORDS", "monitoring,alert,log,metric").split(","),
        },
        "default_team": os.getenv("DEFAULT_TEAM", "Operations"),
        "default_confidence": float(os.getenv("DEFAULT_CONFIDENCE", "0.75")),
    }
}

def print_config():
    """Display current configuration."""
    print("""
╔════════════════════════════════════════════════════════════╗
║           STUAI Agent Configuration (Dynamic)              ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📋 OLLAMA CONFIGURATION")
    print("─" * 60)
    for key, value in CONFIG["ollama"].items():
        print(f"  {key:15} = {value}")
        env_key = f"OLLAMA_{key.upper()}"
        print(f"    (set via: {env_key})")
    
    print("\n🎯 PRIORITY KEYWORDS")
    print("─" * 60)
    for priority, keywords in CONFIG["classification"]["priority_keywords"].items():
        print(f"  {priority:10} : {', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}")
    
    print("\n👥 TEAM ASSIGNMENT KEYWORDS")
    print("─" * 60)
    for team, keywords in CONFIG["classification"]["team_assignments"].items():
        print(f"  {team:20} : {', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}")
    
    print("\n⚙️  CLASSIFICATION DEFAULTS")
    print("─" * 60)
    print(f"  Default Team       = {CONFIG['classification']['default_team']}")
    print(f"  Default Confidence = {CONFIG['classification']['default_confidence']}")
    
    print("""
═══════════════════════════════════════════════════════════════

📝 To CUSTOMIZE:

1. Edit .env file in STUAI folder
2. Modify any OLLAMA_*, *_KEYWORDS, or DEFAULT_* variables
3. Restart the server

Examples:

  # Change model
  OLLAMA_MODEL=mistral

  # Add custom keywords for critical issues
  CRITICAL_KEYWORDS=failing,500,down,outage,critical,emergency,disaster

  # Change default team
  DEFAULT_TEAM=Backend

  # Adjust model temperature (0=deterministic, 1=creative)
  OLLAMA_TEMPERATURE=0.5

═══════════════════════════════════════════════════════════════
    """)

if __name__ == "__main__":
    print_config()
