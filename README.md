# IaaS Platform

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Podman](https://img.shields.io/badge/podman-ready-green.svg)](https://podman.io/)

**Open-source Infrastructure-as-a-Service (IaaS) Platform with Multi-Provider Support and Automatic Failover**

A fully open-source IaaS platform that provides virtual infrastructure provisioning and management across multiple cloud providers, with **automatic failover** as the primary differentiator.

## Architecture: Hybrid Approach (Option 2)

We use a **hybrid architecture** that leverages existing open-source tools for commodity functionality and focuses our development efforts on the unique value proposition.

**Core Principle**: *Build what makes us unique. Reuse what doesn't.*

### Custom Components (We Build)
- **API Gateway** - Single entry point for all user API requests (FastAPI)
- **Control Plane** - Core business logic and orchestration (FastAPI)
- **Failover Manager** - Automatic provider failover and health monitoring (FastAPI)

### Existing Tools (We Leverage)
- **Crossplane** - Multi-cloud resource management (provider abstraction)
- **NATS** - Lightweight, high-performance message queue
- **PostgreSQL** - Primary relational database
- **Redis** - In-memory caching
- **MinIO** - S3-compatible object storage
- **Prometheus + Grafana** - Monitoring and observability

See [ARCHITECTURE-HYBRID.md](docs/ARCHITECTURE-HYBRID.md) for detailed architecture information.

## Features

- **Multi-Provider Support**: Integrate with Hetzner, AWS, DigitalOcean, and more via Crossplane
- **Automatic Failover**: Built-in resilience with automatic provider failover (our primary differentiator)
- **Unified API**: Single API across all providers
- **Open Source**: No vendor lock-in, fully transparent
- **Production-Ready**: Uses battle-tested tools from day one
- **Developer-Friendly**: API-first design with comprehensive tooling

## Quick Start

### Prerequisites

- [Podman](https://podman.io/) (or Docker)
- [Podman Compose](https://github.com/containers/podman-compose)
- Python 3.10+
- (Optional for Crossplane) [Kind](https://kind.sigs.k8s.io/) for local Kubernetes

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ErwinJanssen/iaas-platform.git
   cd iaas-platform
   ```

2. **Start the development environment**:
   ```bash
   make dev-up
   ```

3. **Access the services**:
   - API Gateway: http://localhost:8000
   - Control Plane: http://localhost:8001
   - Failover Manager: http://localhost:8002
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379
   - NATS: localhost:4222 (msg queue), localhost:8222 (monitoring)
   - MinIO: http://localhost:9001 (console)
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001
   - Crossplane Mock: http://localhost:8080 (for dev without Kubernetes)

4. **Stop the development environment**:
   ```bash
   make dev-down
   ```

### For Crossplane (Production or Local Testing)

For **production**, deploy Crossplane to your Kubernetes cluster:

```bash
# Install Crossplane
kubectl crossplane install

# Install providers
kubectl crossplane provider install provider-hetzner
kubectl crossplane provider install provider-aws
kubectl crossplane provider install provider-digitalocean
```

For **local testing** with Kind:

```bash
# Create Kind cluster
make k8s-create-cluster

# Install Crossplane
make k8s-install-crossplane
```

## Documentation

- [Architecture (Hybrid)](docs/ARCHITECTURE-HYBRID.md) - Detailed system architecture
- [Action/Todo List](docs/ACTIONS.md) - Plain-text task management system for AI sessions
- [Project Overview](docs/PROJECT_OVERVIEW.md) - Vision, principles, and success metrics
- [Development Roadmap](docs/ROADMAP.md) - Development plan with phases

## Development

### Running Tests

```bash
# Run all tests
make test

# Run unit tests
make test-unit

# Run integration tests
make test-integration

# Run tests with coverage
make test-coverage
```

### Code Quality

```bash
# Run linters
make lint

# Format code
make format

# Run type checking
make type-check
```

### Building

```bash
# Build Podman images
make podman-build

# Start development environment
make dev-up

# Stop development environment
make dev-down
```

## Project Structure

```
iaas-platform/
├── docs/                          # Documentation
│   ├── ARCHITECTURE-HYBRID.md    # Hybrid architecture design
│   ├── ACTIONS.md                # Plain-text task management (for AI sessions)
│   ├── PROJECT_OVERVIEW.md       # Vision and principles
│   └── ROADMAP.md                # Development roadmap
├── src/                           # Source code
│   ├── api-gateway/               # API Gateway service (custom)
│   │   └── main.py
│   ├── control-plane/             # Control Plane service (custom)
│   │   └── main.py
│   ├── failover-manager/           # Failover Manager service (custom)
│   │   └── main.py
│   └── shared/                    # Shared library
│       ├── __init__.py
│       └── (future: crossplane_client.py, nats_client.py, etc.)
├── tests/                         # Tests
│   └── unit/
│       └── test_services.py
├── deploy/                        # Deployment configurations
│   └── podman-compose/
│       ├── podman-compose.dev.yml  # Development environment
│       ├── Dockerfile.api-gateway
│       ├── Dockerfile.control-plane
│       ├── Dockerfile.failover-manager
│       └── prometheus.yml
├── scripts/                       # Utility scripts
│   └── crossplane_mock/           # Mock Crossplane API for local dev
│       └── server.py
├── .github/                       # GitHub configuration
│   └── workflows/
│       ├── test.yml              # CI: Run tests
│       └── lint.yml              # CI: Run linters
├── LICENSE                       # Apache 2.0 License
├── README.md                     # This file
├── Makefile                      # Common tasks
├── pyproject.toml                # Python project config
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
└── .env.example                  # Environment variables template
```

## Why Hybrid Architecture?

### Benefits

1. **Faster Time to Market**: 80% of functionality with 20% of the effort
2. **Production-Ready**: Uses battle-tested tools from day one
3. **Focus on Unique Value**: Spend time on what makes us different (failover, orchestration)
4. **Community Support**: Leverage existing tool ecosystems
5. **Maintainability**: Less custom code to maintain

### Comparison

| Aspect | Hybrid Approach | Full Custom Build |
|--------|-----------------|-------------------|
| Development Time | 3-6 months | 12-18 months |
| Maintenance | Medium | High |
| Flexibility | High | Higher |
| Production Readiness | High | Medium (initially) |
| Community Support | High | Low (initially) |

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| API Gateway | FastAPI (Python) | User API |
| Control Plane | FastAPI (Python) | Orchestration |
| Failover Manager | FastAPI (Python) | Failover logic |
| Provider Abstraction | Crossplane | Multi-cloud resources |
| Message Queue | NATS | Async communication |
| Database | PostgreSQL | Persistent storage |
| Cache | Redis | Caching |
| Object Storage | MinIO | Object storage |
| Monitoring | Prometheus + Grafana | Metrics/alerting |
| Container Runtime | Podman | Containerization |
| Orchestration | Kubernetes | Production deployment |

## Contributing

See [ACTIONS.md](docs/ACTIONS.md) for the current task list and development status.

### For AI Sessions

The [ACTIONS.md](docs/ACTIONS.md) file serves as a plain-text Jira for AI sessions:
- Tracks all actions, decisions, considerations, and questions
- Structured format for easy parsing by AI
- Can be used across sessions to maintain context
- Includes dependencies, priorities, and status

### For Human Contributors

1. Check [ACTIONS.md](docs/ACTIONS.md) for open tasks
2. Follow the development guidelines in [DEVELOPMENT.md](docs/DEVELOPMENT.md)
3. Submit pull requests with comprehensive tests

## Community

- [GitHub Discussions](https://github.com/ErwinJanssen/iaas-platform/discussions) - Ask questions and discuss ideas
- [GitHub Issues](https://github.com/ErwinJanssen/iaas-platform/issues) - Report bugs and request features
- [Pull Requests](https://github.com/ErwinJanssen/iaas-platform/pulls) - Submit your contributions

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Crossplane**: For multi-cloud resource management
- **NATS**: For high-performance messaging
- **FastAPI**: For the web framework
- **Kubernetes**: For container orchestration
- All the open-source contributors who make these tools possible

---

*Built with ❤️ for the open-source community*
*Architecture: Hybrid (Custom + Existing Tools)*
