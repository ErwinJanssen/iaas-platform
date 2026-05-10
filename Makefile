# IaaS Platform Makefile - Hybrid Architecture
# Provides common tasks for development, testing, and deployment
# Uses existing tools (Crossplane, NATS, etc.) for commodity functionality

.PHONY: help dev-up dev-down dev-restart dev-logs dev-shell
.PHONY: test test-unit test-integration test-e2e test-coverage
.PHONY: lint format type-check clean clean-all
.PHONY: podman-build podman-up podman-down podman-restart podman-logs

# =============================================================================
# Development Environment (Podman)
# =============================================================================

PODMAN_COMPOSE_FILE := deploy/podman-compose/podman-compose.dev.yml
PODMAN_COMPOSE := podman-compose -f $(PODMAN_COMPOSE_FILE)

# Start development environment
dev-up:
	@echo "Starting IaaS Platform development environment with Podman..."
	@echo "Using Hybrid Architecture: Custom services + Existing tools (Crossplane, NATS, etc.)"
	@echo ""
	$(PODMAN_COMPOSE) up -d
	@echo ""
	@echo "Services started:"
	@$(PODMAN_COMPOSE) ps
	@echo ""
	@echo "Access services at:"
	@echo "  API Gateway:      http://localhost:8000"
	@echo "  Control Plane:    http://localhost:8001"
	@echo "  Failover Manager: http://localhost:8002"
	@echo "  PostgreSQL:       localhost:5432"
	@echo "  Redis:            localhost:6379"
	@echo "  NATS:             localhost:4222 (msg queue), localhost:8222 (monitoring)"
	@echo "  MinIO:            localhost:9000 (API), http://localhost:9001 (console)"
	@echo "  Prometheus:       http://localhost:9090"
	@echo "  Grafana:          http://localhost:3001"
	@echo "  Crossplane Mock:  http://localhost:8080 (for dev without Kubernetes)"
	@echo ""
	@echo "Note: For Crossplane in production, deploy to Kubernetes cluster"
	@echo "     For local Crossplane testing, use Kind: kind create cluster --name iaas-crossplane"

# Stop development environment
dev-down:
	@echo "Stopping development environment..."
	$(PODMAN_COMPOSE) down

# Restart development environment
dev-restart: dev-down dev-up

# View development logs
dev-logs:
	$(PODMAN_COMPOSE) logs -f

# View logs for specific service
dev-logs-%:
	$(PODMAN_COMPOSE) logs -f $*

# Open shell in specific service container
dev-shell-%:
	$(PODMAN_COMPOSE) exec $* sh

# =============================================================================
# Testing
# =============================================================================

# Run all tests
test: test-unit test-integration

# Run unit tests
test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v --tb=short

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v --tb=short

# Run end-to-end tests
test-e2e:
	@echo "Running end-to-end tests..."
	pytest tests/e2e/ -v --tb=short

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term -v
	@echo "Coverage report generated in htmlcov/"

# =============================================================================
# Code Quality
# =============================================================================

# Run linters
lint:
	@echo "Running linters..."
	flake8 src/ tests/
	@echo "Flake8 passed"
	@echo "Running mypy..."
	mypy src/
	@echo "Mypy passed"

# Format code
format:
	@echo "Formatting code with Black..."
	black src/ tests/
	@echo "Sorting imports with isort..."
	isort src/ tests/
	@echo "Code formatted"

# Run type checking
type-check:
	mypy src/

# =============================================================================
# Podman Commands
# =============================================================================

# Build Podman images
podman-build:
	@echo "Building Podman images..."
	$(PODMAN_COMPOSE) build

# Start Podman containers
podman-up: dev-up

# Stop Podman containers
podman-down: dev-down

# Restart Podman containers
podman-restart: dev-restart

# View Podman logs
podman-logs: dev-logs

# =============================================================================
# Kubernetes (for Crossplane)
# =============================================================================

# Create Kind cluster for local Crossplane testing
k8s-create-cluster:
	@echo "Creating Kind cluster for Crossplane..."
	kind create cluster --name iaas-crossplane --wait 5m
	@echo "Cluster created. Install Crossplane with: kubectl crossplane install"

# Delete Kind cluster
k8s-delete-cluster:
	@echo "Deleting Kind cluster..."
	kind delete cluster --name iaas-crossplane

# Install Crossplane
k8s-install-crossplane:
	@echo "Installing Crossplane..."
	kubectl crossplane install
	@echo "Crossplane installed. Install providers with: kubectl crossplane provider install <provider>"

# =============================================================================
# Python Environment
# =============================================================================

# Create virtual environment
venv:
	@echo "Creating Python virtual environment..."
	python -m venv .venv
	@echo "Activating and installing dependencies..."
	. .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

# Install dependencies
install:
	pip install -r requirements.txt -r requirements-dev.txt

# Install pre-commit hooks
pre-commit-install:
	pre-commit install

# =============================================================================
# Cleanup
# =============================================================================

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf *.egg-info/ dist/ build/ htmlcov/ .pytest_cache/ .mypy_cache/

# Clean everything (including virtual environment)
clean-all: clean
	rm -rf .venv/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# =============================================================================
# Documentation
# =============================================================================

docs-serve:
	@echo "Serving documentation locally..."
	mkdocs serve

docs-build:
	@echo "Building documentation..."
	mkdocs build

# =============================================================================
# Help
# =============================================================================

help:
	@echo "IaaS Platform Makefile - Hybrid Architecture"
	@echo "=============================================="
	@echo ""
	@echo "Architecture: Custom services (API GW, Control Plane, Failover Mgr)"
	@echo "             + Existing tools (Crossplane, NATS, PostgreSQL, etc.)"
	@echo ""
	@echo "Development Environment:"
	@echo "  make dev-up           Start development environment (Podman)"
	@echo "  make dev-down         Stop development environment"
	@echo "  make dev-restart      Restart development environment"
	@echo "  make dev-logs         View all service logs"
	@echo "  make dev-logs-<svc>   View logs for specific service"
	@echo "  make dev-shell-<svc>  Open shell in service container"
	@echo ""
	@echo "Kubernetes (Crossplane):"
	@echo "  make k8s-create-cluster    Create Kind cluster for local testing"
	@echo "  make k8s-delete-cluster    Delete Kind cluster"
	@echo "  make k8s-install-crossplane Install Crossplane to cluster"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-unit        Run unit tests"
	@echo "  make test-integration Run integration tests"
	@echo "  make test-e2e         Run end-to-end tests"
	@echo "  make test-coverage    Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linters (flake8, mypy)"
	@echo "  make format           Format code (black, isort)"
	@echo "  make type-check       Run type checking (mypy)"
	@echo ""
	@echo "Podman:"
	@echo "  make podman-build     Build Podman images"
	@echo "  make podman-up        Start Podman containers"
	@echo "  make podman-down      Stop Podman containers"
	@echo ""
	@echo "Python:"
	@echo "  make venv             Create virtual environment"
	@echo "  make install          Install dependencies"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Clean build artifacts"
	@echo "  make clean-all        Clean everything (including venv)"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs-serve       Serve documentation locally"
	@echo "  make docs-build       Build documentation"
