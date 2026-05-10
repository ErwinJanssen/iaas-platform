# IaaS Platform - Development Guide

## Overview

This document provides guidelines and instructions for developing the IaaS platform. It covers the development environment setup, coding standards, workflow, and best practices.

## Prerequisites

### Required Tools
- **Git**: Version control system
- **Docker**: Container runtime (v20.10+)
- **Docker Compose**: Container orchestration (v2.0+)
- **Python**: 3.10+ (for backend services)
- **Node.js**: 18+ (for frontend development)
- **Go**: 1.20+ (optional, for some services)
- **PostgreSQL Client**: psql or pgAdmin
- **Redis Client**: redis-cli
- **GitHub CLI**: gh (for GitHub operations)

### Recommended Tools
- **IDE**: VS Code, PyCharm, or GoLand
- **Terminal**: iTerm2 (macOS), Windows Terminal, or Linux terminal
- **API Testing**: Postman, Insomnia, or curl
- **Database GUI**: DBeaver, TablePlus, or pgAdmin
- **Monitoring**: Grafana, Prometheus

---

## Project Structure

```
iaas-platform/
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # Technical architecture
│   ├── ROADMAP.md           # Development roadmap
│   ├── DEVELOPMENT.md       # This file
│   └── ...
├── src/                     # Source code
│   ├── api-gateway/         # API Gateway service
│   ├── control-plane/       # Control Plane service
│   ├── providers/           # Provider adapters
│   │   ├── hetzner/         # Hetzner provider
│   │   ├── aws/             # AWS provider (future)
│   │   └── ...
│   ├── data-layer/          # Data access layer
│   ├── failover-manager/    # Failover management
│   ├── monitoring/          # Monitoring services
│   ├── cli/                 # CLI client
│   └── web-ui/              # Web dashboard
├── tests/                   # Test files
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
├── deploy/                  # Deployment configurations
│   ├── docker-compose/      # Local development
│   ├── kubernetes/         # Production deployment
│   └── terraform/           # Infrastructure as Code
├── scripts/                 # Utility scripts
│   ├── setup-dev.sh         # Development setup
│   ├── run-tests.sh         # Test runner
│   └── ...
├── .github/                 # GitHub configuration
│   ├── workflows/           # CI/CD workflows
│   └── ISSUE_TEMPLATE/      # Issue templates
├── LICENSE                  # Open source license
├── README.md                # Project README
├── pyproject.toml           # Python project config
├── package.json             # Node.js dependencies
└── Makefile                 # Common tasks
```

---

## Development Environment Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/ErwinJanssen/iaas-platform.git
cd iaas-platform

# Set up git hooks (optional)
./scripts/setup-git-hooks.sh
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.\.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Set Up Node.js Environment (for Web UI)

```bash
# Navigate to web-ui directory
cd src/web-ui

# Install dependencies
npm install

# Return to project root
cd ../..
```

### 4. Set Up Docker Environment

```bash
# Build all Docker images
docker-compose -f deploy/docker-compose/docker-compose.dev.yml build

# Start the development environment
docker-compose -f deploy/docker-compose/docker-compose.dev.yml up -d

# Verify services are running
docker-compose -f deploy/docker-compose/docker-compose.dev.yml ps
```

### 5. Verify Setup

```bash
# Check API Gateway health
curl http://localhost:8000/health

# Check database connection
psql -h localhost -p 5432 -U postgres -d iaas

# Check Redis connection
redis-cli -h localhost -p 6379 ping
```

---

## Running the Platform Locally

### Start All Services

```bash
# Using docker-compose (recommended)
docker-compose -f deploy/docker-compose/docker-compose.dev.yml up -d

# Or using Makefile
make dev-up
```

### Stop All Services

```bash
# Using docker-compose
docker-compose -f deploy/docker-compose/docker-compose.dev.yml down

# Or using Makefile
make dev-down
```

### Run Individual Services

```bash
# API Gateway
cd src/api-gateway
uvicorn main:app --reload --port 8000

# Control Plane
cd src/control-plane
python -m control_plane.main

# Web UI
cd src/web-ui
npm run dev
```

---

## Coding Standards

### Python

#### Style Guide
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use single quotes for strings (consistent with Black)
- Use f-strings for string formatting

#### Formatting
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://github.com/PyCQA/isort) for import sorting
- Use [flake8](https://flake8.pycqa.org/) for linting

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Run linter
flake8 src/ tests/
```

#### Type Hints
- Use Python type hints for all function signatures
- Use `typing` module for complex types
- Use `pydantic` for data validation and settings

```python
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class VMCreateRequest(BaseModel):
    name: str
    cpu_cores: int
    memory_gb: int
    image_id: str
    ssh_keys: Optional[List[str]] = None

def create_vm(request: VMCreateRequest) -> Dict[str, Any]:
    # Implementation
    ...
```

#### Testing
- Use [pytest](https://docs.pytest.org/) for testing
- Test files should be named `test_*.py` or `*_test.py`
- Use fixtures for test dependencies
- Aim for >80% test coverage

```python
import pytest
from src.api_gateway.main import app

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

### JavaScript/TypeScript (Web UI)

#### Style Guide
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Use 2 spaces for indentation
- Maximum line length: 100 characters
- Use single quotes for strings

#### Formatting
- Use [Prettier](https://prettier.io/) for code formatting
- Use [ESLint](https://eslint.org/) for linting

```bash
# Format code
cd src/web-ui
npm run format

# Run linter
npm run lint
```

#### Component Structure
- Use functional components with React hooks
- Use TypeScript interfaces for props
- Follow component folder structure:
  ```
  components/
  └── Button/
      ├── Button.tsx
      ├── Button.stories.tsx
      ├── Button.test.tsx
      └── index.ts
  ```

### Go (if used)

#### Style Guide
- Follow [Effective Go](https://golang.org/doc/effective_go.html)
- Use `gofmt` for formatting
- Use `golint` for linting
- Use 4 spaces for indentation (tabs are also acceptable)

```bash
# Format code
gofmt -w ./...

# Run linter
golint ./...
```

---

## Git Workflow

### Branching Strategy

We use a modified GitHub Flow:

1. **main**: Production-ready code (protected)
2. **develop**: Integration branch for features (protected)
3. **feature/***: Feature branches
4. **fix/***: Bug fix branches
5. **release/***: Release preparation branches

### Branch Naming

```
feature/[short-description]    # e.g., feature/add-vm-api
fix/[short-description]        # e.g., fix/auth-bypass
release/v[version]             # e.g., release/v0.1.0
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(api): add VM creation endpoint

- Add POST /api/v1/vms endpoint
- Add request validation
- Add unit tests

Closes #123
```

```
fix(providers/hetzner): handle rate limiting

- Add retry logic for rate limited requests
- Add exponential backoff

Fixes #456
```

### Pull Requests

1. **Title**: Clear and descriptive
2. **Description**: Explain what and why
3. **Linked Issues**: Reference related issues
4. **Checks**: All CI checks must pass
5. **Reviews**: At least 1 approval required
6. **Squash Merge**: Use squash merge for clean history

### PR Template

```markdown
## Description

[Brief description of changes]

## Related Issues

- Closes #123
- Related to #456

## Changes Made

- [ ] Feature implementation
- [ ] Bug fix
- [ ] Documentation update
- [ ] Test coverage
- [ ] Breaking changes

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if applicable)

## Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

---

## CI/CD Pipeline

### GitHub Actions Workflows

Located in `.github/workflows/`:

1. **test.yml**: Runs tests on every push and PR
2. **lint.yml**: Runs linting on every push and PR
3. **build.yml**: Builds Docker images on push to main/develop
4. **deploy.yml**: Deploys to staging/production
5. **release.yml**: Creates releases and publishes packages

### Workflow Triggers

| Workflow | Trigger | Branches |
|----------|---------|----------|
| Test | Push, PR | All |
| Lint | Push, PR | All |
| Build | Push | main, develop |
| Deploy (staging) | Push | develop |
| Deploy (production) | Manual | main |
| Release | Manual | main |

### Environment Variables

Required secrets in GitHub repository:

```
# Docker Hub
DOCKER_HUB_USERNAME
DOCKER_HUB_TOKEN

# Cloud Providers (for testing)
HETZNER_API_TOKEN
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# Database
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

# Other
SENTRY_DSN
SLACK_WEBHOOK_URL
```

---

## Testing Strategy

### Test Pyramid

```
          ┌─────────┐
          │   E2E   │  ~10% of tests
          └────┬────┘
           ┌─────┴─────┐
           │ Integration │  ~20% of tests
           └──────┬──────┘
                ┌──┴──┐
                │ Unit │  ~70% of tests
                └─────┘
```

### Test Types

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test interactions between components
3. **E2E Tests**: Test complete user journeys
4. **Contract Tests**: Test API contracts
5. **Performance Tests**: Test performance characteristics
6. **Security Tests**: Test security vulnerabilities

### Running Tests

```bash
# Run all tests
make test

# Run unit tests
make test-unit

# Run integration tests
make test-integration

# Run E2E tests
make test-e2e

# Run tests with coverage
make test-coverage

# Run specific test file
pytest tests/unit/test_vm_api.py

# Run tests with verbose output
pytest -v tests/unit/

# Run tests and watch for changes
pytest-watch tests/unit/
```

---

## Monitoring and Observability

### Local Development

```bash
# View logs for all services
docker-compose -f deploy/docker-compose/docker-compose.dev.yml logs -f

# View logs for specific service
docker-compose -f deploy/docker-compose/docker-compose.dev.yml logs -f api-gateway

# Access Prometheus
open http://localhost:9090

# Access Grafana
open http://localhost:3000

# Access Jaeger (tracing)
open http://localhost:16686
```

### Metrics

All services should expose Prometheus metrics at `/metrics`:

```python
from prometheus_client import start_http_server

# Start metrics server on port 8000
start_http_server(8000)
```

### Logging

Use structured logging with `structlog` or `logging`:

```python
import logging
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()
logger.info("user_login", user_id="123", action="login")
```

Log levels:
- `DEBUG`: Detailed debugging information
- `INFO`: General information about operations
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

---

## Debugging

### Python Debugging

```bash
# Run with debug mode
python -m pdb src/api_gateway/main.py

# Or use breakpoint() in code
breakpoint()

# Remote debugging with VS Code
# Add to launch.json:
{
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    }
}
```

### Docker Debugging

```bash
# Enter running container
docker exec -it iaas-platform-api-gateway-1 bash

# View container logs
docker logs iaas-platform-api-gateway-1

# Inspect container
docker inspect iaas-platform-api-gateway-1

# View resource usage
docker stats iaas-platform-api-gateway-1
```

### Database Debugging

```bash
# Connect to PostgreSQL
psql -h localhost -p 5432 -U postgres -d iaas

# List tables
\dt

# View table schema
\d users

# Run queries
SELECT * FROM vms LIMIT 10;

# Connect to Redis
redis-cli -h localhost -p 6379

# List keys
KEYS *

# Get value
GET some_key
```

---

## Performance Optimization

### Profiling Python Code

```bash
# Install profiler
pip install py-spy

# Profile running application
py-spy top --pid <PID>

# Record profile
py-spy record -o profile.svg --pid <PID>

# Use cProfile
python -m cProfile -o profile.prof src/api_gateway/main.py

# Analyze profile
python -m pstats profile.prof
```

### Database Optimization

```bash
# Enable slow query logging in PostgreSQL
ALTER SYSTEM SET log_min_duration_statement = 1000;  # Log queries > 1s

# View query execution plan
EXPLAIN ANALYZE SELECT * FROM vms WHERE user_id = 123;

# Add index
CREATE INDEX idx_vms_user_id ON vms(user_id);

# Vacuum analyze
VACUUM ANALYZE vms;
```

---

## Security Best Practices

### Secrets Management

1. **Never commit secrets to Git**: Use environment variables or secret managers
2. **Use .env files for development**: Add to `.gitignore`
3. **Production secrets**: Use HashiCorp Vault or cloud secret manager

```bash
# .env file example
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_DB=iaas
HETZNER_API_TOKEN=your_token
```

### Dependency Security

```bash
# Scan Python dependencies for vulnerabilities
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit

# Scan Node.js dependencies
npm audit

# Scan Docker images
docker scan iaas-platform-api-gateway
```

### Code Security

1. **Input Validation**: Always validate user input
2. **Output Encoding**: Prevent XSS attacks
3. **SQL Injection**: Use parameterized queries
4. **Authentication**: Use strong authentication
5. **Authorization**: Always check permissions
6. **Rate Limiting**: Prevent abuse

```python
# Example: SQL Injection prevention
import psycopg2

# BAD: Vulnerable to SQL injection
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

---

## Documentation

### Code Documentation

1. **Module Docstrings**: Every module should have a docstring
2. **Function Docstrings**: Every public function should have a docstring
3. **Type Hints**: Use type hints for better IDE support
4. **Comments**: Use comments to explain why, not what

```python
"""Module for VM management.

This module provides functionality for creating, managing, and deleting
virtual machines across multiple cloud providers.
"""

from typing import Optional


def create_vm(name: str, cpu_cores: int, memory_gb: int) -> Optional[str]:
    """Create a new virtual machine.
    
    Args:
        name: The name of the VM
        cpu_cores: Number of CPU cores
        memory_gb: Amount of memory in GB
        
    Returns:
        The ID of the created VM, or None if creation failed
        
    Raises:
        ValueError: If parameters are invalid
        ProviderError: If provider fails to create VM
    """
    # Implementation
    ...
```

### API Documentation

Use OpenAPI/Swagger for API documentation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class VMCreateRequest(BaseModel):
    """Request model for VM creation."""
    name: str
    cpu_cores: int
    memory_gb: int

@app.post("/api/v1/vms", response_model=VMResponse)
def create_vm(request: VMCreateRequest):
    """Create a new virtual machine.
    
    Creates a new VM with the specified configuration.
    
    - **name**: Unique name for the VM
    - **cpu_cores**: Number of CPU cores (1-64)
    - **memory_gb**: Amount of memory in GB (1-512)
    """
    # Implementation
    ...
```

### Architecture Decision Records (ADRs)

Document important architectural decisions in `docs/adr/`:

```markdown
# ADR 001: Use FastAPI for API Gateway

## Status
Accepted

## Context
We need to choose a web framework for the API Gateway service.

## Decision
Use FastAPI for the API Gateway.

## Alternatives Considered
1. Flask: Simpler but less structured
2. Django: More batteries-included but heavier
3. Express (Node.js): Different language ecosystem
4. Gin (Go): Different language ecosystem

## Rationale
- FastAPI provides automatic OpenAPI documentation
- Built-in data validation with Pydantic
- Async support out of the box
- Excellent performance
- Growing ecosystem
- Python is the primary language for the project

## Consequences
- Positive: Faster development, better documentation
- Negative: Python runtime dependency
```

---

## Contributing

### For External Contributors

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### For Team Members

1. Pick up an issue from the current sprint
2. Create a branch from develop
3. Make your changes
4. Push to your branch
5. Create a pull request to develop
6. Request reviews
7. Address feedback
8. Merge after approval

### Code Review Guidelines

1. **Be Respectful**: Always be respectful and constructive
2. **Focus on Quality**: Ensure code meets quality standards
3. **Suggest Improvements**: Offer suggestions, not just criticism
4. **Be Timely**: Review PRs within 24-48 hours
5. **Test Changes**: Verify changes work as expected

---

## Troubleshooting

### Common Issues

#### Docker Issues

```bash
# Docker daemon not running
sudo systemctl start docker

# Permission denied
docker-compose -f deploy/docker-compose/docker-compose.dev.yml up -d
# If still issues:
sudo usermod -aG docker $USER
newgrp docker

# Port already in use
lsof -i :8000
kill -9 <PID>
```

#### Database Issues

```bash
# Database not starting
# Check logs:
docker logs iaas-platform-postgres-1

# Reset database (development only)
docker-compose -f deploy/docker-compose/docker-compose.dev.yml down -v
docker-compose -f deploy/docker-compose/docker-compose.dev.yml up -d

# Connection refused
# Check if database is running:
psql -h localhost -p 5432 -U postgres -c "SELECT 1"
```

#### Python Issues

```bash
# Module not found
pip install -r requirements.txt

# Virtual environment not activated
source .venv/bin/activate

# Port already in use
lsof -i :8000
kill -9 <PID>
```

#### Node.js Issues

```bash
# Module not found
cd src/web-ui
npm install

# Port already in use
lsof -i :3000
kill -9 <PID>
```

---

## Makefile Reference

```bash
# Development
make dev-up          # Start development environment
make dev-down        # Stop development environment
make dev-restart     # Restart development environment
make dev-logs        # View development logs

# Testing
make test            # Run all tests
make test-unit       # Run unit tests
make test-integration # Run integration tests
make test-e2e        # Run E2E tests
make test-coverage   # Run tests with coverage

# Code Quality
make lint            # Run linters
make format          # Format code
make type-check      # Run type checking

# Docker
make docker-build    # Build Docker images
make docker-push     # Push Docker images
make docker-pull     # Pull Docker images

# Documentation
make docs-serve      # Serve documentation locally
make docs-build      # Build documentation

# Cleanup
make clean           # Clean build artifacts
make clean-all       # Clean everything
```

---

## Additional Resources

- [Architecture Document](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Project Overview](PROJECT_OVERVIEW.md)
- [GitHub Repository](https://github.com/ErwinJanssen/iaas-platform)
- [Issue Tracker](https://github.com/ErwinJanssen/iaas-platform/issues)
- [Discussions](https://github.com/ErwinJanssen/iaas-platform/discussions)

---

*Last Updated: 2024-05-10*
