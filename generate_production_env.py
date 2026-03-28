#!/usr/bin/env python
"""
Interactive Production Environment Generator
Guides user step-by-step to collect real credentials and generate .env
"""

import os
import sys
from typing import Optional

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print section header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def get_input(prompt: str, required: bool = False, secret: bool = False) -> str:
    """Get user input with optional validation."""
    while True:
        if secret:
            import getpass
            value = getpass.getpass(f"{Colors.YELLOW}➜{Colors.ENDC} {prompt}: ")
        else:
            value = input(f"{Colors.YELLOW}➜{Colors.ENDC} {prompt}: ")
        
        if not required or value.strip():
            return value.strip()
        print(f"{Colors.RED}✗{Colors.ENDC} This field is required!")

def confirm(prompt: str) -> bool:
    """Get yes/no confirmation."""
    while True:
        response = input(f"{Colors.YELLOW}➜{Colors.ENDC} {prompt} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False

def generate_env():
    """Generate production .env file interactively."""
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║     STUAI Production Deployment - Environment Generator           ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(Colors.ENDC)

    env_config = {}

    # ============== OLLAMA CONFIGURATION ==============
    print_header("1️⃣  OLLAMA CONFIGURATION (Local LLM)")
    print(f"""
{Colors.GREEN}✓ Ollama Setup Options:{Colors.ENDC}
  1. Local (localhost): http://localhost:11434
  2. Remote Server: http://192.168.1.100:11434 (example)
  3. Cloud Instance: AWS EC2, GCP Compute, Azure VM

{Colors.CYAN}Need help?{Colors.ENDC}
  • Local Docker: docker run -d -p 11434:11434 ollama/ollama
  • Remote: ssh into server and run same command
  • Get server IP: hostname -I or ping your-server.com
    """)
    
    env_config["OLLAMA_URL"] = get_input("Enter Ollama URL", required=True) or "http://localhost:11434"
    env_config["OLLAMA_MODEL"] = get_input("Enter Ollama Model (llama3/mistral/neural-chat)", required=True) or "llama3"
    env_config["OLLAMA_TEMPERATURE"] = get_input("Model temperature (0.0-1.0, default 0.3)") or "0.3"
    env_config["OLLAMA_TIMEOUT"] = get_input("Request timeout in seconds (default 30)") or "30"

    # ============== GITHUB CONFIGURATION ==============
    if confirm("\n2️⃣  Configure GitHub Integration?"):
        print_header("GITHUB SETUP")
        print(f"""
{Colors.GREEN}✓ Get GitHub Token:{Colors.ENDC}
  1. Go to: https://github.com/settings/personal-access-tokens/new
  2. Name: "STUAI Production"
  3. Expiration: 90 days
  4. Scopes: repo, read:user, user:email
  5. Click "Generate token"
  6. COPY THE TOKEN (won't appear again!)

{Colors.YELLOW}⚠️  Token Format:{Colors.ENDC}  ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx
        """)
        
        env_config["GITHUB_TOKEN"] = get_input("GitHub Personal Access Token", required=True, secret=True)
        env_config["GITHUB_REPO"] = get_input("GitHub Repository (owner/repo)", required=True)
    else:
        env_config["GITHUB_TOKEN"] = ""
        env_config["GITHUB_REPO"] = ""

    # ============== SLACK CONFIGURATION ==============
    if confirm("\n3️⃣  Configure Slack Integration?"):
        print_header("SLACK BOT SETUP")
        print(f"""
{Colors.GREEN}✓ Create Slack Bot:{Colors.ENDC}
  1. Go to: https://api.slack.com/apps/new
  2. Click "From scratch"
  3. App Name: "STUAI Bot"
  4. Select workspace
  5. Left menu → OAuth & Permissions
  6. Add scopes: chat:write, channels:read, users:read, team:read
  7. Install to workspace
  8. Copy "Bot User OAuth Token"

{Colors.YELLOW}⚠️  Token Format:{Colors.ENDC}  xoxb-1234567890-abcdefghijk-xxxxxxxxxxxxxx
        """)
        
        env_config["SLACK_BOT_TOKEN"] = get_input("Slack Bot Token", required=True, secret=True)
        env_config["SLACK_CHANNEL"] = get_input("Slack Channel (e.g., #ops)", required=True)
    else:
        env_config["SLACK_BOT_TOKEN"] = ""
        env_config["SLACK_CHANNEL"] = ""

    # ============== DATABASE CONFIGURATION ==============
    print_header("4️⃣  DATABASE CONFIGURATION")
    print(f"""
{Colors.GREEN}✓ Database Options:{Colors.ENDC}
  
  Option A: JSON File (Development)
    DATABASE_URL=
    
  Option B: Local PostgreSQL
    DATABASE_URL=postgresql://user:password@localhost:5432/autonomous_ops
    
  Option C: AWS RDS (Production)
    DATABASE_URL=postgresql://admin:password@autonomous-ops-db.xxxxx.us-east-1.rds.amazonaws.com:5432/autonomous_ops
    
  Option D: ElephantSQL (Free)
    DATABASE_URL=postgresql://lvzzxabc:xyz@otto.db.elephantsql.com:5432/lvzzxabc

{Colors.CYAN}Setup links:{Colors.ENDC}
  • AWS RDS: https://console.aws.amazon.com/rds/
  • ElephantSQL: https://www.elephantsql.com/
    """)
    
    env_config["DATABASE_URL"] = get_input("Database URL (leave empty for JSON fallback)")

    # ============== REDIS CONFIGURATION ==============
    if confirm("\n5️⃣  Configure Redis Queue?"):
        print_header("REDIS SETUP")
        print(f"""
{Colors.GREEN}✓ Redis Options:{Colors.ENDC}
  
  Option A: Local Docker
    REDIS_URL=redis://localhost:6379/0
    
  Option B: Redis Cloud (Free 30MB)
    REDIS_URL=redis://:PASSWORD@xxxxx.redis.cloud.com:12345
    
  Option C: AWS ElastiCache
    REDIS_URL=redis://node.xxxxx.ng.0001.use1.cache.amazonaws.com:6379

{Colors.CYAN}Setup links:{Colors.ENDC}
  • Redis Cloud: https://redis.com/try-free/
  • AWS ElastiCache: https://console.aws.amazon.com/elasticache/
        """)
        
        env_config["REDIS_URL"] = get_input("Redis URL", required=True)
    else:
        env_config["REDIS_URL"] = ""

    # ============== EMAIL CONFIGURATION ==============
    if confirm("\n6️⃣  Configure Email Service?"):
        print_header("EMAIL SETUP")
        print(f"""
{Colors.GREEN}✓ Email Provider Options:{Colors.ENDC}
  
  Option A: Gmail
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    Get app password: https://myaccount.google.com/apppasswords
    
  Option B: Sendgrid (100 emails/day free)
    SMTP_SERVER=smtp.sendgrid.net
    SMTP_PORT=587
    Username: apikey
    Get key: https://app.sendgrid.com/settings/api_keys
    
  Option C: Office 365
    SMTP_SERVER=smtp.office365.com
    SMTP_PORT=587
        """)
        
        env_config["SMTP_SERVER"] = get_input("SMTP Server", required=True)
        env_config["SMTP_PORT"] = get_input("SMTP Port (default 587)") or "587"
        env_config["SMTP_USERNAME"] = get_input("SMTP Username/Email", required=True)
        env_config["SMTP_PASSWORD"] = get_input("SMTP Password", required=True, secret=True)
    else:
        env_config["SMTP_SERVER"] = ""
        env_config["SMTP_PORT"] = ""
        env_config["SMTP_USERNAME"] = ""
        env_config["SMTP_PASSWORD"] = ""

    # ============== JIRA CONFIGURATION ==============
    if confirm("\n7️⃣  Configure Jira Ticket Creation?"):
        print_header("JIRA SETUP")
        print(f"""
{Colors.GREEN}✓ Get Jira API Token:{Colors.ENDC}
  1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
  2. Click "Create API token"
  3. Name: "STUAI Bot"
  4. COPY THE TOKEN
  
{Colors.CYAN}Your Jira Instance:{Colors.ENDC}
  • URL format: https://YOUR-COMPANY.atlassian.net
  • Find it in Jira → Settings → Project Settings
        """)
        
        env_config["JIRA_URL"] = get_input("Jira URL (https://xxx.atlassian.net)", required=True)
        env_config["JIRA_USERNAME"] = get_input("Jira Username/Email", required=True)
        env_config["JIRA_API_TOKEN"] = get_input("Jira API Token", required=True, secret=True)
    else:
        env_config["JIRA_URL"] = ""
        env_config["JIRA_USERNAME"] = ""
        env_config["JIRA_API_TOKEN"] = ""

    # ============== PAGERDUTY CONFIGURATION ==============
    if confirm("\n8️⃣  Configure PagerDuty Incident Management?"):
        print_header("PAGERDUTY SETUP")
        print(f"""
{Colors.GREEN}✓ Get Integration Key:{Colors.ENDC}
  1. Log in to PagerDuty dashboard
  2. Go to Services
  3. Create new service
  4. Add "Events API v2" integration
  5. COPY THE INTEGRATION KEY

{Colors.CYAN}Dashboard:{Colors.ENDC} https://www.pagerduty.com/
        """)
        
        env_config["PAGERDUTY_INTEGRATION_KEY"] = get_input("PagerDuty Integration Key", required=True, secret=True)
    else:
        env_config["PAGERDUTY_INTEGRATION_KEY"] = ""

    # ============== SERVER CONFIGURATION ==============
    print_header("9️⃣  SERVER CONFIGURATION")
    env_config["HOST"] = get_input("API Host (default 0.0.0.0)") or "0.0.0.0"
    env_config["PORT"] = get_input("API Port (default 8000)") or "8000"
    env_config["DEBUG"] = "False" if confirm("Production mode? (set DEBUG=False)") else "True"

    # ============== GENERATE FILE ==============
    print_header("📝 GENERATING .env FILE")
    
    env_content = generate_env_content(env_config)
    
    # Write to .env
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(f"{Colors.GREEN}✓{Colors.ENDC} Successfully created {Colors.CYAN}.env{Colors.ENDC} file!")
    print(f"\n{Colors.BOLD}Next steps:{Colors.ENDC}")
    print(f"  1. {Colors.CYAN}python show_all_links.py{Colors.ENDC}      (Verify all credentials)")
    print(f"  2. {Colors.CYAN}python quick_start.py{Colors.ENDC}         (Start system)")
    print(f"  3. {Colors.CYAN}http://localhost:8000{Colors.ENDC}         (Access application)")

def generate_env_content(config: dict) -> str:
    """Generate .env file content."""
    return f"""# STUAI Autonomous Ops - Production Configuration
# Generated: {__import__('datetime').datetime.now().isoformat()}
# WARNING: Keep this file secure! Don't commit to git!

# ============================================
# Ollama Local LLM Configuration
# ============================================
OLLAMA_URL={config.get('OLLAMA_URL', 'http://localhost:11434')}
OLLAMA_MODEL={config.get('OLLAMA_MODEL', 'llama3')}
OLLAMA_TEMPERATURE={config.get('OLLAMA_TEMPERATURE', '0.3')}
OLLAMA_TIMEOUT={config.get('OLLAMA_TIMEOUT', '30')}

# ============================================
# GitHub Integration (Optional)
# ============================================
GITHUB_TOKEN={config.get('GITHUB_TOKEN', '')}
GITHUB_REPO={config.get('GITHUB_REPO', '')}

# ============================================
# Slack Integration (Optional)
# ============================================
SLACK_BOT_TOKEN={config.get('SLACK_BOT_TOKEN', '')}
SLACK_CHANNEL={config.get('SLACK_CHANNEL', '')}

# ============================================
# Database Configuration
# ============================================
# Leave empty to use JSON fallback
DATABASE_URL={config.get('DATABASE_URL', '')}

# ============================================
# Redis Queue (Optional)
# ============================================
REDIS_URL={config.get('REDIS_URL', '')}

# ============================================
# Email Service (Optional)
# ============================================
SMTP_SERVER={config.get('SMTP_SERVER', '')}
SMTP_PORT={config.get('SMTP_PORT', '587')}
SMTP_USERNAME={config.get('SMTP_USERNAME', '')}
SMTP_PASSWORD={config.get('SMTP_PASSWORD', '')}

# ============================================
# Jira Integration (Optional)
# ============================================
JIRA_URL={config.get('JIRA_URL', '')}
JIRA_USERNAME={config.get('JIRA_USERNAME', '')}
JIRA_API_TOKEN={config.get('JIRA_API_TOKEN', '')}

# ============================================
# PagerDuty Integration (Optional)
# ============================================
PAGERDUTY_INTEGRATION_KEY={config.get('PAGERDUTY_INTEGRATION_KEY', '')}

# ============================================
# API Server Configuration
# ============================================
HOST={config.get('HOST', '0.0.0.0')}
PORT={config.get('PORT', '8000')}
DEBUG={config.get('DEBUG', 'False')}

# ============================================
# Priority Classification Keywords
# ============================================
CRITICAL_KEYWORDS=failing,500,down,outage,critical,emergency,disaster
HIGH_KEYWORDS=error,bug,issue,broken,malfunction
MEDIUM_KEYWORDS=slow,performance,degraded,latency
LOW_KEYWORDS=feature,enhancement,improvement,documentation

# ============================================
# Team Assignment Keywords
# ============================================
PAYMENTS_KEYWORDS=payment,billing,transaction,invoice,refund
BACKEND_KEYWORDS=api,server,database,service,endpoint
FRONTEND_KEYWORDS=ui,page,layout,button,styling,responsive
DEVOPS_KEYWORDS=deploy,infrastructure,kubernetes,docker,ci/cd,pipeline
OPERATIONS_KEYWORDS=monitoring,alert,log,metric,dashboard,uptime

# Default assignment if no keywords match
DEFAULT_TEAM=Operations
DEFAULT_CONFIDENCE=0.75
"""

if __name__ == "__main__":
    try:
        generate_env()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}✗ Cancelled!{Colors.ENDC}\n")
        sys.exit(1)
