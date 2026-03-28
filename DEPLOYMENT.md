# STUAI Production Deployment Guide

Complete step-by-step instructions for deploying STUAI to production environments.

---

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Docker Compose Deployment](#docker-compose-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Deployments](#cloud-deployments)
5. [SSL/TLS Configuration](#ssltls-configuration)
6. [Backup & Recovery](#backup--recovery)
7. [Monitoring & Alerts](#monitoring--alerts)
8. [Troubleshooting](#troubleshooting)
9. [Performance Tuning](#performance-tuning)

---

## Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] Server/Cluster with 4GB+ RAM
- [ ] 20GB+ storage for databases and models
- [ ] Network connectivity to external APIs
- [ ] Backup storage configured
- [ ] Monitoring/logging infrastructure ready

### Credentials Prepared
- [ ] GitHub personal access token (API access)
- [ ] Slack bot token (automation)
- [ ] Jira API token (ticket creation)
- [ ] PagerDuty integration key (incident management)
- [ ] SMTP credentials (email notifications)
- [ ] Database URL (PostgreSQL or RDS)
- [ ] Redis URL (cache/queue)

### Configuration Ready
- [ ] `.env` file created and filled
- [ ] Database backup schedule configured
- [ ] SSL certificates obtained (if needed)
- [ ] Domain name configured (if needed)
- [ ] Firewall rules updated

### Testing Complete
- [ ] All tests passing locally
- [ ] Type checking clean (Pylance)
- [ ] Code reviewed for hardcoded values
- [ ] Security scan performed
- [ ] Load testing conducted

---

## Docker Compose Deployment

### Quick Start (Development/Testing)
```bash
# Clone repository
git clone <repository-url>
cd STUAI

# Create Python environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose up

# Wait for services to initialize
# Then open http://localhost:8000/docs
```

### Production Deployment (with Real Credentials)

#### Step 1: Generate Production Credentials
```bash
# Run interactive credential generator
python generate_production_env.py

# This will prompt you for:
# - Ollama URL (local or remote)
# - GitHub configuration
# - Slack bot setup
# - Database connection details
# - All other integrations

# Creates: .env file with all credentials
```

#### Step 2: Verify Environment
```bash
# Check all services are configured
python config_view.py

# Should show:
# ✓ OLLAMA_HOST configured
# ✓ DATABASE_URL configured
# ✓ REDIS_URL configured
# ✓ GITHUB_TOKEN configured
# ✓ SLACK_BOT_TOKEN configured
# ... etc
```

#### Step 3: Customize Production Settings
```bash
# Edit .env if needed
vi .env

# Optional: Customize docker-compose.prod.yml
# - Adjust replica count
# - Change resource limits
# - Add custom labels/tags
# - Configure specific volumes
```

#### Step 4: Deploy Production Stack
```bash
# Build Docker image (optional, uses latest if skipped)
docker build -t stuai:latest .

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Verify all containers running
docker-compose ps

# Expected output:
# NAME                  STATUS
# stuai-api-1          Up (healthy)
# stuai-api-2          Up (healthy)
# stuai-api-3          Up (healthy)
# stuai-postgres       Up (healthy)
# stuai-redis          Up (healthy)
# stuai-ollama         Up (healthy)
# stuai-pgadmin        Up
```

#### Step 5: Health Verification
```bash
# Check API health
curl http://localhost:8000/health

# Expected response should show all services "up"
# Response:
# {
#   "status": "healthy",
#   "services": {
#     "api": "up",
#     "database": "up",
#     "redis": "up",
#     "ollama": "up"
#   }
# }

# View logs for any errors
docker-compose logs -f api
```

#### Step 6: Test Endpoints
```bash
# Test classification endpoint
curl -X POST http://localhost:8000/ticket \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Service down",
    "description": "Production API not responding",
    "source": "monitoring"
  }'

# Expected response with classification

# Test memory search
curl "http://localhost:8000/memory/search?q=error"

# Test stats
curl "http://localhost:8000/memory/stats?period=24h"
```

#### Step 7: Configure External Integrations

**GitHub Setup:**
```bash
# 1. In GitHub Settings > Developer settings > Personal access tokens
# 2. Generate new token with: repo, admin:repo_hook, admin:org_hook
# 3. Copy token to GITHUB_TOKEN in .env
# 4. Add webhook to repository:
#    URL: http://your-domain.com/github
#    Content type: JSON
#    Events: Issues, Pull requests
# 5. Verify webhook delivery in GitHub UI
```

**Slack Setup:**
```bash
# 1. Go to https://api.slack.com/apps
# 2. Create New App (From scratch)
# 3. Select your workspace
# 4. In OAuth & Permissions:
#    - Add scopes: chat:write, chat:write.public
# 5. Install App to workspace
# 6. Copy Bot Token to SLACK_BOT_TOKEN in .env
# 7. Add bot to channels where you want messages
# 8. Test: python -c "from tools import ExecutionEngine; e = ExecutionEngine(); e.send_alert(('general', 'Test alert from STUAI'))"
```

**Jira Integration:**
```bash
# 1. Go to atlassian.net account settings
# 2. Security > API tokens > Create API token
# 3. Add token to JIRA_API_TOKEN in .env
# 4. Set JIRA_URL and JIRA_EMAIL
# 5. Verify connection: python -c "import requests; ..."
```

**PagerDuty Integration:**
```bash
# 1. Go to PagerDuty > Integrations > Event Rules
# 2. Create integration key
# 3. Add to PAGERDUTY_API_KEY in .env
# 4. Find service ID and add to PAGERDUTY_SERVICE_ID
```

#### Step 8: Setup Monitoring
```bash
# View real-time logs
docker-compose logs -f

# Monitor specific service
docker-compose logs -f api

# Check resource usage
docker stats

# Export logs for analysis
docker-compose logs > logs-$(date +%Y%m%d).txt
```

#### Step 9: Backup Strategy
```bash
# Backup PostgreSQL data
docker-compose exec postgres pg_dump -U stuai stuai_prod > backup-$(date +%Y%m%d).sql

# Backup Redis data
docker-compose exec redis redis-cli SAVE
docker cp stuai-redis:/data/dump.rdb ./redis-backup-$(date +%Y%m%d).rdb

# Verify backups
ls -lh backup-*

# Test restore
psql -U stuai stuai_prod < backup-YYYYMMDD.sql
```

#### Step 10: Daily Operations
```bash
# Check status
docker-compose ps

# View logs for errors
docker-compose logs --tail 100

# Check metrics
curl http://localhost:8000/memory/stats?period=24h

# Restart services if needed
docker-compose restart api

# Graceful shutdown
docker-compose down
```

---

## Kubernetes Deployment

### Prerequisites
```bash
# 1. kubectl installed and configured
# 2. Access to Kubernetes cluster
# 3. Docker image in registry: docker.io/yourusername/stuai:latest
# 4. Persistent volume provisioner available
```

### Step 1: Push Docker Image
```bash
# Build image
docker build -t yourusername/stuai:latest .

# Push to Docker Hub (or your registry)
docker push yourusername/stuai:latest

# Or use your private registry
docker tag stuai:latest your-registry/stuai:latest
docker push your-registry/stuai:latest
```

### Step 2: Create Namespace and Secrets
```bash
# Create namespace
kubectl create namespace stuai

# Create secrets from .env file
kubectl create secret generic stuai-secrets \
  --from-env-file=.env \
  --namespace=stuai

# Verify
kubectl get secrets -n stuai
```

### Step 3: Customize Manifests
```yaml
# Edit k8s-deployment.yaml:
# 1. Change image: stuai:latest → your-registry/stuai:latest
# 2. Update resource limits if needed
# 3. Configure ingress for your domain
# 4. Set replicas initial count
```

### Step 4: Deploy
```bash
# Apply manifest
kubectl apply -f k8s-deployment.yaml

# Monitor deployment progress
kubectl rollout status deployment/stuai-api -n stuai

# Check pods
kubectl get pods -n stuai

# Expected output: 3 pods running (or your configured replicas)
```

### Step 5: Verify Deployment
```bash
# Port forward to test
kubectl port-forward svc/stuai-api 8000:80 -n stuai

# In another terminal, test
curl http://localhost:8000/health

# View logs
kubectl logs -f deployment/stuai-api -n stuai

# Get service details
kubectl get svc stuai-api -n stuai
```

### Step 6: SSL/TLS Setup (See below)

### Step 7: Configure Ingress
```yaml
# Example Ingress (add to k8s-deployment.yaml)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: stuai-ingress
  namespace: stuai
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: stuai-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: stuai-api
            port:
              number: 80
```

### Step 8: Setup HPA Monitoring
```bash
# View autoscaler status
kubectl get hpa -n stuai

# Watch scaling events
kubectl get hpa -n stuai -w

# Check metrics (requires metrics-server)
kubectl top pods -n stuai
```

### Step 9: Backup Strategy
```bash
# Backup PostgreSQL in K8s
kubectl exec -n stuai postgres-pod-name -- \
  pg_dump -U stuai stuai_prod > backup.sql

# Backup persistent volumes
kubectl get pv  # List volumes
kubectl describe pv pv-name

# Use snapshot feature if available
```

### Step 10: Scaling
```bash
# Manual scale
kubectl scale deployment stuai-api --replicas=5 -n stuai

# View HPA status
kubectl get hpa -n stuai

# HPA will auto-scale based on CPU (70%) and memory (80%)
```

---

## Cloud Deployments

### AWS ECS
```bash
# Create ECR repository
aws ecr create-repository --repository-name stuai --region us-east-1

# Push image
docker tag stuai:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/stuai:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/stuai:latest

# Create ECS cluster and task definition
# See AWS documentation for detailed steps
```

### AWS App Runner
```bash
# Deploy from Docker Hub
# Use AWS Console or:
aws apprunner create-service \
  --service-name stuai \
  --source-configuration '{...}' \
  --region us-east-1
```

### Heroku
```bash
# Create Heroku app
heroku create stuai-prod

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0

# Set environment variables
heroku config:set SLACK_BOT_TOKEN=xxx --app stuai-prod

# Deploy
git push heroku main
```

### DigitalOcean App Platform
```bash
# Through console:
# 1. Create new app
# 2. Connect GitHub repository
# 3. Configure PostgreSQL database
# 4. Set environment variables
# 5. Deploy
```

---

## SSL/TLS Configuration

### Let's Encrypt with Docker Compose
```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot certonly --standalone -d api.yourdomain.com

# Update docker-compose to mount certificates
volumes:
  - /etc/letsencrypt:/etc/letsencrypt

# Configure nginx reverse proxy
# See nginx configuration template
```

### Kubernetes with Cert Manager
```bash
# Install cert-manager
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Ingress will automatically get signed certificate
```

---

## Backup & Recovery

### Automated Backups (Cron Job)
```bash
# Create backup script: backup.sh
#!/bin/bash
BACKUP_DIR="/backups/stuai"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup PostgreSQL
docker-compose exec -T postgres pg_dump -U stuai stuai_prod > \
  $BACKUP_DIR/postgres_$DATE.sql

# Backup Redis
docker-compose exec -T redis redis-cli SAVE
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Compress
gzip $BACKUP_DIR/*.sql
gzip $BACKUP_DIR/*.rdb

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR s3://your-backup-bucket/ --recursive

# Clean old backups (keep 30 days)
find $BACKUP_DIR -mtime +30 -delete

# Schedule in crontab
# 0 2 * * * /path/to/backup.sh (runs daily at 2 AM)
```

### Recovery Procedures
```bash
# Restore PostgreSQL
psql -U stuai stuai_prod < postgres_YYYYMMDD.sql

# Or if using Docker:
docker-compose exec -T postgres psql -U stuai stuai_prod < backup.sql

# Restore Redis
docker-compose exec -T redis redis-cli SHUTDOWN
cp redis_YYYYMMDD.rdb /var/lib/redis/dump.rdb
docker-compose restart redis

# Verify restoration
curl http://localhost:8000/health
```

---

## Monitoring & Alerts

### Prometheus + Grafana
```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

### Log Aggregation
```bash
# ELK Stack (Elasticsearch, Logstash, Kibana)
# or
# Datadog/New Relic/CloudWatch

# Configure application logging
# Set LOG_LEVEL=INFO in .env
# All logs go to stdout (captured by Docker)
```

### Health Checks
```bash
# Monitor health endpoint
curl -f http://localhost:8000/health || alert_sysadmin

# Create monitoring rule:
# If health check fails 5 consecutive times → page on-call engineer
```

---

## Troubleshooting

### Common Issues

**Issue: API container keeps restarting**
```bash
# Check logs
docker-compose logs api

# Common causes:
# - DATABASE_URL invalid
# - OLLAMA_HOST unreachable
# - Port 8000 already in use

# Fix:
docker-compose ps
# Kill conflicting process
lsof -i :8000
kill -9 <PID>
```

**Issue: Database connection timeout**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U stuai -c "SELECT 1"

# Check hostname resolution
ping postgres  # From inside docker network

# Verify DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host:port/db
```

**Issue: Ollama model not loading**
```bash
# Pull model
docker-compose exec ollama ollama pull mistral

# Check model list
docker-compose exec ollama ollama list

# Test model inference
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hello"
}'
```

**Issue: Out of memory**
```bash
# Check usage
docker stats

# Increase Docker memory limit
# Update docker-compose resource limits:
# api:
#   deploy:
#     resources:
#       limits:
#         memory: 2G

# Reduce replicas
docker-compose up -d --scale api=1
```

---

## Performance Tuning

### Database Optimization
```sql
-- Create indexes for common queries
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_team ON tickets(assigned_team);
CREATE INDEX idx_tickets_created ON tickets(created_at DESC);

-- Full-text search index
CREATE INDEX idx_tickets_fts ON tickets USING gin(to_tsvector('english', title || ' ' || description));

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM tickets WHERE priority = 'CRITICAL';
```

### Redis Optimization
```bash
# Monitor Redis memory
docker-compose exec redis redis-cli INFO memory

# Configure max memory policy
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Check slow queries
docker-compose exec redis redis-cli CONFIG GET slowlog-log-slower-than
```

### API Performance
```bash
# Configure gunicorn workers
# In docker-compose: 4 workers per CPU core
--workers 4

# Connection pooling (PostgreSQL)
# min_size=5, max_size=20

# Redis connection pool
# redis-py handles automatically

# Load testing
# wrk -t4 -c100 -d30s http://localhost:8000/health
```

---

## Production Checklist

- [ ] All credentials in .env, not hardcoded
- [ ] Database backup schedule running
- [ ] SSL certificates configured and auto-renewing
- [ ] Monitoring and alerting configured
- [ ] Logging aggregation setup
- [ ] Health checks passing
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Team trained on deployment
- [ ] Runbook documented
- [ ] Incident response plan created
- [ ] Disaster recovery tested

---

## Support & Next Steps

1. **Monitoring Dashboard:** Setup Grafana with key metrics
2. **Alert Routing:** Configure PagerDuty for on-call engineers
3. **Documentation:** Keep runbook updated
4. **Training:** Train operations team on STUAI
5. **Optimization:** Continuously monitor and optimize performance

For help: See production_deployment_guide.py or contact team.
