# IaaS Platform

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Podman](https://img.shields.io/badge/podman-ready-green.svg)](https://podman.io/)

**Open-source Infrastructure-as-a-Service (IaaS) Platform**

A fully open-source IaaS platform that provides virtual infrastructure provisioning and management, similar to hyperscalers like AWS, Azure, or GCP. The platform supports multiple cloud providers with automatic failover capabilities.

## Features

- **Multi-Provider Support**: Integrate with Hetzner, AWS, DigitalOcean, and more
- **Automatic Failover**: Built-in resilience with automatic provider failover
- **Provider Agnostic**: Abstract away provider-specific details
- **Open Source**: No vendor lock-in, fully transparent
- **Modular Architecture**: Independent services that scale horizontally
- **Developer-Friendly**: API-first design with comprehensive tooling

## Architecture

The IaaS platform consists of multiple independent services:

- **API Gateway**: Single entry point for all API requests (FastAPI)
- **Control Plane**: Core business logic and orchestration (Python + Celery)
- **Provider Abstraction Layer**: Unified interface for multiple cloud providers
- **Data Layer**: PostgreSQL + Redis for persistent storage
- **Message Queue**: RabbitMQ for async communication
- **Failover Manager**: Health monitoring and automatic failover
- **Web UI**: React + TypeScript dashboard
- **CLI**: Command-line interface for automation
- **Monitoring**: Prometheus + Grafana for observability

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture information.

## Quick Start

### Prerequisites

- [Podman](https://podman.io/) (or Docker)
- [Podman Compose](https://github.com/containers/podman-compose)
- Python 3.10+
- Node.js 18+ (for Web UI)

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
   - Web UI: http://localhost:3000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379
   - RabbitMQ: http://localhost:15672
   - MinIO: http://localhost:9001
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001

4. **Stop the development environment**:
   ```bash
   make dev-down
   ```

### Using the CLI

```bash
# Install the CLI
pip install -e .

# Check version
iaas-cli version

# Check service health
iaas-cli health
```

## Documentation

- [Project Overview](docs/PROJECT_OVERVIEW.md) - Vision, principles, and success metrics
- [Architecture](docs/ARCHITECTURE.md) - Detailed system architecture and component design
- [Development Roadmap](docs/ROADMAP.md) - 12-phase development plan with timeline
- [Development Guide](docs/DEVELOPMENT.md) - Setup instructions, coding standards, and workflow
- [Contributing](CONTRIBUTING.md) - How to contribute to the project

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
├── docs/                    # Documentation
├── src/                     # Source code
│   ├── api-gateway/         # API Gateway service
│   ├── control-plane/       # Control Plane service
│   ├── providers/           # Provider adapters
│   │   ├── hetzner/         # Hetzner Cloud provider
│   │   ├── aws/             # AWS provider
│   │   └── digitalocean/    # DigitalOcean provider
│   ├── data-layer/          # Data access layer
│   ├── failover-manager/    # Failover management
│   ├── monitoring/          # Monitoring services
│   ├── cli/                 # CLI client
│   └── web-ui/              # Web dashboard
├── tests/                   # Test files
├── deploy/                  # Deployment configurations
│   └── podman-compose/      # Podman Compose files
├── scripts/                 # Utility scripts
├── .github/                 # GitHub configuration
│   └── workflows/           # CI/CD workflows
├── LICENSE                  # Apache 2.0 License
├── README.md                # This file
├── pyproject.toml           # Python project config
├── Makefile                 # Common tasks
└── requirements.txt         # Python dependencies
```

## Supported Providers

| Provider | Status | Adapter |
|----------|--------|---------|
| Hetzner Cloud | ✅ Planned | `src/providers/hetzner/` |
| AWS | 📋 Planned | `src/providers/aws/` |
| DigitalOcean | 📋 Planned | `src/providers/digitalocean/` |

## Roadmap

The project is currently in **Phase 0: Project Foundation**. See [ROADMAP.md](docs/ROADMAP.md) for the complete 12-phase development plan.

### Upcoming Milestones

- **Phase 1**: Core Infrastructure (Provider Abstraction Layer, Data Layer, API Gateway)
- **Phase 2**: Compute Service (VM lifecycle management)
- **Phase 3**: Storage Service (Block and object storage)
- **Phase 4**: Network Service (VPC, security groups, load balancing)
- **Phase 5**: Identity & Access Management (Authentication, RBAC, multi-tenancy)
- **Phase 6**: Failover System (Health monitoring, automatic failover)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to the project.

### Good First Issues

Look for issues labeled with:
- `good first issue` - Beginner-friendly issues
- `help wanted` - Issues needing community help
- `documentation` - Documentation improvements

## Community

- [GitHub Discussions](https://github.com/ErwinJanssen/iaas-platform/discussions) - Ask questions and discuss ideas
- [GitHub Issues](https://github.com/ErwinJanssen/iaas-platform/issues) - Report bugs and request features
- [Pull Requests](https://github.com/ErwinJanssen/iaas-platform/pulls) - Submit your contributions

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by hyperscaler cloud platforms (AWS, Azure, GCP)
- Built with open-source technologies
- Thanks to all contributors and the open-source community

---

*Built with ❤️ for the open-source community*
