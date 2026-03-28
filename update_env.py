#!/usr/bin/env python3
"""
Interactive .env credential updater for STUAI
Guides user through getting real credentials for all services
"""

import os
from datetime import datetime

COLORS = {
    'GREEN': '\033[92m',
    'BLUE': '\033[94m',
    'YELLOW': '\033[93m',
    'BOLD': '\033[1m',
    'ENDC': '\033[0m',
}

def print_title():
    print(f"\n{COLORS['BOLD']}{'='*70}{COLORS['ENDC']}")
    print(f"{COLORS['BOLD']}🔐 STUAI .env CREDENTIAL CONFIGURATOR{COLORS['ENDC']}")
    print(f"{COLORS['BOLD']}{'='*70}\n{COLORS['ENDC']}")

def get_github_token():
    """Get GitHub token from user."""
    print(f"{COLORS['BLUE']}{COLORS['BOLD']}→ STEP 1: GITHUB TOKEN{COLORS['ENDC']}")
    print(f"  Go to: {COLORS['YELLOW']}https://github.com/settings/personal-access-tokens/new{COLORS['ENDC']}")
    print("  1. Click 'Generate new token (beta)'")
    print("  2. Name: 'STUAI Autonomous Ops'")
    print("  3. Scopes: repo, read:user, user:email")
    print("  4. Generate and COPY token (starts with ghp_)")
    print()
    
    token = input("  Enter GitHub token (or press Enter to skip): ").strip()
    repo = input("  Enter GitHub repo (owner/repo, or press Enter): ").strip() or "your-org/repo"
    
    return token, repo

def get_slack_token():
    """Get Slack bot token from user."""
    print(f"\n{COLORS['BLUE']}{COLORS['BOLD']}→ STEP 2: SLACK BOT TOKEN{COLORS['ENDC']}")
    print(f"  Go to: {COLORS['YELLOW']}https://api.slack.com/apps{COLORS['ENDC']}")
    print("  1. Click 'Create New App' > 'From scratch'")
    print("  2. Name: 'STUAI Autonomous Ops'")
    print("  3. Select your workspace")
    print("  4. Go to 'OAuth & Permissions'")
    print("  5. Add scopes: chat:write, channels:read, users:read")
    print("  6. 'Install to Workspace'")
    print("  7. Copy Bot Token (starts with xoxb-)")
    print()
    
    token = input("  Enter Slack Bot Token (or press Enter to skip): ").strip()
    channel = input("  Enter Slack channel (e.g., #ops, or press Enter): ").strip() or "#ops"
    
    return token, channel

def get_database():
    """Get database URL from user."""
    print(f"\n{COLORS['BLUE']}{COLORS['BOLD']}→ STEP 3: DATABASE (PostgreSQL){COLORS['ENDC']}")
    print("  Options:")
    print("    A) Local: postgresql://postgres:password@localhost:5432/autonomous_ops")
    print("    B) ElephantSQL (Free): https://www.elephantsql.com/")
    print("    C) AWS RDS: https://console.aws.amazon.com/rds/")
    print("    D) Skip (use JSON fallback)")
    print()
    
    choice = input("  Choose option (A/B/C/D, or paste URL): ").strip()
    
    if choice.lower() == 'a':
        return "postgresql://postgres:YOUR_PASSWORD@localhost:5432/autonomous_ops"
    elif choice.lower() == 'b':
        return input("  Paste ElephantSQL connection URL: ").strip()
    elif choice.lower() == 'c':
        return input("  Paste AWS RDS connection URL: ").strip()
    elif choice.lower() == 'd':
        return ""
    else:
        return choice if choice and "://" in choice else ""

def get_optional_services():
    """Get optional service credentials."""
    print(f"\n{COLORS['BLUE']}{COLORS['BOLD']}→ STEP 4: OPTIONAL SERVICES{COLORS['ENDC']}")
    print("  Leave blank to skip\n")
    
    jira_url = input("  Jira URL (e.g., https://yourcompany.atlassian.net): ").strip()
    jira_email = input("  Jira Email: ").strip()
    jira_token = input("  Jira API Token: ").strip()
    
    pagerduty_key = input("  PagerDuty Integration Key: ").strip()
    
    return {
        'jira_url': jira_url,
        'jira_email': jira_email,
        'jira_token': jira_token,
        'pagerduty_key': pagerduty_key,
    }

def create_env_file(github_token, github_repo, slack_token, slack_channel, 
                   database_url, optional):
    """Create and save .env file."""
    
    env_content = f"""# Autonomous Ops Demo Configuration
# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# ============================================
# Ollama Local LLM Configuration
# ============================================
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
OLLAMA_TEMPERATURE=0.3
OLLAMA_TIMEOUT=30

# ============================================
# Priority Classification Keywords
# ============================================
CRITICAL_KEYWORDS=failing,500,down,outage,critical,emergency
HIGH_KEYWORDS=error,bug,issue,broken
MEDIUM_KEYWORDS=slow,performance,degraded
LOW_KEYWORDS=feature,enhancement,improvement

# ============================================
# Team Assignment Keywords
# ============================================
PAYMENTS_KEYWORDS=payment,billing,transaction,invoice
BACKEND_KEYWORDS=api,server,database,service
FRONTEND_KEYWORDS=ui,page,layout,button,styling
DEVOPS_KEYWORDS=deploy,infrastructure,kubernetes,docker,ci/cd
OPERATIONS_KEYWORDS=monitoring,alert,log,metric

DEFAULT_TEAM=Operations
DEFAULT_CONFIDENCE=0.75

# ============================================
# Database Configuration (PostgreSQL)
# ============================================
DATABASE_URL={database_url if database_url else ''}

# ============================================
# Redis Queue Configuration (optional)
# ============================================
REDIS_URL=redis://localhost:6379/0

# ============================================
# Integrations
# ============================================
GITHUB_TOKEN={github_token if github_token else ''}
GITHUB_REPO={github_repo}
SLACK_BOT_TOKEN={slack_token if slack_token else ''}
SLACK_CHANNEL={slack_channel}

# ============================================
# Jira Integration (optional)
# ============================================
JIRA_URL={optional['jira_url'] if optional['jira_url'] else ''}
JIRA_EMAIL={optional['jira_email'] if optional['jira_email'] else ''}
JIRA_API_TOKEN={optional['jira_token'] if optional['jira_token'] else ''}

# ============================================
# PagerDuty Integration (optional)
# ============================================
PAGERDUTY_API_KEY={optional['pagerduty_key'] if optional['pagerduty_key'] else ''}

# ============================================
# API Server Configuration
# ============================================
HOST=0.0.0.0
PORT=8000
DEBUG=True
"""
    
    return env_content

def main():
    """Main function."""
    print_title()
    
    # Collect credentials
    github_token, github_repo = get_github_token()
    slack_token, slack_channel = get_slack_token()
    database_url = get_database()
    optional = get_optional_services()
    
    # Show summary
    print(f"\n{COLORS['GREEN']}{COLORS['BOLD']}✓ SUMMARY{COLORS['ENDC']}")
    print(f"  GitHub: {'✓ Configured' if github_token else '(empty)'}")
    print(f"  Slack: {'✓ Configured' if slack_token else '(empty)'}")
    print(f"  Database: {'✓ Configured' if database_url else 'Will use JSON fallback'}")
    if optional['jira_url']:
        print(f"  Jira: ✓ Configured")
    if optional['pagerduty_key']:
        print(f"  PagerDuty: ✓ Configured")
    
    # Confirm
    print(f"\n{COLORS['BOLD']}Ready to update .env? (y/n): {COLORS['ENDC']}", end="")
    confirm = input().strip().lower()
    
    if confirm == 'y':
        env_content = create_env_file(
            github_token, github_repo, slack_token, slack_channel,
            database_url, optional
        )
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print(f"\n{COLORS['GREEN']}{COLORS['BOLD']}✅ .env file updated successfully!{COLORS['ENDC']}\n")
        
        print(f"{COLORS['BOLD']}✨ Next steps:{COLORS['ENDC']}")
        print("  1. Run: python main.py")
        print("  2. Open: http://localhost:8000")
        print("  3. Test the API!\n")
    else:
        print("\n  Cancelled. No changes made.\n")

if __name__ == "__main__":
    main()
