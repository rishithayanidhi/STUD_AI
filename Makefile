.PHONY: help install dev test build deploy clean docker-build docker-up docker-down setup-db prod-env prod-deploy

help:
	@echo "================================================================"
	@echo "STUAI Autonomous Operations - Command Reference"
	@echo "================================================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          - Install Python dependencies"
	@echo "  make setup-db         - Setup PostgreSQL database"
	@echo "  make prod-env         - Generate production .env interactively"
	@echo ""
	@echo "Development:"
	@echo "  make dev              - Run FastAPI server in dev mode"
	@echo "  make test             - Run test suite"
	@echo "  make lint             - Run code quality checks"
	@echo ""
	@echo "Docker & Deployment:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start Docker Compose stack (dev)"
	@echo "  make docker-down      - Stop Docker Compose stack"
	@echo "  make prod-deploy      - Deploy production stack with real credentials"
	@echo "  make docker-logs      - View Docker logs"
	@echo "  make docker-clean     - Clean up Docker resources"
	@echo ""
	@echo "Utilities:"
	@echo "  make show-links       - Display all service URLs and endpoints"
	@echo "  make show-config      - Display current configuration"
	@echo "  make clean            - Clean up Python cache and build artifacts"
	@echo "  make health           - Check all service health"
	@echo ""

install:
	pip install -r requirements.txt

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	python -m pytest tests/ -v --cov=. --cov-report=html

lint:
	pylint agent.py main.py tools.py memory.py || true
	black --check agent.py main.py tools.py memory.py || true

setup-db:
	python quick_postgres.py

prod-env:
	python generate_production_env.py

docker-build:
	docker build -t stuai:latest .
	@echo "✓ Docker image built successfully"

docker-up:
	docker-compose up -d
	@echo "✓ Docker Compose stack started"
	@echo "API available at: http://localhost:8000"
	@echo "pgAdmin available at: http://localhost:5050"

docker-down:
	docker-compose down
	@echo "✓ Docker Compose stack stopped"

docker-logs:
	docker-compose logs -f

docker-clean:
	docker system prune -f
	docker image prune -f

prod-deploy:
	@echo "Starting production deployment..."
	@echo ""
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Running credential collection..."; \
		python generate_production_env.py; \
	fi
	@echo "Deploying production stack..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✓ Production deployment complete"
	@echo ""
	@echo "🚀 Next steps:"
	@echo "  1. Check health: curl http://localhost:8000/health"
	@echo "  2. View API docs: http://localhost:8000/docs"
	@echo "  3. Monitor logs: docker-compose -f docker-compose.prod.yml logs -f"

show-links:
	python show_all_links.py

show-config:
	python config_view.py

health:
	@echo "Checking STUAI services health..."
	@curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "❌ API not responding"
	@echo ""
	@echo "Database health:"
	@docker-compose exec -T postgres pg_isready -U stuai 2>/dev/null && echo "✓ PostgreSQL healthy" || echo "⚠️  PostgreSQL not responding"
	@echo ""
	@echo "Redis health:"
	@docker-compose exec -T redis redis-cli ping 2>/dev/null && echo "✓ Redis healthy" || echo "⚠️  Redis not responding"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage*" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned up Python cache files"
