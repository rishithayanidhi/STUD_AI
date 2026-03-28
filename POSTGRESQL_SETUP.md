# PostgreSQL Setup Guide for Autonomous Ops Demo

## Overview

Your demo now supports **both PostgreSQL and JSON storage**. The system automatically uses PostgreSQL if available, otherwise falls back to JSON.

| Backend        | Pros                                 | Cons                     | Setup Time       |
| -------------- | ------------------------------------ | ------------------------ | ---------------- |
| **PostgreSQL** | Production-ready, scales, enterprise | Requires database setup  | 10-15 min        |
| **JSON**       | Works immediately, no setup          | Not scalable, local only | Already done! ✅ |

---

## Quick Start (If you want PostgreSQL)

### Option 1: Docker (Easiest)

```bash
# Start PostgreSQL in Docker
docker run --name autonomous-ops-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=autonomous_ops \
  -p 5432:5432 \
  -d postgres:15-alpine

# Verify it's running
docker ps

# You should see: autonomous-ops-db with status "Up"
```

Then start your app:

```bash
python run_server.py
```

You should see: `✅ PostgreSQL connected: postgres@localhost:5432/autonomous_ops`

### Option 2: Local PostgreSQL

**Windows:**

1. Download: https://www.postgresql.org/download/windows/
2. Install (keep default port 5432)
3. Create database:
   ```
   psql -U postgres
   CREATE DATABASE autonomous_ops;
   \q
   ```

**macOS:**

```bash
brew install postgresql
brew services start postgresql
psql postgres
CREATE DATABASE autonomous_ops;
\q
```

**Linux:**

```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo sudo -u postgres psql
CREATE DATABASE autonomous_ops;
\q
```

Then:

```bash
python run_server.py
```

### Option 3: Remote/Managed PostgreSQL

Set environment variables:

```bash
export DB_HOST="your-host.com"
export DB_PORT="5432"
export DB_NAME="your-db-name"
export DB_USER="your-username"
export DB_PASSWORD="your-password"
```

Then run:

```bash
python run_server.py
```

---

## Verify PostgreSQL is Running

### Method 1: Check API /stats endpoint

```bash
# While server is running
curl http://localhost:8000/stats

# Response with PostgreSQL:
{
  "status": "running",
  "memory": {
    "total_tickets": 5,
    "storage": "PostgreSQL",
    "backend": "Relational database",
    "priority_distribution": {
      "High": 2,
      "Medium": 3
    }
  },
  "backend": "postgres",
  "database": {
    "dbname": "autonomous_ops",
    "host": "localhost",
    ...
  }
}

# Response with JSON fallback:
{
  "status": "running",
  "memory": {
    "total_tickets": 3,
    "storage": "JSON (file-based)",
    "backend": "Local file system"
  },
  "backend": "json",
  "database": null
}
```

### Method 2: Check server startup

Look for one of these messages:

**PostgreSQL Connected:**

```
✅ PostgreSQL connected: postgres@localhost:5432/autonomous_ops
```

**JSON Fallback (no PostgreSQL):**

```
⚠️  psycopg2 not installed. Using JSON file fallback.
   To use PostgreSQL: pip install psycopg2-binary
```

Or:

```
⚠️  PostgreSQL connection failed: could not connect to server
   Using JSON file fallback instead
```

---

## Environment Variables

### Defaults (work out of the box)

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=autonomous_ops
DB_USER=postgres
DB_PASSWORD=postgres
```

### Set Custom Values

**Linux/macOS (.bashrc, .zshrc):**

```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="autonomous_ops"
export DB_USER="postgres"
export DB_PASSWORD="postgres"

source ~/.bashrc  # or ~/.zshrc
```

**Windows PowerShell:**

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="autonomous_ops"
$env:DB_USER="postgres"
$env:DB_PASSWORD="postgres"
```

**Windows Command Prompt (permanently):**

```
setx DB_HOST localhost
setx DB_PORT 5432
setx DB_NAME autonomous_ops
setx DB_USER postgres
setx DB_PASSWORD postgres
```

Then restart Command Prompt and run:

```bash
python run_server.py
```

---

## What Gets Stored in PostgreSQL

### Tickets Table

```
ticket_id    : VARCHAR(255)          - Unique ticket identifier
issue        : TEXT                  - Issue description
priority     : VARCHAR(50)           - High/Medium/Low
category     : VARCHAR(50)           - Incident/Request/etc
team         : VARCHAR(255)          - Assigned team
confidence   : FLOAT                 - AI confidence (0.0-1.0)
decision     : JSONB                 - Full decision JSON
created_at   : TIMESTAMP             - When ticket was created
updated_at   : TIMESTAMP             - Last update time
```

### Actions Log Table

```
ticket_id    : VARCHAR(255)          - References tickets table
action       : VARCHAR(255)          - Action name
status       : VARCHAR(50)           - success/failure
details      : TEXT                  - Action details
created_at   : TIMESTAMP             - When action was taken
```

---

## Troubleshooting

### "psycopg2 not installed"

Solution:

```bash
pip install psycopg2-binary
python run_server.py
```

### "could not connect to server"

Check:

1. **Is PostgreSQL running?**

   ```
   docker ps  # if using Docker

   # Or check service status:
   # Windows: Services → PostgreSQL
   # Mac: brew services list
   # Linux: systemctl status postgresql
   ```

2. **Is the database created?**

   ```
   psql -U postgres -l
   # Should list: autonomous_ops
   ```

3. **Are environment variables set?**

   ```
   echo $DB_HOST $DB_PORT $DB_NAME $DB_USER
   ```

4. **Can you connect manually?**
   ```
   psql -h localhost -U postgres -d autonomous_ops
   ```

### "dial tcp 127.0.0.1:5432: connect: connection refused"

The database isn't running. Start it:

**Docker:**

```bash
docker start autonomous-ops-db
```

**macOS (Homebrew):**

```bash
brew services start postgresql
```

**Linux (systemd):**

```bash
sudo systemctl start postgresql
```

**Windows (Services):**

- Search "Services" → Find "PostgreSQL Database Server" → Right-click → Start

---

## FAQ

**Q: What if I switch between PostgreSQL and JSON?**  
A: No problem! Both backends read from JSON as fallback, so data is never lost.

**Q: Will the demo judges see a difference?**  
A: No, the UI is identical. But `/stats` endpoint shows the backend being used.

**Q: What if PostgreSQL goes down?**  
A: System automatically falls back to JSON. Demo continues working!

**Q: Can I switch databases mid-demo?**  
A: Yes. Stop the server, change DB\_\* environment variables, restart. New backend used.

**Q: How much data can PostgreSQL store?**  
A: Gigabytes without issue. JSON file: megabytes practical limit.

**Q: Do I need to manually create tables?**  
A: No! Tables are auto-created on first connection.

---

## For The Demo

Show judges the `/stats` endpoint to prove production-grade architecture:

```bash
curl http://localhost:8000/stats | jq
```

Shows:

- ✅ PostgreSQL backend active
- ✅ Tickets stored in database
- ✅ Analytics available (priority distribution, etc.)

This impresses judges more than JSON storage! 🚀

---

## Need Help?

Run the setup script:

```bash
python setup_postgres.py
```

It will guide you through interactive setup.
