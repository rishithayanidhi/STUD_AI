#!/usr/bin/env python
"""
Guide to Get Real Links, Tokens, and Credentials
Complete step-by-step instructions for all services
"""

def print_guide():
    guide = """
╔════════════════════════════════════════════════════════════════════╗
║        HOW TO GET REAL LINKS & CREDENTIALS FOR ALL SERVICES       ║
╚════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════
1️⃣  OLLAMA (Local LLM - Free, No Credentials Needed)
═══════════════════════════════════════════════════════════════════════

✓ Default Link (localhost):  http://localhost:11434
✓ Status URL:                http://localhost:11434/api/tags

How to verify it's running:
  curl http://localhost:11434/api/tags

If you want to run on a different machine:

  Remote Server Setup:
    1. SSH into your server
    2. docker run -d -p 11434:11434 ollama/ollama
    3. docker exec ollama ollama pull llama3
    4. Get server IP: hostname -I
    5. Use in .env: OLLAMA_URL=http://YOUR_SERVER_IP:11434

Example with real server IP:
    OLLAMA_URL=http://192.168.1.100:11434


═══════════════════════════════════════════════════════════════════════
2️⃣  GITHUB API (Get Personal Access Token)
═══════════════════════════════════════════════════════════════════════

🔗 Step 1: Generate Personal Access Token
   URL: https://github.com/settings/personal-access-tokens/new

   OR Alternative (classic token):
   URL: https://github.com/settings/tokens

🔐 Step 2: Follow these steps:
   1. Go to https://github.com/settings/personal-access-tokens/new
   2. Click "Generate new token"
   3. Name it: "STUAI Autonomous Ops"
   4. Select Expiration: 90 days (or your preference)
   5. Select Scopes:
      ✓ repo (Full control of private/public repos)
      ✓ read:user (Read user profile)
      ✓ user:email (Read user email)
   6. Click "Generate token"
   7. COPY THE TOKEN - you won't see it again!

💾 Add to .env:
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   GITHUB_REPO=your-username/your-repo-name

🧪 Test it:
   curl -H "Authorization: token YOUR_TOKEN" \\
        https://api.github.com/user

Example Response:
   {
     "login": "your-username",
     "id": 12345,
     "name": "Your Name"
   }


═══════════════════════════════════════════════════════════════════════
3️⃣  SLACK BOT (Get Slack Bot Token)
═══════════════════════════════════════════════════════════════════════

🔗 Step 1: Create Slack App
   URL: https://api.slack.com/apps

🔐 Step 2: Create new app
   1. Click "Create New App"
   2. Choose "From scratch"
   3. App Name: "STUAI Autonomous Ops"
   4. Select your workspace
   5. Click "Create App"

🔐 Step 3: Configure Bot Token Scopes
   Left menu → Click "OAuth & Permissions"
   Under "Scopes" → "Bot Token Scopes"
   Add these scopes:
     ✓ chat:write       (Post messages)
     ✓ channels:read    (View channels)
     ✓ users:read       (View users)
     ✓ team:read        (View team info)

🔐 Step 4: Install to Workspace
   Click "Install to Workspace"
   Accept permissions

🔐 Step 5: Get Bot Token
   Copy "Bot User OAuth Token" (starts with xoxb-)

💾 Add to .env:
   SLACK_BOT_TOKEN=xoxb-1234567890-abcdefghijk-xxxxxxxxxxxxx
   SLACK_CHANNEL=#ops

🧪 Test it:
   curl -X POST https://slack.com/api/auth.test \\
     -H "Authorization: Bearer xoxb-..." \\
     -H "Content-Type: application/x-www-form-urlencoded"

💡 Finding your channel ID:
   1. Go to Slack workspace
   2. Right-click channel → Copy link
   3. Extract channel ID from URL: slack.com/archives/C123XXXXX


═══════════════════════════════════════════════════════════════════════
4️⃣  POSTGRESQL (Database - Local or Cloud)
═══════════════════════════════════════════════════════════════════════

Option A: Local Database (Recommended for Dev)
──────────────────────────────────
  docker run -d -p 5432:5432 \\
    -e POSTGRES_PASSWORD=your_password \\
    -e POSTGRES_DB=autonomous_ops \\
    postgres:15

  DATABASE_URL=postgresql://postgres:your_password@localhost:5432/autonomous_ops

Option B: AWS RDS (Production)
──────────────────────────────────
  1. Go to https://console.aws.amazon.com/rds/
  2. Click "Create database"
  3. Engine: PostgreSQL
  4. DB instance identifier: autonomous-ops-db
  5. Master username: admin
  6. Master password: (choose strong password)
  7. Storage: 20 GB (free tier)
  8. Public accessibility: Yes
  9. Create database (wait 5-10 minutes)
  10. Copy endpoint from Database details

  DATABASE_URL=postgresql://admin:PASSWORD@autonomous-ops-db.xxxxx.us-east-1.rds.amazonaws.com:5432/autonomous_ops

Option C: ElephantSQL (Simple & Free)
──────────────────────────────────
  1. Go to https://www.elephantsql.com/
  2. Sign up (free tier available)
  3. Create instance
  4. Copy URL from dashboard

  DATABASE_URL=postgresql://lvzzxabc:xyz@otto.db.elephantsql.com:5432/lvzzxabc

🧪 Test connection:
   psql "postgresql://user:password@localhost:5432/autonomous_ops"


═══════════════════════════════════════════════════════════════════════
5️⃣  REDIS (Message Queue - Optional)
═══════════════════════════════════════════════════════════════════════

Option A: Local Redis (Dev)
──────────────────────────────────
  docker run -d -p 6379:6379 redis:7

  REDIS_URL=redis://localhost:6379/0

Option B: Redis Cloud (Free & Cloud)
──────────────────────────────────
  1. Go to https://redis.com/try-free/
  2. Sign up (free tier: 30MB)
  3. Create database
  4. Copy connection URL

  REDIS_URL=redis://:PASSWORD@xxxxx.redis.cloud.com:12345

Option C: AWS ElastiCache
──────────────────────────────────
  1. Go to https://console.aws.amazon.com/elasticache/
  2. Create Redis cluster
  3. Copy endpoint

  REDIS_URL=redis://node.xxxxx.ng.0001.use1.cache.amazonaws.com:6379

🧪 Test connection:
   redis-cli -u redis://localhost:6379/0 ping


═══════════════════════════════════════════════════════════════════════
6️⃣  JIRA CLOUD (Ticket Creation - Optional)
═══════════════════════════════════════════════════════════════════════

🔗 Step 1: Get API Token
   URL: https://id.atlassian.com/manage-profile/security/api-tokens

🔐 Step 2: Create API Token
   1. Click "Create API token"
   2. Name it: "STUAI Autonomous Ops"
   3. Click "Create"
   4. COPY THE TOKEN

💾 Add to .env:
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_USERNAME=your-email@company.com
   JIRA_API_TOKEN=ATATT3xFfGxxxxxxxxxxxx

🧪 Test it:
   curl -u EMAIL:TOKEN https://your-domain.atlassian.net/rest/api/3/issue

Example:
   curl -u john@company.com:ATATT3xFf... \\
        https://my-company.atlassian.net/rest/api/3/issue


═══════════════════════════════════════════════════════════════════════
7️⃣  PAGERDUTY (Incident Management - Optional)
═══════════════════════════════════════════════════════════════════════

🔗 Step 1: Get Integration Key
   URL: https://www.pagerduty.com/

🔐 Step 2: Create Service & Integration
   1. Log in to PagerDuty dashboards
   2. Go to Services
   3. Create new service
   4. Add "Events API v2" integration
   5. Copy Integration Key

💾 Add to .env:
   PAGERDUTY_INTEGRATION_KEY=xxxxxxxxxxxxx

🧪 Test it:
   curl -X POST https://events.pagerduty.com/v2/enqueue \\
     -H 'Content-Type: application/json' \\
     -d '{
       "routing_key":"YOUR_KEY",
       "event_action":"trigger",
       "dedup_key":"test-event",
       "payload":{
         "summary":"Test event",
         "severity":"error",
         "source":"STUAI"
       }
     }'


═══════════════════════════════════════════════════════════════════════
8️⃣  SMTP EMAIL (Optional for Alerts)
═══════════════════════════════════════════════════════════════════════

Option A: Gmail
──────────────────────────────────
  1. Go to myaccount.google.com
  2. Security → 2-Step Verification (enable if not already)
  3. App passwords (search for this)
  4. Select "Mail" and "Windows Computer"
  5. Copy the 16-character password

  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=your-email@gmail.com
  SMTP_PASSWORD=xxxx xxxx xxxx xxxx (16 chars)

Option B: Sendgrid (Free tier: 100 emails/day)
──────────────────────────────────
  1. Go to https://signup.sendgrid.com/
  2. Create account (free tier available)
  3. Create API key
  4. Save API key

  SMTP_SERVER=smtp.sendgrid.net
  SMTP_PORT=587
  SMTP_USERNAME=apikey
  SMTP_PASSWORD=SG.your_api_key_xxxxx

Option C: Office 365
──────────────────────────────────
  SMTP_SERVER=smtp.office365.com
  SMTP_PORT=587
  SMTP_USERNAME=your-email@company.com
  SMTP_PASSWORD=your_password

🧪 Test it:
   python -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('email', 'password')
   print('✓ Connected!')
   "


═══════════════════════════════════════════════════════════════════════
COMPLETE EXAMPLE .env FILE
═══════════════════════════════════════════════════════════════════════

# Ollama (localhost)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# GitHub (real token)
GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwx
GITHUB_REPO=my-username/my-repo

# Slack (real token)
SLACK_BOT_TOKEN=xoxb-1234567890-abcdefghijk-xxxxxxxxxxxxxx
SLACK_CHANNEL=#ops

# Database (remote)
DATABASE_URL=postgresql://admin:password@autonomous-ops-db.xxxxx.us-east-1.rds.amazonaws.com:5432/autonomous_ops

# Redis (cloud)
REDIS_URL=redis://:password@xxxxx.redis.cloud.com:12345

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx

# Jira
JIRA_URL=https://my-company.atlassian.net
JIRA_USERNAME=your-email@company.com
JIRA_API_TOKEN=ATATT3xFfxxxxxxxxxxxxxxx

# PagerDuty
PAGERDUTY_INTEGRATION_KEY=xxxxxxxxxxxxx


═══════════════════════════════════════════════════════════════════════
⚡ QUICK CHECKLIST: Which Links Do I Need?
═══════════════════════════════════════════════════════════════════════

Minimum Setup (Works Offline):
  ✓ OLLAMA_URL (localhost)
  ✓ OLLAMA_MODEL
  → JSON storage, no database needed

Standard Setup:
  ✓ All above
  ✓ DATABASE_URL (PostgreSQL)
  ✓ Default keywords in .env

Production Setup:
  ✓ All above
  ✓ GITHUB_TOKEN + GITHUB_REPO
  ✓ SLACK_BOT_TOKEN + SLACK_CHANNEL
  ✓ REDIS_URL (cloud or local)
  ✓ JIRA_* (optional)
  ✓ PAGERDUTY_* (optional)
  ✓ SMTP_* (optional)


═══════════════════════════════════════════════════════════════════════
🚀 QUICK SETUP COMMANDS
═══════════════════════════════════════════════════════════════════════

1. Copy example to .env:
   cp .env.example .env

2. Edit .env with your real credentials:
   nano .env      # Linux/Mac
   notepad .env   # Windows

3. View what's configured:
   python show_all_links.py

4. Check current config:
   python config_view.py

5. Start system:
   python quick_start.py


═══════════════════════════════════════════════════════════════════════
🔒 SECURITY TIPS
═══════════════════════════════════════════════════════════════════════

✓ Never commit .env file (already in .gitignore)
✓ Keep tokens secret - don't share them
✓ Rotate tokens/passwords regularly
✓ Use strong passwords for databases
✓ Use environment variables for all secrets
✓ Test tokens before deploying to production
✓ Set token expiration dates where possible
✓ Create separate tokens for dev/staging/prod


═══════════════════════════════════════════════════════════════════════
📞 HOW TO TEST EACH LINK
═══════════════════════════════════════════════════════════════════════

Ollama:
  curl http://localhost:11434/api/tags

FastAPI:
  curl http://localhost:8000/health

GitHub:
  curl -H "Authorization: token YOUR_TOKEN" \\
       https://api.github.com/user

Slack:
  curl -H "Authorization: Bearer YOUR_TOKEN" \\
       https://slack.com/api/auth.test

PostgreSQL:
  psql "postgresql://user:password@host:5432/db"

Redis:
  redis-cli -u redis://localhost:6379/0 ping


═══════════════════════════════════════════════════════════════════════

Ready? Let's go!

1. Get your real links from guides above
2. Edit .env file with credentials
3. Run: python show_all_links.py
4. Start: python quick_start.py

Questions? Check individual service documentation!
    """
    print(guide)

if __name__ == "__main__":
    print_guide()
