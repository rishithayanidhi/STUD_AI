#!/usr/bin/env python3
"""
STUAI Production Deployment Complete Guide
==========================================

This comprehensive guide walks through every step from zero to production deployment.
Run this guide first to understand the complete workflow, then follow specific paths.

Usage: python production_deployment_guide.py
"""

import os
import sys
from datetime import datetime

COLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

def print_section(title, level=1):
    """Print a formatted section title."""
    if level == 1:
        print(f"\n{COLORS['HEADER']}{COLORS['BOLD']}{'='*70}{COLORS['ENDC']}")
        print(f"{COLORS['HEADER']}{COLORS['BOLD']}{title}{COLORS['ENDC']}")
        print(f"{COLORS['HEADER']}{COLORS['BOLD']}{'='*70}{COLORS['ENDC']}\n")
    else:
        print(f"\n{COLORS['OKCYAN']}{COLORS['BOLD']}→ {title}{COLORS['ENDC']}\n")

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"{COLORS['OKBLUE']}{COLORS['BOLD']}[Step {step_num}]{COLORS['ENDC']} {description}")

def print_success(message):
    """Print success message."""
    print(f"{COLORS['OKGREEN']}✓ {message}{COLORS['ENDC']}")

def print_warning(message):
    """Print warning message."""
    print(f"{COLORS['WARNING']}⚠️  {message}{COLORS['ENDC']}")

def print_info(message):
    """Print info message."""
    print(f"{COLORS['OKCYAN']}ℹ️  {message}{COLORS['ENDC']}")

def get_deployment_path():
    """Get user's preferred deployment path."""
    print_section("Deployment Path Selection", 2)
    print("Choose your deployment method:\n")
    print(f"{COLORS['OKBLUE']}1{COLORS['ENDC']} - Docker Compose (Local/Single Server)")
    print(f"{COLORS['OKBLUE']}2{COLORS['ENDC']} - Kubernetes (Cloud/Multi-Server)")
    print(f"{COLORS['OKBLUE']}3{COLORS['ENDC']} - Manual Setup (Advanced)")
    print(f"{COLORS['OKBLUE']}4{COLORS['ENDC']} - View Full Guide")
    
    choice = input(f"\n{COLORS['BOLD']}Select option (1-4): {COLORS['ENDC']}").strip()
    return choice

def deployment_overview():
    """Display complete deployment architecture overview."""
    print_section("Architecture Overview")
    
    print(f"{COLORS['BOLD']}System Components:{COLORS['ENDC']}")
    print("""
    ┌─────────────────────────────────────────────────────────┐
    │                     STUAI Architecture                   │
    ├─────────────────────────────────────────────────────────┤
    │                                                           │
    │  🌐 Load Balancer / Reverse Proxy                        │
    │      ↓                                                    │
    │  📡 FastAPI Server (3+ replicas)                         │
    │      ├─ POST /ticket          → agent.py                │
    │      ├─ GET /health           → Status check            │
    │      ├─ GET /memory/*         → Storage query          │
    │      ├─ GET /stats            → Analytics              │
    │      └─ WS /ws                → Real-time updates      │
    │      ↓                                                    │
    │  ┌─────────────────────────────────────────────┐         │
    │  │          Agent Processing Layer              │         │
    │  │ ┌───────────────────────────────────────┐   │         │
    │  │ │ agent.py - Ticket Classification      │   │         │
    │  │ │ • Ollama/Mistral LLM Integration      │   │         │
    │  │ │ • Keywords: CRITICAL/HIGH/MEDIUM/LOW  │   │         │
    │  │ │ • Team Assignment (5 teams)           │   │         │
    │  │ │ • Priority scoring                    │   │         │
    │  │ │ • Fallback mock mode                  │   │         │
    │  │ └───────────────────────────────────────┘   │         │
    │  │ ┌───────────────────────────────────────┐   │         │
    │  │ │ tools.py - Execution Engine            │   │         │
    │  │ │ • Mock tool implementations            │   │         │
    │  │ │ • Real API integrations ready:         │   │         │
    │  │ │   - GitHub API                         │   │         │
    │  │ │   - Slack SDK                          │   │         │
    │  │ │   - Jira Cloud                         │   │         │
    │  │ │   - PagerDuty API                      │   │         │
    │  │ │   - SMTP (Email)                       │   │         │
    │  │ │   - Custom Webhooks                    │   │         │
    │  │ │ • Logging & auditing                   │   │         │
    │  │ └───────────────────────────────────────┘   │         │
    │  └─────────────────────────────────────────────┘         │
    │      ↓                                                    │
    │  ┌─────────────────────────────────────────────┐         │
    │  │       Infrastructure Services               │         │
    │  │                                              │         │
    │  │  🦙 Ollama                                  │         │
    │  │     • Mistral 7B / Llama3 (local)           │         │
    │  │     • 11434 port                            │         │
    │  │     • 0 latency, 100% privacy               │         │
    │  │                                              │         │
    │  │  🐘 PostgreSQL                              │         │
    │  │     • Primary data store                    │         │
    │  │     • Full-text search indexes              │         │
    │  │     • 5432 port                             │         │
    │  │                                              │         │
    │  │  🔴 Redis                                   │         │
    │  │     • Caching & queue layer                 │         │
    │  │     • Session management                    │         │
    │  │     • 6379 port                             │         │
    │  │                                              │         │
    │  │  🔍 ChromaDB                                │         │
    │  │     • Vector embeddings                     │         │
    │  │     • Semantic search                       │         │
    │  │     • Optional vector ops                   │         │
    │  │                                              │         │
    │  │  📊 PostgreSQL on AWS RDS (Recommended)     │         │
    │  │     • Managed PostgreSQL                    │         │
    │  │     • Automatic backups                     │         │
    │  │     • Multi-AZ redundancy                   │         │
    │  │                                              │         │
    │  └─────────────────────────────────────────────┘         │
    │      ↓                                                    │
    │  ┌─────────────────────────────────────────────┐         │
    │  │       External Integrations (Real APIs)      │         │
    │  │                                              │         │
    │  │  ✓ GitHub           (Webhooks + REST)       │         │
    │  │  ✓ Slack            (Bot + Events)          │         │
    │  │  ✓ Jira Cloud       (REST API)              │         │
    │  │  ✓ PagerDuty        (Events/Incidents)      │         │
    │  │  ✓ Email            (SMTP)                  │         │
    │  │  ✓ Custom Webhooks  (HTTP POST)             │         │
    │  │                                              │         │
    │  └─────────────────────────────────────────────┘         │
    │                                                           │
    └─────────────────────────────────────────────────────────┘
    """)

def docker_compose_path():
    """Docker Compose deployment path."""
    print_section("Docker Compose Deployment Path")
    
    steps = [
        ("Prepare environment", [
            "Ensure Docker & Docker Compose installed",
            "Check /docker-compose.prod.yml exists",
            "Review .env template settings"
        ]),
        ("Generate production credentials", [
            "Run: python generate_production_env.py",
            "Interactive prompts for all services",
            "Creates production .env file"
        ]),
        ("Build Docker image (optional)", [
            "Run: make docker-build",
            "OR: docker build -t stuai:latest .",
            "Tags image for local registry"
        ]),
        ("Start production stack", [
            "Run: make prod-deploy",
            "OR: docker-compose -f docker-compose.prod.yml up -d",
            "Starts all 5 services with health checks"
        ]),
        ("Verify deployment", [
            "Check health: curl http://localhost:8000/health",
            "View API docs: http://localhost:8000/docs",
            "Monitor logs: docker-compose logs -f api"
        ]),
        ("Configure integrations", [
            "GitHub: Add Webhook at /github",
            "Slack: Install bot and get token",
            "Email: Verify SMTP credentials",
            "External APIs: Test with real tokens"
        ]),
        ("Test end-to-end", [
            "Send test ticket: POST /ticket",
            "Verify classification works",
            "Check database storage",
            "Confirm tool execution logs"
        ]),
    ]
    
    for step_num, (description, details) in enumerate(steps, 1):
        print_step(step_num, description)
        for detail in details:
            print(f"  • {detail}")

def kubernetes_path():
    """Kubernetes deployment path."""
    print_section("Kubernetes Deployment Path")
    
    steps = [
        ("Prerequisites", [
            "kubectl configured and connected to cluster",
            "Docker image pushed to Docker Hub: yourusername/stuai:latest",
            "k8s-deployment.yaml reviewed and customized",
            "Cluster resource availability: 3GB RAM, 2 CPUs minimum"
        ]),
        ("Create namespace and secrets", [
            "Run: kubectl create namespace stuai",
            "Create secrets: kubectl create secret generic stuai-secrets \\",
            "  --from-env-file=.env --namespace=stuai",
            "Verify: kubectl get secrets -n stuai"
        ]),
        ("Deploy services", [
            "Apply manifest: kubectl apply -f k8s-deployment.yaml",
            "Verify deployment: kubectl get deployments -n stuai",
            "Check pods: kubectl get pods -n stuai",
            "Wait for ready: kubectl rollout status deployment/stuai-api -n stuai"
        ]),
        ("Access the service", [
            "Port forward (local): kubectl port-forward svc/stuai-api 8000:80 -n stuai",
            "OR use LoadBalancer: kubectl get svc stuai-api -n stuai",
            "API available at: http://localhost:8000"
        ]),
        ("Monitor and scale", [
            "View logs: kubectl logs -f deployment/stuai-api -n stuai",
            "Manual scale: kubectl scale deployment stuai-api --replicas=5 -n stuai",
            "HPA handles auto-scaling (3-10 replicas)",
            "Monitor metrics: kubectl top pods -n stuai"
        ]),
        ("SSL/TLS setup", [
            "Install cert-manager: helm install cert-manager ...",
            "Create Certificate resource in manifest",
            "Setup Ingress with TLS termination",
            "Configure DNS for domain"
        ]),
    ]
    
    for step_num, (description, details) in enumerate(steps, 1):
        print_step(step_num, description)
        for detail in details:
            print(f"  • {detail}")

def manual_setup_path():
    """Manual deployment path."""
    print_section("Manual Setup Path (Advanced)")
    
    print(f"{COLORS['WARNING']}⚠️  This path requires manual configuration. Recommended only for learning.{COLORS['ENDC']}\n")
    
    steps = [
        ("Install system dependencies", [
            "Ubuntu: sudo apt-get install python3.11 postgresql redis-server",
            "macOS: brew install python@3.11 postgresql redis",
            "Windows: Download installers from official websites"
        ]),
        ("Start infrastructure services", [
            "PostgreSQL: pg_ctl start",
            "Redis: redis-server --daemonize yes",
            "Ollama: ollama serve (in separate terminal)"
        ]),
        ("Setup Python environment", [
            "Create venv: python3.11 -m venv venv",
            "Activate: source venv/bin/activate (or venv\\Scripts\\activate on Windows)",
            "Install: pip install -r requirements.txt"
        ]),
        ("Setup database", [
            "Run: python quick_postgres.py",
            "Creates stuai_dev database",
            "Creates required tables via memory.py"
        ]),
        ("Create .env file", [
            "Copy from .env.example",
            "Edit with local service URLs",
            "All infrastructure on localhost:*"
        ]),
        ("Start STUAI API", [
            "Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000",
            "Open: http://localhost:8000/docs",
            "Test endpoints directly"
        ]),
        ("Manual integration setup", [
            "GitHub: Generate personal access token",
            "Slack: Create bot and copy token",
            "Jira: Generate API token for account",
            "PagerDuty: Create integration key"
        ]),
    ]
    
    for step_num, (description, details) in enumerate(steps, 1):
        print_step(step_num, description)
        for detail in details:
            print(f"  • {detail}")

def production_readiness_checklist():
    """Display production readiness checklist."""
    print_section("Production Readiness Checklist")
    
    checklist = {
        "Environment & Configuration": [
            "□ .env file created with all required variables",
            "□ No hardcoded values in Python files",
            "□ Sensitive data in environment variables only",
            "□ Separate .env files for dev/staging/production"
        ],
        "Database & Storage": [
            "□ PostgreSQL running and accessible",
            "□ Database backup strategy configured",
            "□ Connection pooling optimized",
            "□ Database migrations applied",
            "□ Indexes created for performance"
        ],
        "API & Services": [
            "□ FastAPI health check responding",
            "□ All endpoints returning correct responses",
            "□ Error handling comprehensive",
            "□ Logging configured and working",
            "□ Rate limiting implemented"
        ],
        "External Integrations": [
            "□ GitHub token verified and working",
            "□ Slack bot token installed",
            "□ Jira API authentication tested",
            "□ PagerDuty integration configured",
            "□ SMTP credentials verified"
        ],
        "Deployment & Infrastructure": [
            "□ Docker image built successfully",
            "□ Docker Compose (or Kubernetes) manifest reviewed",
            "□ Health checks configured",
            "□ Resource limits set appropriately",
            "□ Backup and recovery tested"
        ],
        "Security": [
            "□ No credentials in version control",
            "□ HTTPS/TLS configured",
            "□ Authentication implemented",
            "□ Input validation comprehensive",
            "□ Rate limiting and DDoS protection"
        ],
        "Monitoring & Logging": [
            "□ Log aggregation configured",
            "□ Performance metrics collection",
            "□ Error alerting configured",
            "□ Monitoring dashboard created",
            "□ SLOs/SLIs defined"
        ],
        "Testing & Validation": [
            "□ Unit tests passing",
            "□ Integration tests passing",
            "□ Load testing performed",
            "□ Security scanning completed",
            "□ End-to-end test successful"
        ],
    }
    
    for category, items in checklist.items():
        print(f"{COLORS['BOLD']}{category}:{COLORS['ENDC']}")
        for item in items:
            print(f"  {item}")
        print()

def troubleshooting_guide():
    """Display common troubleshooting scenarios."""
    print_section("Troubleshooting Guide")
    
    issues = {
        "API not responding": [
            "Check: curl http://localhost:8000/health",
            "View logs: docker-compose logs api",
            "Verify DATABASE_URL is correct",
            "Check Ollama is running: curl http://localhost:11434/api/tags"
        ],
        "Database connection error": [
            "Check PostgreSQL running: psql -U stuai -d stuai_prod -c 'SELECT 1;'",
            "Verify DATABASE_URL in .env",
            "Check password is correct",
            "Ensure database exists: createdb stuai_prod"
        ],
        "Ollama model not found": [
            "Pull model: ollama pull mistral",
            "Verify: ollama list",
            "Check OLLAMA_HOST is correct",
            "Restart Ollama: ollama serve"
        ],
        "Redis connection failed": [
            "Check Redis running: redis-cli ping",
            "Verify REDIS_HOST and REDIS_PORT",
            "Check password if configured",
            "Restart Redis: redis-server"
        ],
        "GitHub webhook not working": [
            "Verify webhook URL is public",
            "Check GitHub has correct token",
            "Monitor logs for webhook payloads",
            "Ensure /github endpoint is configured"
        ],
        "Out of memory": [
            "Increase Docker memory limit",
            "Reduce replica count: docker-compose down && docker-compose up -d",
            "Check for memory leaks in logs",
            "Upgrade infrastructure resources"
        ],
    }
    
    for issue, solutions in issues.items():
        print(f"{COLORS['WARNING']}{issue}:{COLORS['ENDC']}")
        for solution in solutions:
            print(f"  → {solution}")
        print()

def show_helpful_commands():
    """Display helpful commands."""
    print_section("Helpful Commands Reference")
    
    commands = {
        "Development": [
            ("make dev", "Start FastAPI in dev mode with auto-reload"),
            ("make test", "Run test suite with coverage report"),
            ("python config_view.py", "View current configuration"),
            ("python show_all_links.py", "Show all service URLs"),
        ],
        "Docker": [
            ("make docker-up", "Start Docker Compose stack"),
            ("make docker-down", "Stop Docker Compose stack"),
            ("make docker-logs", "View live Docker logs"),
            ("make prod-deploy", "Deploy production stack"),
        ],
        "Database": [
            ("python quick_postgres.py", "Quick PostgreSQL setup"),
            ("python setup_postgres.py", "Full PostgreSQL configuration"),
            ("psql stuai_prod", "Connect to database directly"),
        ],
        "Credentials": [
            ("python generate_production_env.py", "Interactive credential generator"),
            ("python GET_REAL_LINKS.py", "Show all credential links"),
        ],
        "Health Checks": [
            ("curl http://localhost:8000/health", "Check API health"),
            ("docker-compose ps", "View service status"),
            ("docker-compose logs -f", "Stream all logs"),
        ],
    }
    
    for category, cmd_list in commands.items():
        print(f"{COLORS['BOLD']}{category}:{COLORS['ENDC']}")
        for cmd, description in cmd_list:
            print(f"  {COLORS['OKCYAN']}{cmd}{COLORS['ENDC']}")
            print(f"    → {description}\n")

def next_steps():
    """Display next steps based on deployment choice."""
    print_section("Next Steps")
    
    print(f"{COLORS['OKGREEN']}{COLORS['BOLD']}🚀 Your STUAI Production Deployment Journey{COLORS['ENDC']}\n")
    
    steps = [
        "1. Choose your deployment method above (Docker Compose or Kubernetes)",
        "2. Run interactive credential generator: python generate_production_env.py",
        "3. Review and customize your configuration",
        "4. Deploy to your chosen environment",
        "5. Verify health checks and service connectivity",
        "6. Configure external integrations (GitHub, Slack, etc.)",
        "7. Run end-to-end tests with real data",
        "8. Setup monitoring and alerting",
        "9. Document your specific deployment",
        "10. Keep your .env secure and backed up"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n{COLORS['OKBLUE']}💡 For detailed guides on specific integrations, see:{{COLORS['ENDC']}}")
    print(f"   • generate_production_env.py - Interactive setup")
    print(f"   • GET_REAL_LINKS.py - All service links with credentials")
    print(f"   • show_all_links.py - Quick reference for all URLs")
    print(f"   • Makefile - Common commands reference\n")

def main():
    """Main guide flow."""
    print(f"\n{COLORS['HEADER']}{COLORS['BOLD']}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           STUAI Production Deployment Complete Guide️              ║")
    print("║              From Development to Production Ready                   ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{COLORS['ENDC']}")
    
    print_info(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    deployment_overview()
    
    while True:
        choice = get_deployment_path()
        
        if choice == "1":
            docker_compose_path()
            break
        elif choice == "2":
            kubernetes_path()
            break
        elif choice == "3":
            manual_setup_path()
            break
        elif choice == "4":
            production_readiness_checklist()
            print()
            troubleshooting_guide()
            print()
            show_helpful_commands()
            print()
            next_steps()
            break
        else:
            print_warning("Invalid selection. Please choose 1-4.")
            continue
    
    print()
    production_readiness_checklist()
    print()
    troubleshooting_guide()
    print()
    show_helpful_commands()
    print()
    next_steps()
    
    print(f"\n{COLORS['OKGREEN']}{COLORS['BOLD']}✓ Guide complete. Ready for deployment!{COLORS['ENDC']}\n")

if __name__ == "__main__":
    main()
