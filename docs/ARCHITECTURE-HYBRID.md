# IaaS Platform - Hybrid Architecture (Option 2)

## Overview

This document describes the **Hybrid Architecture** approach for the IaaS Platform, which leverages existing open-source tools where possible and builds custom components only where necessary.

## Architecture Philosophy

**"Stand on the shoulders of giants"** - Use production-grade, battle-tested tools for commodity functionality, and focus our development efforts on the unique value proposition of the IaaS Platform.

## Core Principle

> **Build what makes us unique. Reuse what doesn't.**

Our unique value propositions:
1. **Multi-provider abstraction with automatic failover**
2. **Unified API across providers**
3. **Developer-friendly experience**
4. **Open-source transparency**

Everything else (message queues, databases, monitoring, UI frameworks) should use existing tools.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IaaS Platform - Hybrid Architecture                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CUSTOM COMPONENTS                              │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────┐    │   │
│  │  │   API        │    │  Control     │    │   Failover           │    │   │
│  │  │   Gateway    │◄──►│   Plane      │◄──►│   Manager           │    │   │
│  │  │  (FastAPI)   │    │  (FastAPI)   │    │   (FastAPI)          │    │   │
│  │  └──────────────┘    └──────────────┘    └─────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ▲        ▲        ▲                              │
│                              │        │        │                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      EXISTING TOOLS (LEVERAGED)                        │   │
│  │                                                                     │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────┐    │   │
│  │  │  Crossplane  │    │    NATS      │    │  Prometheus +       │    │   │
│  │  │ (Provider   │    │  (Message    │    │  Grafana            │    │   │
│  │  │  Abstraction)│    │   Queue)    │    │  (Monitoring)      │    │   │
│  │  └──────────────┘    └──────────────┘    └─────────────────────┘    │   │
│  │           ▲                  ▲                  ▲                    │   │
│  │           │                  │                  │                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    PROVIDER ADAPTERS (Crossplane)                │   │   │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐  ┌─────────────┐    │   │   │
│  │  │  │Hetzner  │  │  AWS    │  │ DigitalOcean │  │   ...      │    │   │   │
│  │  │  │Provider │  │ Provider │  │ Provider     │  │   Provider  │    │   │   │
│  │  │  └─────────┘  └─────────┘  └─────────────┘  └─────────────┘    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DATA LAYER                                      │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────┐    │   │
│  │  │ PostgreSQL   │    │   Redis      │    │   MinIO             │    │   │
│  │  │ (Primary DB) │    │  (Cache)     │    │   (Object Storage)  │    │   │
│  │  └──────────────┘    └──────────────┘    └─────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        WEB UI (Optional)                               │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Backstage (Future)                             │   │   │
│  │  │  Developer portal with plugins for Kubernetes, monitoring, etc.   │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### Custom Components (We Build)

These are the components that provide our **unique value proposition** and require custom development:

#### 1. API Gateway
- **Purpose**: Single entry point for all user API requests
- **Technology**: FastAPI (Python)
- **Responsibilities**:
  - Authentication and authorization
  - Request routing to Control Plane
  - Rate limiting
  - API documentation (OpenAPI)
  - Request/response transformation
- **Why Custom**: We need a user-facing API that abstracts our internal architecture

#### 2. Control Plane
- **Purpose**: Core business logic and orchestration
- **Technology**: FastAPI (Python) + Crossplane client
- **Responsibilities**:
  - Resource provisioning/deprovisioning
  - Workflow orchestration
  - State management
  - Quota enforcement
  - Provider selection logic
  - Integration with Crossplane for resource management
- **Why Custom**: This is where our orchestration logic lives - our secret sauce

#### 3. Failover Manager
- **Purpose**: Automatic provider failover and health monitoring
- **Technology**: FastAPI (Python)
- **Responsibilities**:
  - Provider health monitoring
  - Failover detection
  - Automatic resource migration
  - Failover policy enforcement
  - Notification during failover events
  - Integration with Crossplane for resource recreation
- **Why Custom**: This is our **primary differentiator** - automatic multi-provider failover

### Existing Tools (We Leverage)

These are production-grade tools we'll use instead of building our own:

#### 1. Crossplane (Provider Abstraction Layer)
- **Purpose**: Multi-cloud resource management
- **Website**: https://crossplane.io
- **What it provides**:
  - Provider-agnostic resource types (Compute, Storage, Network)
  - Existing providers for Hetzner, AWS, DigitalOcean, GCP, Azure, etc.
  - Kubernetes-native control plane
  - Resource reconciliation and drift detection
- **Our integration**:
  - Control Plane will use Crossplane's Python SDK or REST API
  - We'll extend with custom logic for our use cases
- **Benefit**: Saves **3-6 months** of development

#### 2. NATS (Message Queue)
- **Purpose**: Lightweight, high-performance message queue
- **Website**: https://nats.io
- **What it provides**:
  - Pub/sub messaging
  - Request/reply patterns
  - Queue groups for load balancing
  - JetStream for persistence
- **Our integration**:
  - Async communication between services
  - Event-driven architecture
- **Benefit**: Lighter and faster than RabbitMQ, cloud-native

#### 3. PostgreSQL (Database)
- **Purpose**: Primary relational database
- **Website**: https://www.postgresql.org
- **What it provides**:
  - ACID-compliant relational database
  - JSON support for flexible schemas
  - Extensible with custom types
- **Our integration**:
  - Store platform state (users, organizations, resources, etc.)
  - SQLAlchemy ORM for Python
- **Benefit**: Production-ready, well-understood

#### 4. Redis (Cache)
- **Purpose**: In-memory caching and session storage
- **Website**: https://redis.io
- **What it provides**:
  - Key/value caching
  - Session storage
  - Rate limiting
  - Pub/sub capabilities
- **Our integration**:
  - Caching for frequently accessed data
  - Session management
- **Benefit**: Battle-tested, high performance

#### 5. MinIO (Object Storage)
- **Purpose**: S3-compatible object storage
- **Website**: https://min.io
- **What it provides**:
  - Object storage API
  - S3 compatibility
  - Multi-tenant support
- **Our integration**:
  - Store user data, backups, logs
  - Can be replaced with actual S3 later
- **Benefit**: Self-hosted, S3-compatible

#### 6. Prometheus + Grafana (Monitoring)
- **Purpose**: Metrics collection and visualization
- **Websites**: https://prometheus.io, https://grafana.com
- **What it provides**:
  - Metrics collection and storage
  - Alerting
  - Dashboards and visualization
  - Query language (PromQL)
- **Our integration**:
  - Monitor all services
  - Custom metrics for platform resources
  - Alerts for failover events
- **Benefit**: Industry standard, production-ready

#### 7. Backstage (Web UI - Future)
- **Purpose**: Developer portal
- **Website**: https://backstage.io
- **What it provides**:
  - Unified developer portal
  - Plugins for Kubernetes, monitoring, CI/CD, etc.
  - Customizable dashboards
  - Tech docs integration
- **Our integration**:
  - Plugin for our API
  - Custom UI components for our features
- **Benefit**: Saves **weeks** of frontend development
- **Status**: Optional - can add later

---

## Data Flow

### User Request Flow

```
User → API Gateway → Control Plane → Crossplane → Cloud Provider
                     ↓
               NATS (async tasks)
                     ↓
               Failover Manager ←─┘
```

### Failover Flow

```
Provider Health Check (Failover Manager)
         ↓
   Detect Outage
         ↓
   Verify (multiple checks)
         ↓
   Select Target Provider
         ↓
   Notify Control Plane
         ↓
   Recreate Resources (via Crossplane)
         ↓
   Update DNS/Routing
         ↓
   Notify User
```

---

## Service Communication

| From | To | Protocol | Purpose |
|------|-----|----------|---------|
| User | API Gateway | HTTPS | API requests |
| API Gateway | Control Plane | HTTP | Resource operations |
| Control Plane | Crossplane | HTTP/Kubernetes API | Resource provisioning |
| Control Plane | NATS | NATS | Async tasks |
| Failover Manager | NATS | NATS | Listen for events |
| Failover Manager | Control Plane | HTTP | Failover coordination |
| All Services | PostgreSQL | PostgreSQL | Data storage |
| All Services | Redis | Redis | Caching |
| All Services | MinIO | S3 API | Object storage |
| All Services | Prometheus | HTTP | Metrics |

---

## Resource Model

### Platform Resources (Our Abstraction)

```
Organization
  └── Project
      ├── Compute (VMs)
      │   ├── Spec: name, cpu, memory, image
      │   └── State: pending, running, stopped, error
      ├── Storage
      │   ├── Block Storage (Volumes)
      │   └── Object Storage (Buckets)
      ├── Network
      │   ├── VPC
      │   ├── Subnet
      │   ├── Security Group
      │   └── Load Balancer
      └── Identity
          ├── User
          ├── Group
          ├── Role
          └── Permission
```

### Mapping to Crossplane

Our platform resources map to Crossplane's **Managed Resources**:

| Platform Resource | Crossplane Resource | Provider |
|-------------------|---------------------|----------|
| VM | `ComputeInstance` | provider-hetzner, provider-aws, etc. |
| Volume | `Volume` | provider-hetzner, provider-aws, etc. |
| VPC | `Network` | provider-hetzner, provider-aws, etc. |
| Subnet | `Subnet` | provider-hetzner, provider-aws, etc. |
| Security Group | `SecurityGroup` | provider-hetzner, provider-aws, etc. |

---

## Deployment Architecture

### Development Environment (Podman)

```
┌─────────────────────────────────────────────────────────────┐
│  Development Machine                                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │
│  │ API     │  │ Control │  │ Failover │  │ Crossplane  │    │
│  │ Gateway │  │ Plane   │  │ Manager │  │             │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └──────┬──────┘    │
│       │            │            │             │            │
│       ▼            ▼            ▼             ▼            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Podman Network (iaas-network)                         │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │  │PostgreSQL│  │ Redis   │  │ NATS    │  │ MinIO   │  │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Prometheus + Grafana (Monitoring)                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Production Environment (Kubernetes)

```
┌─────────────────────────────────────────────────────────────┐
│  Kubernetes Cluster                                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Namespaces                                              │   │
│  │                                                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │
│  │  │ iaas-api     │  │ iaas-control │  │ iaas-failover│    │   │
│  │  │             │  │             │  │             │    │   │
│  │  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │    │   │
│  │  │  │ API   │  │  │  │Control│  │  │  │Failover│  │    │   │
│  │  │  │ GW    │  │  │  │Plane │  │  │  │Manager│  │    │   │
│  │  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  crossplane-system (Crossplane)                      │   │   │
│  │  │  - Crossplane controller                            │   │   │
│  │  │  - Provider controllers (Hetzner, AWS, etc.)        │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │
│  │  │ monitoring  │  │ logging     │  │ storage      │    │   │
│  │  │             │  │             │  │             │    │   │
│  │  │ - Prometheus│  │ - Loki      │  │ - MinIO      │    │   │
│  │  │ - Grafana   │  │ - Promtail  │  │ - PostgreSQL │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Ingress Controller (Traefik/NGINX)                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Summary

| Component | Technology | Purpose | Custom/Existing |
|-----------|------------|---------|----------------|
| API Gateway | FastAPI (Python) | User API | Custom |
| Control Plane | FastAPI (Python) | Orchestration | Custom |
| Failover Manager | FastAPI (Python) | Failover logic | Custom |
| Provider Abstraction | Crossplane | Multi-cloud resources | Existing |
| Message Queue | NATS | Async communication | Existing |
| Database | PostgreSQL | Persistent storage | Existing |
| Cache | Redis | Caching | Existing |
| Object Storage | MinIO | Object storage | Existing |
| Monitoring | Prometheus + Grafana | Metrics/alerting | Existing |
| Web UI | Backstage (future) | Developer portal | Existing |
| Container Runtime | Podman/Docker | Containerization | Existing |
| Orchestration | Kubernetes | Production deployment | Existing |

---

## Integration Points

### Crossplane Integration

The Control Plane will integrate with Crossplane in two ways:

1. **Direct Kubernetes API**: If deployed in the same cluster
   ```python
   from kubernetes import client, config
   
   # Load in-cluster config
   config.load_incluster_config()
   v1 = client.CustomObjectsApi()
   
   # Create a ComputeInstance
   v1.create_namespaced_custom_object(
       group="compute.aws.crossplane.io",
       version="v1beta1",
       namespace="default",
       plural="ec2instances",
       body=ec2_instance_spec
   )
   ```

2. **Crossplane REST API**: If deployed separately
   ```python
   import httpx
   
   async with httpx.AsyncClient() as client:
       response = await client.post(
           "https://crossplane-api:9443/apis/compute.aws.crossplane.io/v1beta1/ec2instances",
           json=ec2_instance_spec,
           headers={"Authorization": "Bearer " + token}
       )
   ```

### NATS Integration

```python
import asyncio
import nats

async def connect_to_nats():
    nc = await nats.connect("nats://nats:4222")
    
    # Subscribe to events
    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")
    
    await nc.subscribe("iaas.events.>", cb=message_handler)
    
    # Publish events
    await nc.publish("iaas.events.vm.created", b'{"vm_id": "123"}')
```

---

## Security Considerations

### Authentication
- **API Gateway**: JWT tokens for user authentication
- **Service-to-Service**: mTLS for internal communication
- **Crossplane**: Kubernetes RBAC for resource access

### Authorization
- **RBAC**: Role-based access control for users
- **ABAC**: Attribute-based access control for fine-grained policies
- **Crossplane**: Uses Kubernetes RBAC

### Data Protection
- **Encryption at Rest**: PostgreSQL encryption, MinIO server-side encryption
- **Encryption in Transit**: TLS 1.3 for all external communication
- **Secrets Management**: HashiCorp Vault or Kubernetes Secrets

---

## Performance Considerations

### Scaling
- **API Gateway**: Stateless, can scale horizontally
- **Control Plane**: Stateless, can scale horizontally
- **Failover Manager**: Singleton (only one active instance)
- **PostgreSQL**: Vertical scaling with read replicas
- **Redis**: Cluster mode for horizontal scaling
- **NATS**: Cluster mode for horizontal scaling

### Caching
- **Redis**: Cache frequently accessed data (VM lists, user info)
- **API Gateway**: Cache provider capabilities
- **Control Plane**: Cache Crossplane resource states

---

## Failure Modes and Mitigations

| Component | Failure Mode | Detection | Mitigation |
|-----------|--------------|-----------|------------|
| API Gateway | Crash | Health check | Kubernetes restarts pod |
| Control Plane | Crash | Health check | Kubernetes restarts pod |
| Failover Manager | Crash | Health check | Kubernetes restarts pod |
| Crossplane | Crash | Health check | Kubernetes restarts controller |
| PostgreSQL | Crash | Connection error | Failover to replica |
| Redis | Crash | Connection error | Failover to cluster node |
| NATS | Crash | Connection error | Failover to cluster node |
| Provider | Outage | Health check | Failover Manager triggers failover |

---

## Open Questions

1. **Crossplane Deployment**: Should Crossplane run in the same Kubernetes cluster or separately?
2. **Provider Scope**: Which providers should we support initially? (Hetzner + AWS + DigitalOcean?)
3. **Web UI**: Should we start with Backstage or build a simple custom UI first?
4. **Authentication**: Should we use OAuth2/OIDC or build our own auth system?
5. **Multi-Tenancy**: How should we isolate resources between organizations?
6. **Billing**: Should we implement billing from day one or add it later?

---

## Comparison with Full Custom Build

| Aspect | Hybrid Approach | Full Custom Build |
|--------|-----------------|-------------------|
| Development Time | 3-6 months | 12-18 months |
| Maintenance | Medium | High |
| Flexibility | High | Higher |
| Control | Good | Full |
| Production Readiness | High | Medium (initially) |
| Community Support | High | Low (initially) |
| Unique Value | Focused | Diluted |

**Conclusion**: The Hybrid Approach gives us **80% of functionality with 20% of the effort**, allowing us to focus on our unique differentiators.
